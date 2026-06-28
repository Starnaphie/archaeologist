"""Tool selection eval suite for the slides revision agent. Tests whether revise_with_tools picks the correct tool for 18 natural-language instructions covering all supported tools and unsupported request categories."""

import json
import sys
import os
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lambdas.slides.openai_agent import revise_with_tools
from openai import OpenAI

from .metrics import EvalReport, timed_step
from .openai_tokens import accumulate_into
from .token_utils import check_token_coverage


STUB_OUTLINE = {
    "title": "Introduction to Retrieval-Augmented Generation",
    "slides": [
        {"layout": "title_slide", "title": "Introduction to RAG", "content": {}, "speaker_notes": []},
        {"layout": "big_statement", "title": "LLMs hallucinate without grounding", "content": {"statement": "70% of LLM errors stem from lack of context"}, "speaker_notes": []},
        {"layout": "title_and_content", "title": "How RAG works", "content": {"bullets": ["Retrieve relevant documents", "Augment the prompt", "Generate grounded output"]}, "speaker_notes": []},
        {"layout": "two_column", "title": "RAG vs Fine-tuning", "content": {"left_header": "RAG", "left_bullets": ["No retraining", "Always current"], "right_header": "Fine-tuning", "right_bullets": ["Baked-in knowledge", "Expensive to update"]}, "speaker_notes": []},
        {"layout": "section_header", "title": "Implementation", "content": {"heading": "Implementation", "subheading": "Building a RAG pipeline"}, "speaker_notes": []},
        {"layout": "title_and_content", "title": "Vector databases are the backbone", "content": {"bullets": ["Embed documents", "Store vectors", "Query by similarity"]}, "speaker_notes": []},
        {"layout": "closing", "title": "Start small, iterate fast", "content": {"headline": "Start small, iterate fast", "cta": "Try RAG on your next project"}, "speaker_notes": []},
    ],
}


TEST_CASES = [
    {"instruction": "make it 5 slides", "expected_tool": "set_slide_count", "expected_args_subset": {"target_count": 5}},
    {"instruction": "trim to 10 slides", "expected_tool": "set_slide_count", "expected_args_subset": {"target_count": 10}},
    {"instruction": "I only want 4 slides", "expected_tool": "set_slide_count", "expected_args_subset": {"target_count": 4}},
    {"instruction": "cut it down to 6", "expected_tool": "set_slide_count", "expected_args_subset": {"target_count": 6}},
    {"instruction": "give me exactly 8 slides", "expected_tool": "set_slide_count", "expected_args_subset": {"target_count": 8}},
    {"instruction": "add a slide about vector databases", "expected_tool": "add_slides"},
    {"instruction": "add two slides covering evaluation metrics for RAG", "expected_tool": "add_slides"},
    {"instruction": "I need a slide on cost considerations", "expected_tool": "add_slides"},
    {"instruction": "delete the last slide", "expected_tool": "delete_slides"},
    {"instruction": "remove slide 3", "expected_tool": "delete_slides"},
    {"instruction": "get rid of the RAG vs Fine-tuning slide", "expected_tool": "delete_slides"},
    {"instruction": "change the title of slide 2 to 'Hallucination is a real problem'", "expected_tool": "update_slides"},
    {"instruction": "rewrite the bullets on the How RAG works slide to be shorter", "expected_tool": "update_slides"},
    {"instruction": "move the closing slide to be second", "expected_tool": "reorder_slides"},
    {"instruction": "swap the order of slides 3 and 4", "expected_tool": "reorder_slides"},
    {"instruction": "change the font to Arial", "expected_tool": "respond"},
    {"instruction": "add an image of a neural network to slide 2", "expected_tool": "respond"},
    {"instruction": "export this as a PDF", "expected_tool": "respond"},
]


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
        "lambdas.slides.openai_agent.OpenAI",
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


def _matches_expected_args(tool_args: dict, expected_args_subset: dict) -> bool:
    return all(tool_args.get(key) == value for key, value in expected_args_subset.items())


def run_tool_call_evals(report: EvalReport | None = None) -> dict:
    if report is None:
        report = EvalReport(label="Tool Call Evals")

    total = 0
    passed = 0
    failed = 0
    failures = []

    for case in TEST_CASES:
        total += 1
        tool_result = None
        with timed_step(f"Tool: {case['instruction'][:40]}") as metrics:
            with _capturing_openai():
                tool_result = revise_with_tools(
                    history=[],
                    current_outline=STUB_OUTLINE,
                    instruction=case["instruction"],
                )
            for response in _response_log:
                accumulate_into(metrics, response)
            metrics.model = "gpt-4o"

            expected_tool = case["expected_tool"]
            check_passed = tool_result.tool_name == expected_tool
            expected_args_subset = case.get("expected_args_subset")
            if expected_args_subset:
                check_passed = check_passed and _matches_expected_args(
                    tool_result.tool_args,
                    expected_args_subset,
                )

            if check_passed:
                passed += 1
            else:
                failed += 1
                failures.append(
                    {
                        "instruction": case["instruction"],
                        "expected": expected_tool,
                        "got": tool_result.tool_name,
                        "args": tool_result.tool_args,
                    }
                )
                metrics.error = f"expected {expected_tool}, got {tool_result.tool_name}"

        report.add(metrics)

    check_token_coverage(report, skip_steps=set())
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 1),
        "failures": failures,
    }


if __name__ == "__main__":
    result = run_tool_call_evals()
    print(json.dumps(result, indent=2))
    if result["failures"]:
        print(f"\n{result['failed']}/{result['total']} cases failed.")
        sys.exit(1)
    else:
        print(f"\nAll {result['total']} cases passed.")
