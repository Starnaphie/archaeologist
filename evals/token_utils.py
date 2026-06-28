"""Utilities for merging EvalReports across agents and checking for token tracking gaps. Call check_token_coverage after building any report and print warnings before displaying the table."""

from .metrics import EvalReport, StepMetrics


def merge_metrics(a: StepMetrics, b: StepMetrics, merged_name: str) -> StepMetrics:
    errors = [error for error in (a.error, b.error) if error is not None]
    return StepMetrics(
        step_name=merged_name,
        wall_time_s=a.wall_time_s + b.wall_time_s,
        compute_time_s=a.compute_time_s + b.compute_time_s,
        prompt_tokens=a.prompt_tokens + b.prompt_tokens,
        completion_tokens=a.completion_tokens + b.completion_tokens,
        total_tokens=a.total_tokens + b.total_tokens,
        error=" | ".join(errors) if errors else None,
    )


def merge_reports(reports: list[EvalReport], label: str = "Combined") -> EvalReport:
    merged = EvalReport(label=label)
    for report in reports:
        merged.steps.extend(report.steps)
    return merged


def check_token_coverage(
    report: EvalReport,
    skip_steps: set[str] | None = None,
) -> list[str]:
    skip_steps = skip_steps or set()
    warnings: list[str] = []
    for step in report.steps:
        if step.step_name in skip_steps:
            continue
        if step.succeeded and step.total_tokens == 0:
            warnings.append(
                f"WARNING: step '{step.step_name}' succeeded but recorded 0 tokens — token tracking may have failed for this step."
            )
    return warnings
