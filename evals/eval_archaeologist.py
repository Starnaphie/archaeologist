"""Instrumented evaluation runner for the archaeologist repo analysis agent."""

import sys
import os
import json
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import OpenAI
from lambdas.archaeologist import embedder
from lambdas.archaeologist import parser as code_parser
from lambdas.archaeologist.agent import (
    _purpose_step,
    _architecture_step,
    run_incomplete_agent,
    build_mermaid_graph,
    detect_repo_owner,
    extract_setup_instructions,
    _extract_setup_single_pass,
    build_folder_hierarchy,
)
from .metrics import StepMetrics, EvalReport, timed_step
from .langchain_tokens import tracked_langchain_step
from .openai_tokens import accumulate_into
from .token_utils import check_token_coverage


_response_log: list = []
_openai_patch = None
_real_client = None


def _patch_openai_client() -> None:
    global _openai_patch
    mock_client = MagicMock()

    def _create(*args, **kwargs):
        response = _real_client.chat.completions.create(*args, **kwargs)
        _response_log.append(response)
        return response

    mock_client.chat.completions.create.side_effect = _create
    _openai_patch = patch(
        "lambdas.archaeologist.agent.OpenAI",
        return_value=mock_client,
    )
    _openai_patch.start()


def _unpatch_openai_client() -> None:
    global _openai_patch
    if _openai_patch is not None:
        _openai_patch.stop()
        _openai_patch = None


@contextmanager
def _capturing_openai():
    global _real_client
    _response_log.clear()
    _real_client = OpenAI()
    _patch_openai_client()
    try:
        yield
    finally:
        _unpatch_openai_client()
        _real_client = None


def _run_embedder_setup(root: str, report: EvalReport) -> None:
    with timed_step("Embedder Setup") as metrics:
        manifest = {
            "repo_name": os.path.basename(os.path.abspath(root)),
            "temp_dir": root,
            "files": [
                os.path.join(dirpath, filename)
                for dirpath, dirnames, filenames in os.walk(root)
                for filename in filenames
                if filename.endswith(".py")
                and "__pycache__" not in os.path.join(dirpath, filename).split(os.sep)
                and "venv" not in os.path.join(dirpath, filename).split(os.sep)
                and ".venv" not in os.path.join(dirpath, filename).split(os.sep)
                and ".git" not in os.path.join(dirpath, filename).split(os.sep)
                and "node_modules" not in os.path.join(dirpath, filename).split(os.sep)
            ],
        }
        parse_result = code_parser.parse_manifest(manifest)
        embedder.build_index(parse_result.chunks)
        metrics.model = "text-embedding-3-small"

        # Embedding API calls do not return usage in the same structure as chat completions.
        metrics.comment = "Token count is 0 because embedding API usage is not tracked like chat completions."

    report.add(metrics)


def _eval_purpose_step(root: str, report: EvalReport) -> tuple:
    result = ([], None)
    with timed_step("Purpose") as metrics:
        with tracked_langchain_step(metrics):
            chunks, purpose_output = _purpose_step(root)
            result = (chunks, purpose_output)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_architecture_step(root: str, report: EvalReport) -> tuple:
    result = ([], None, False)
    with timed_step("Architecture") as metrics:
        with tracked_langchain_step(metrics):
            chunks, architecture_output, was_chunked = _architecture_step(root)
            result = (chunks, architecture_output, was_chunked)
        metrics.model = "gpt-4o-mini"
        if result[2]:
            metrics.step_name += " [chunked]"

    report.add(metrics)
    return result


def _eval_incomplete_step(root: str, report: EvalReport) -> tuple:
    result = ([], None)
    with timed_step("Incomplete Features") as metrics:
        with tracked_langchain_step(metrics):
            chunks, incomplete_output = run_incomplete_agent(root)
            result = (chunks, incomplete_output)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_mermaid_step(symbol_map: dict, report: EvalReport) -> str:
    graph_string = ""
    with timed_step("Mermaid Graph") as metrics:
        graph_string = build_mermaid_graph(symbol_map)

    report.add(metrics)
    return graph_string


def _eval_repo_owner_step(root: str, report: EvalReport) -> dict:
    result = {}
    with timed_step("Repo Owner Detection") as metrics:
        result = detect_repo_owner(root)

    report.add(metrics)
    return result


def _eval_setup_pass1(root: str, report: EvalReport) -> dict:
    result = {}
    with timed_step("Setup Extraction — Pass 1 (baseline)") as metrics:
        with _capturing_openai():
            result = _extract_setup_single_pass(root)
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_setup_pass2(root: str, report: EvalReport) -> dict:
    result = {}
    with timed_step("Setup Extraction — Pass 2 (with README)") as metrics:
        with _capturing_openai():
            result = extract_setup_instructions(root)
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_folder_hierarchy_step(root: str, report: EvalReport) -> dict:
    result = {}
    with timed_step("Folder Hierarchy") as metrics:
        with _capturing_openai():
            result = build_folder_hierarchy(root)
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def run_archaeologist_eval(root: str) -> EvalReport:
    report = EvalReport(label="Archaeologist")
    _run_embedder_setup(root, report)
    purpose_chunks, purpose_output = _eval_purpose_step(root, report)
    arch_chunks, architecture_output, was_chunked = _eval_architecture_step(root, report)
    inc_chunks, incomplete_output = _eval_incomplete_step(root, report)
    symbol_map = embedder.build_symbol_map() if hasattr(embedder, "build_symbol_map") else {}
    _eval_mermaid_step(symbol_map, report)
    _eval_repo_owner_step(root, report)
    _eval_setup_pass1(root, report)
    _eval_setup_pass2(root, report)
    _eval_folder_hierarchy_step(root, report)

    warnings = check_token_coverage(
        report,
        skip_steps={"Embedder Setup", "Mermaid Graph", "Repo Owner Detection"},
    )
    for w in warnings:
        print(w, file=sys.stderr)

    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m evals.eval_archaeologist <path_to_repo>")
        sys.exit(1)
    root_path = sys.argv[1]
    result = run_archaeologist_eval(root_path)
    try:
        from .reporter import print_report

        print_report(result)
    except ModuleNotFoundError:
        print(result)
