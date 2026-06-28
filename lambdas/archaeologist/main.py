import asyncio
import json
import shutil
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Dict

import git.exc

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from . import agent, embedder, ingestion
from . import parser as code_parser
from .agent import (
    _purpose_step,
    _architecture_step,
    run_incomplete_agent,
    detect_repo_owner,
    extract_setup_instructions,
    build_folder_hierarchy,
    _rel_path,
    generate_readme_from_report,
)

from dotenv import load_dotenv

# Walk up to repo root .env regardless of where the process is invoked from
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

app = FastAPI(title="archaeologist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORTS: Dict[str, dict] = {}

USE_MULTI_AGENT = False


class AnalyzeRequest(BaseModel):
    github_url: str


class ReadmeRequest(BaseModel):
    github_url: str
    job_id: str | None = None


async def _run_pipeline(github_url: str, job_id: str):
    yield {"event": "job_id", "data": job_id}

    # ── Clone ──────────────────────────────────────────────────────────
    yield {"event": "progress", "data": "Cloning repo..."}
    try:
        manifest = await asyncio.to_thread(ingestion.clone_and_manifest, github_url)
    except (git.exc.GitCommandError, git.exc.InvalidGitRepositoryError):
        yield {"event": "error", "data": "Could not clone repository. Check the URL and make sure it is public."}
        return
    if manifest["file_count"] == 0:
        yield {"event": "error", "data": "No Python files found. This tool currently supports Python repositories only."}
        return

    root = manifest["temp_dir"]

    # ── Parse ──────────────────────────────────────────────────────────
    yield {"event": "progress", "data": f"Parsing {manifest['file_count']} files..."}
    try:
        parse_result = await asyncio.to_thread(code_parser.parse_manifest, manifest)
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at parsing: {str(e)}"}
        shutil.rmtree(root, ignore_errors=True)
        return

    # ── Embed ──────────────────────────────────────────────────────────
    yield {"event": "progress", "data": "Embedding chunks..."}
    try:
        await asyncio.to_thread(embedder.build_index, parse_result.chunks)
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at embedding: {str(e)}"}
        shutil.rmtree(root, ignore_errors=True)
        return

    # ── Section 1: Purpose, Repo Owner, Incomplete ─────────────────────
    yield {"event": "progress", "data": "Analyzing purpose and structure..."}
    try:
        purpose_chunks, purpose_out = await asyncio.to_thread(_purpose_step, root)
        inc_chunks, incomplete_out = await asyncio.to_thread(run_incomplete_agent, root)
        repo_owner = await asyncio.to_thread(detect_repo_owner, root)

        section1 = {
            "purpose": purpose_out.purpose,
            "one_liner": purpose_out.one_liner,
            "purpose_citations": [
                {"file_path": _rel_path(c.get("file_path", ""), root), "name": c.get("name", ""), "kind": c.get("kind", ""), "source": c.get("source", "")[:300]}
                for c in purpose_chunks
            ],
            "incomplete_features": list(incomplete_out.incomplete_features),
            "incomplete_citations": [
                {"file_path": _rel_path(c.get("file_path", ""), root), "name": c.get("name", ""), "kind": c.get("kind", ""), "source": c.get("source", "")[:300]}
                for c in inc_chunks
            ],
            "repo_owner": repo_owner,
        }
        yield {"event": "section", "data": json.dumps(section1)}
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at purpose step: {str(e)}"}
        shutil.rmtree(root, ignore_errors=True)
        return

    # ── Section 2: Architecture ────────────────────────────────────────
    yield {"event": "progress", "data": "Analyzing architecture (this may take a moment)..."}
    try:
        arch_chunks, architecture_out, was_chunked = await asyncio.to_thread(_architecture_step, root)

        from dataclasses import asdict as _asdict
        modules = []
        for m in architecture_out.modules:
            d = m.model_dump() if hasattr(m, "model_dump") else _asdict(m)
            modules.append(d)

        section2 = {
            "modules": modules,
            "module_citations": [
                {"file_path": _rel_path(c.get("file_path", ""), root), "name": c.get("name", ""), "kind": c.get("kind", ""), "source": c.get("source", "")[:300]}
                for c in arch_chunks
            ],
            "was_chunked": was_chunked,
        }
        yield {"event": "section", "data": json.dumps(section2)}
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at architecture step: {str(e)}"}
        shutil.rmtree(root, ignore_errors=True)
        return

    # ── Section 3: Folder Hierarchy ────────────────────────────────────
    yield {"event": "progress", "data": "Mapping folder structure..."}
    try:
        folder_hierarchy = await asyncio.to_thread(build_folder_hierarchy, root)
        yield {"event": "section", "data": json.dumps({"folder_hierarchy": folder_hierarchy})}
    except Exception as e:
        # Non-fatal — yield empty hierarchy and continue
        yield {"event": "section", "data": json.dumps({"folder_hierarchy": {"folders": [], "root_files": []}})}

    # ── Section 4: Setup Instructions ──────────────────────────────────
    yield {"event": "progress", "data": "Extracting setup instructions..."}
    try:
        setup_instructions = await asyncio.to_thread(extract_setup_instructions, root)
        yield {"event": "section", "data": json.dumps({"setup_instructions": setup_instructions})}
    except Exception as e:
        # Non-fatal — yield empty setup and continue
        yield {"event": "section", "data": json.dumps({"setup_instructions": {"setup_markdown": "", "files_used": [], "skipped": True}})}

    # ── Done ───────────────────────────────────────────────────────────
    # Build full report dict for REPORTS cache (used by /report/{job_id})
    report_dict = {
        **section1,
        **section2,
        "folder_hierarchy": folder_hierarchy if "folder_hierarchy" in dir() else {"folders": [], "root_files": []},
        "setup_instructions": setup_instructions if "setup_instructions" in dir() else {"setup_markdown": "", "files_used": [], "skipped": True},
        "dependency_graph": "",  # intentionally omitted from SSE — left for future use
    }
    REPORTS[job_id] = report_dict
    yield {"event": "done", "data": "{}"}
    shutil.rmtree(root, ignore_errors=True)


async def _run_readme_pipeline(github_url: str, job_id: str | None = None):
    if job_id and job_id in REPORTS:
        yield {"event": "progress", "data": "Using existing analysis to generate README..."}
        try:
            readme = await asyncio.to_thread(generate_readme_from_report, REPORTS[job_id])
            yield {"event": "done", "data": json.dumps({"content": readme})}
        except Exception as e:
            yield {"event": "error", "data": f"README generation failed: {str(e)}"}
        return

    yield {"event": "progress", "data": "Cloning repo..."}
    try:
        manifest = await asyncio.to_thread(ingestion.clone_and_manifest, github_url)
    except (git.exc.GitCommandError, git.exc.InvalidGitRepositoryError):
        yield {"event": "error", "data": "Could not clone repository. Check the URL and make sure it is public."}
        return

    if manifest["file_count"] == 0:
        yield {"event": "error", "data": "No Python files found. This tool currently supports Python repositories only."}
        return

    yield {"event": "progress", "data": "Parsing files..."}
    try:
        parse_result = await asyncio.to_thread(code_parser.parse_manifest, manifest)
    except Exception as e:
        yield {"event": "error", "data": f"README generation failed at parsing: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    yield {"event": "progress", "data": "Embedding..."}
    try:
        await asyncio.to_thread(embedder.build_index, parse_result.chunks)
    except Exception as e:
        yield {"event": "error", "data": f"README generation failed at embedding: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    print(f"README: index built with {len(embedder._chunks)} chunks")

    yield {"event": "progress", "data": "Generating README..."}
    try:
        readme = await asyncio.to_thread(agent.generate_readme, manifest["temp_dir"])
    except Exception as e:
        yield {"event": "error", "data": f"README generation failed at reasoning: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    print(f"README result length: {len(readme)}")
    print(f"README first 200 chars: {readme[:200]}")

    yield {"event": "done", "data": json.dumps({"content": readme})}
    shutil.rmtree(manifest["temp_dir"], ignore_errors=True)


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    job_id = str(uuid.uuid4())
    return EventSourceResponse(_run_pipeline(req.github_url, job_id))


@app.post("/generate-readme")
async def generate_readme_endpoint(req: ReadmeRequest):
    return EventSourceResponse(_run_readme_pipeline(req.github_url, req.job_id))


@app.get("/report/{job_id}")
async def get_report(job_id: str):
    if job_id not in REPORTS:
        raise HTTPException(status_code=404, detail="report not found")
    return REPORTS[job_id]
