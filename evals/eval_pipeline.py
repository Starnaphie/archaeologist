"""Instrumented evaluation runner for the 4-pass slides generation pipeline. Each pass is wrapped with timed_step and a capturing OpenAI client to record wall time, CPU time, and token usage per pass and in total."""

import sys
import os
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lambdas.slides.openai_agent import (
    _pass_progression,
    _pass_paragraph_content,
    _pass_template_and_content,
    _pass_speaker_notes,
    _build_system_prompt,
)
from openai import OpenAI
from .metrics import StepMetrics, EvalReport, timed_step
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


def _eval_pass_progression(
    topic: str,
    description: str,
    audience: str,
    tone: str,
    max_slides: int,
    report: EvalReport,
) -> list[dict]:
    progression: list[dict] = []
    with timed_step("Pass 1 — Progression") as metrics:
        with _capturing_openai():
            progression = _pass_progression(
                topic,
                description,
                audience,
                tone,
                max_slides,
            )
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o"

    report.add(metrics)
    return progression


def _eval_pass_paragraph_content(
    progression: list[dict],
    topic: str,
    audience: str,
    tone: str,
    report: EvalReport,
) -> list[dict]:
    paragraphs: list[dict] = []
    with timed_step("Pass 2 — Paragraph Content") as metrics:
        with _capturing_openai():
            paragraphs = _pass_paragraph_content(
                progression,
                topic,
                audience,
                tone,
            )
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o"
        # Batch count for debugging: len(_response_log).
        metrics.batch_count = len(_response_log)

    report.add(metrics)
    return paragraphs


def _eval_pass_template_and_content(
    paragraphs: list[dict],
    audience: str,
    tone: str,
    report: EvalReport,
) -> list[dict]:
    expanded_slides: list[dict] = []
    with timed_step("Pass 3 — Template and Content") as metrics:
        with _capturing_openai():
            expanded_slides = _pass_template_and_content(
                paragraphs,
                audience,
                tone,
            )
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o"
        print(
            f"  [Pass 3] {len(paragraphs)} paragraphs → {len(expanded_slides)} slides"
        )

    report.add(metrics)
    return expanded_slides


def _eval_pass_speaker_notes(
    slides: list[dict],
    paragraphs: list[dict],
    audience: str,
    tone: str,
    report: EvalReport,
) -> list[dict]:
    slides_with_notes: list[dict] = []
    with timed_step("Pass 4 — Speaker Notes") as metrics:
        with _capturing_openai():
            slides_with_notes = _pass_speaker_notes(
                slides,
                paragraphs,
                audience,
                tone,
            )
        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o"

        empty_notes_count = sum(
            1
            for slide in slides_with_notes
            if not slide.get("speaker_notes")
        )
        if slides_with_notes and empty_notes_count > len(slides_with_notes) / 2:
            metrics.error = (
                "WARNING: majority of slides have empty speaker_notes — Pass 4 may have partially failed"
            )

    report.add(metrics)
    return slides_with_notes


def _eval_title_inference(
    topic: str,
    audience: str,
    tone: str,
    slide_titles: list[str],
    report: EvalReport,
) -> str:
    inferred_title = ""
    with timed_step("Title Inference") as metrics:
        with _capturing_openai():
            numbered_titles = "\n".join(
                f"{index + 1}. {title}" for index, title in enumerate(slide_titles)
            )
            client = _pass_progression.__globals__["OpenAI"]()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=64,
                messages=[
                    {"role": "system", "content": _build_system_prompt(audience, tone)},
                    {
                        "role": "user",
                        "content": (
                            f"Topic: {topic}\n"
                            f"Slide titles:\n{numbered_titles}\n"
                            "Return only a concise compelling presentation title — no punctuation at the end, no quotes, no explanation. 8 words maximum."
                        ),
                    },
                ],
            )
            inferred_title = response.choices[0].message.content.strip()
            inferred_title = inferred_title.strip('"').strip("'").rstrip(".!?")

        for response in _response_log:
            accumulate_into(metrics, response)
        metrics.model = "gpt-4o-mini"

    report.add(metrics)
    return inferred_title


def run_pipeline_eval(
    topic: str,
    audience: str,
    tone: str = "professional",
    description: str = "",
    num_slides: int | None = None,
) -> tuple[EvalReport, dict]:
    report = EvalReport(label="Pipeline")
    max_slides = num_slides if num_slides is not None else 20

    progression = _eval_pass_progression(
        topic,
        description,
        audience,
        tone,
        max_slides,
        report,
    )
    if not progression:
        print("Pass 1 failed — aborting pipeline eval", file=sys.stderr)
        return report, {}

    paragraphs = _eval_pass_paragraph_content(
        progression,
        topic,
        audience,
        tone,
        report,
    )
    expanded_slides = _eval_pass_template_and_content(
        paragraphs,
        audience,
        tone,
        report,
    )
    slides_with_notes = _eval_pass_speaker_notes(
        expanded_slides,
        paragraphs,
        audience,
        tone,
        report,
    )
    slide_titles = [slide["title"] for slide in slides_with_notes]
    title = _eval_title_inference(
        topic,
        audience,
        tone,
        slide_titles,
        report,
    )

    paragraphs_by_index = {
        item.get("index"): item.get("paragraph", "")
        for item in paragraphs
        if isinstance(item, dict)
    }
    for slide in slides_with_notes:
        source_index = slide.get("source_index")
        slide["_paragraph"] = paragraphs_by_index.get(source_index, "")
        slide["_source_index"] = source_index

    outline = {
        "title": title,
        "slides": slides_with_notes,
    }

    warnings = check_token_coverage(report)
    for warning in warnings:
        print(warning, file=sys.stderr)

    return report, outline


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--tone", default="professional")
    parser.add_argument("--description", default="")
    parser.add_argument("--num-slides", type=int, default=None)
    args = parser.parse_args()
    result_report, result_outline = run_pipeline_eval(
        topic=args.topic,
        audience=args.audience,
        tone=args.tone,
        description=args.description,
        num_slides=args.num_slides,
    )
    try:
        from .reporter import print_report

        print_report(result_report)
    except ModuleNotFoundError:
        print(result_report)
