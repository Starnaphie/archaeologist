"""Lambda handler for the archaeologist agent. Clones the repo, indexes it, runs generate_report, validates output against FindingsSchema, and writes findings.json to S3. Re-raises all exceptions so Step Functions failure handling triggers correctly."""

import os
import json
import logging
import tempfile
from dataclasses import asdict

from .repo_cloner import clone_repo, cleanup_repo
from .event_parser import parse_event, build_output
from . import embedder
from . import parser as code_parser
from .agent import generate_report

from lambdas.shared.s3_io import write_json, build_key
from lambdas.shared.validation import load_and_validate_findings
from lambdas.shared.schemas import FindingsSchema


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


EXCLUDE_DIRS = {"__pycache__", "venv", ".venv", ".git", "node_modules"}


def _build_manifest(root: str) -> dict:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDE_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.abspath(os.path.join(dirpath, filename)))

    return {
        "repo_name": os.path.basename(os.path.abspath(root)),
        "temp_dir": root,
        "files": files,
        "file_count": len(files),
    }


def _ensure_findings_contract(report_dict: dict, repo_source: str) -> FindingsSchema:
    repo_name = repo_source.rstrip("/").split("/")[-1].removesuffix(".git")
    report_dict.setdefault(
        "repo_owner",
        {
            "owner": None,
            "repo_name": repo_name or None,
            "source": repo_source,
        },
    )
    report_dict.setdefault(
        "setup_instructions",
        {
            "setup_markdown": "",
            "files_used": [],
        },
    )
    report_dict.setdefault(
        "folder_hierarchy",
        {
            "folders": [],
            "root_files": [],
        },
    )
    report_dict.setdefault("acronyms", [])
    report_dict.setdefault("was_chunked", False)
    return report_dict


def handler(event: dict, context) -> dict:
    root = ""
    parsed = None
    try:
        parsed = parse_event(event)
        logger.info(
            f"Archaeologist started: execution_id={parsed.execution_id}, "
            f"repo={parsed.repo_source}"
        )

        tmp_dir = tempfile.mkdtemp()
        root = clone_repo(parsed.repo_source, tmp_dir)
        logger.info(f"Repo ready at: {root}")

        manifest = _build_manifest(root)
        parse_result = code_parser.parse_manifest(manifest)
        embedder.build_index(parse_result.chunks)
        logger.info(f"Embedder indexed {len(embedder._chunks)} chunks")

        report = generate_report(symbol_map=parse_result.symbol_map, root=root)
        logger.info(
            f"Report generated: {len(report.modules)} modules, "
            f"was_chunked={getattr(report, 'was_chunked', False)}"
        )

        report_dict = _ensure_findings_contract(asdict(report), parsed.repo_source)
        try:
            load_and_validate_findings(json.dumps(report_dict))
        except ValueError:
            logger.error("Generated findings failed validation", exc_info=True)
            raise

        findings_key = build_key(parsed.execution_id, "findings.json")
        write_json(findings_key, report_dict)
        logger.info(f"Wrote findings to s3 key: {findings_key}")

        return build_output(
            parsed.execution_id,
            findings_key,
            parsed.repo_source,
            parsed.topic,
            parsed.description,
        )
    except Exception as e:
        logger.error(f"Archaeologist failed: {e}", exc_info=True)
        raise
    finally:
        if parsed is not None and root:
            cleanup_repo(root, parsed.repo_source)
