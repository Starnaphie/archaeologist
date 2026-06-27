"""Core metrics dataclass for eval instrumentation.

Usage:
    with timed_step("Purpose Step") as metrics:
        chunks, result = _purpose_step(root)
        metrics.prompt_tokens = 120
        metrics.completion_tokens = 80
        metrics.total_tokens = 200
    report.add(metrics)
"""

import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Optional

from .cost_config import compute_cost, format_cost


@dataclass
class StepMetrics:
    step_name: str
    wall_time_s: float = 0.0
    compute_time_s: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    cost_usd: float = 0.0
    error: Optional[str] = None

    @property
    def succeeded(self) -> bool:
        return self.error is None

    def compute_and_set_cost(self) -> None:
        if not self.model or self.total_tokens == 0:
            return
        self.cost_usd = compute_cost(
            self.model,
            self.prompt_tokens,
            self.completion_tokens,
        )

    def to_row(self) -> dict:
        return {
            "Step": self.step_name,
            "Runtime (s)": round(self.wall_time_s, 3),
            "Compute (s)": round(self.compute_time_s, 3),
            "Prompt Tokens": self.prompt_tokens,
            "Completion Tokens": self.completion_tokens,
            "Total Tokens": self.total_tokens,
            "Cost (USD)": format_cost(self.cost_usd),
            "Status": "OK" if self.succeeded else "FAILED",
        }


@dataclass
class EvalReport:
    steps: list[StepMetrics] = field(default_factory=list)
    label: str = ""

    @property
    def total_wall_time_s(self) -> float:
        return round(sum(step.wall_time_s for step in self.steps), 3)

    @property
    def total_compute_time_s(self) -> float:
        return round(sum(step.compute_time_s for step in self.steps), 3)

    @property
    def total_prompt_tokens(self) -> int:
        return sum(step.prompt_tokens for step in self.steps)

    @property
    def total_completion_tokens(self) -> int:
        return sum(step.completion_tokens for step in self.steps)

    @property
    def total_tokens(self) -> int:
        return sum(step.total_tokens for step in self.steps)

    @property
    def total_cost_usd(self) -> float:
        return round(sum(step.cost_usd for step in self.steps), 6)

    @property
    def all_succeeded(self) -> bool:
        return all(step.succeeded for step in self.steps)

    def totals_row(self) -> dict:
        return {
            "Step": "TOTAL",
            "Runtime (s)": self.total_wall_time_s,
            "Compute (s)": self.total_compute_time_s,
            "Prompt Tokens": self.total_prompt_tokens,
            "Completion Tokens": self.total_completion_tokens,
            "Total Tokens": self.total_tokens,
            "Cost (USD)": format_cost(self.total_cost_usd),
            "Status": "OK" if self.all_succeeded else "PARTIAL",
        }

    def add(self, step: StepMetrics) -> None:
        self.steps.append(step)


@contextmanager
def timed_step(step_name: str) -> StepMetrics:
    metrics = StepMetrics(step_name=step_name)
    wall_start = time.time()
    cpu_start = time.process_time()

    try:
        yield metrics
    except Exception as exception:
        print(f"[timed_step] '{step_name}' failed: {exception}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        metrics.error = str(exception)
    finally:
        metrics.wall_time_s = round(time.time() - wall_start, 3)
        metrics.compute_time_s = round(time.process_time() - cpu_start, 3)
        metrics.compute_and_set_cost()
