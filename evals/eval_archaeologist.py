"""Instrumented evaluation runner for the archaeologist repo analysis agent. Each step in generate_report is wrapped with timed_step and tracked_langchain_step to capture wall time, CPU time, and token usage independently."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lambdas.archaeologist import embedder
from lambdas.archaeologist import parser as code_parser
from lambdas.archaeologist.agent import (
    _purpose_step,
    _architecture_step,
    run_incomplete_agent,
    build_mermaid_graph,
)
from .metrics import StepMetrics, EvalReport, timed_step
from .langchain_tokens import tracked_langchain_step
from .token_utils import check_token_coverage


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
    with timed_step("Purpose Step") as metrics:
        with tracked_langchain_step(metrics):
            chunks, purpose_output = _purpose_step(root)
            result = (chunks, purpose_output)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_architecture_step(root: str, report: EvalReport) -> tuple:
    result = ([], None)
    with timed_step("Architecture Step") as metrics:
        with tracked_langchain_step(metrics):
            chunks, architecture_output = _architecture_step(root)
            result = (chunks, architecture_output)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return result


def _eval_incomplete_step(root: str, report: EvalReport) -> tuple:
    result = ([], None)
    with timed_step("Incomplete Features Step") as metrics:
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
        metrics.model = ""

    report.add(metrics)
    return graph_string


def run_archaeologist_eval(root: str) -> EvalReport:
    report = EvalReport(label="Archaeologist")
    _run_embedder_setup(root, report)
    purpose_chunks, purpose_output = _eval_purpose_step(root, report)
    arch_chunks, architecture_output = _eval_architecture_step(root, report)
    inc_chunks, incomplete_output = _eval_incomplete_step(root, report)

    if hasattr(embedder, "build_symbol_map"):
        symbol_map = embedder.build_symbol_map()
    else:
        symbol_map = {}
    _eval_mermaid_step(symbol_map, report)

    warnings = check_token_coverage(
        report,
        skip_steps={"Embedder Setup", "Mermaid Graph"},
    )
    for warning in warnings:
        print(warning, file=sys.stderr)

    return report


if __name__ == "__main__":
    import sys

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
