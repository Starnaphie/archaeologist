import asyncio
import json
import shutil
import uuid
from dataclasses import asdict
from typing import Dict

import git.exc

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from . import agent, embedder, ingestion
from . import parser as code_parser

app = FastAPI(title="archaeologist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORTS: Dict[str, dict] = {}

USE_MULTI_AGENT = True


class AnalyzeRequest(BaseModel):
    github_url: str


async def _run_pipeline(github_url: str, job_id: str):
    yield {"event": "job_id", "data": job_id}

    yield {"event": "progress", "data": "Cloning repo..."}
    try:
        manifest = await asyncio.to_thread(ingestion.clone_and_manifest, github_url)
    except (git.exc.GitCommandError, git.exc.InvalidGitRepositoryError):
        yield {"event": "error", "data": "Could not clone repository. Check the URL and make sure it is public."}
        return

    if manifest["file_count"] == 0:
        yield {"event": "error", "data": "No Python files found. This tool currently supports Python repositories only."}
        return

    yield {"event": "progress", "data": f"Parsing {manifest['file_count']} files..."}
    try:
        parse_result = await asyncio.to_thread(code_parser.parse_manifest, manifest)
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at parsing: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    yield {"event": "progress", "data": "Embedding chunks..."}
    try:
        await asyncio.to_thread(embedder.build_index, parse_result.chunks)
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at embedding: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    yield {"event": "progress", "data": "Running analysis..."}
    try:
        if USE_MULTI_AGENT:
            from .multi_agent import build_agent_graph
            graph = build_agent_graph()
            state = await asyncio.to_thread(
                graph.invoke, {"manifest": manifest, "root": manifest["temp_dir"]}
            )
            report = await asyncio.to_thread(
                agent.generate_report_multi_agent,
                state, parse_result.symbol_map, manifest["temp_dir"]
            )
        else:
            report = await asyncio.to_thread(
                agent.generate_report, parse_result.symbol_map, manifest["temp_dir"]
            )
    except Exception as e:
        yield {"event": "error", "data": f"Analysis failed at reasoning: {str(e)}"}
        shutil.rmtree(manifest["temp_dir"], ignore_errors=True)
        return

    report_dict = asdict(report)
    REPORTS[job_id] = report_dict
    yield {"event": "done", "data": json.dumps(report_dict)}
    shutil.rmtree(manifest["temp_dir"], ignore_errors=True)


async def _run_readme_pipeline(github_url: str):
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
async def generate_readme(req: AnalyzeRequest):
    return EventSourceResponse(_run_readme_pipeline(req.github_url))


@app.get("/report/{job_id}")
async def get_report(job_id: str):
    if job_id not in REPORTS:
        raise HTTPException(status_code=404, detail="report not found")
    return REPORTS[job_id]
