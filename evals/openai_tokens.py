"""Token extraction utilities for raw OpenAI client responses. Use accumulate_into inside each batch iteration so token counts aggregate correctly across all calls in a single pass."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .metrics import StepMetrics

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletion


def extract_usage(response: ChatCompletion) -> dict:
    usage = response.usage
    if usage is None:
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }


def accumulate_into(metrics: StepMetrics, response: ChatCompletion) -> None:
    usage = extract_usage(response)
    metrics.prompt_tokens += usage["prompt_tokens"]
    metrics.completion_tokens += usage["completion_tokens"]
    metrics.total_tokens += usage["total_tokens"]


def sum_usages(responses: list[ChatCompletion]) -> dict:
    totals = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    for response in responses:
        usage = extract_usage(response)
        totals["prompt_tokens"] += usage["prompt_tokens"]
        totals["completion_tokens"] += usage["completion_tokens"]
        totals["total_tokens"] += usage["total_tokens"]

    return totals
