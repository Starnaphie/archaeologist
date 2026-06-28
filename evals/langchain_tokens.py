"""Token extraction utilities for LangChain ChatOpenAI calls. Use tracked_langchain_step inside a timed_step block — it accumulates token counts from all LangChain LLM calls that occur within the with block."""

from contextlib import contextmanager

from langchain_community.callbacks import get_openai_callback

from .metrics import StepMetrics


@contextmanager
def tracked_langchain_step(metrics: StepMetrics):
    with get_openai_callback() as cb:
        try:
            yield
        finally:
            usage = extract_langchain_usage(cb)
            metrics.prompt_tokens += usage["prompt_tokens"]
            metrics.completion_tokens += usage["completion_tokens"]
            metrics.total_tokens += usage["total_tokens"]


def extract_langchain_usage(cb) -> dict:
    return {
        "prompt_tokens": getattr(cb, "prompt_tokens", 0),
        "completion_tokens": getattr(cb, "completion_tokens", 0),
        "total_tokens": getattr(cb, "total_tokens", 0),
    }
