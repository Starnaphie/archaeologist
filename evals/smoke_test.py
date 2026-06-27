from .metrics import StepMetrics, EvalReport, timed_step
from .reporter import print_report, print_combined_report
import time


def _fake_step(
    name: str,
    wall: float,
    cpu: float,
    prompt: int,
    completion: int,
    error: str | None = None,
    model: str = "",
) -> StepMetrics:
    metrics = StepMetrics(
        step_name=name,
        wall_time_s=wall,
        compute_time_s=cpu,
        prompt_tokens=prompt,
        completion_tokens=completion,
        total_tokens=prompt + completion,
        model=model,
        error=error,
    )
    metrics.compute_and_set_cost()
    return metrics


def run_smoke_test() -> None:
    arch_report = EvalReport(label="Archaeologist (smoke)")
    arch_report.add(_fake_step("Embedder Setup", 1.2, 0.8, 0, 0, None))
    arch_report.add(
        _fake_step("Purpose Step", 3.4, 1.1, 420, 180, None, model="gpt-4o-mini")
    )
    arch_report.add(
        _fake_step("Architecture Step", 8.7, 2.3, 1100, 450, None, model="gpt-4o-mini")
    )
    arch_report.add(
        _fake_step(
            "Incomplete Features Step",
            2.1,
            0.7,
            310,
            90,
            None,
            model="gpt-4o-mini",
        )
    )
    arch_report.add(_fake_step("Mermaid Graph", 0.3, 0.3, 0, 0, None))

    pipeline_report = EvalReport(label="Pipeline (smoke)")
    pipeline_report.add(
        _fake_step("Pass 1 — Progression", 4.2, 1.5, 510, 220, None, model="gpt-4o")
    )
    pipeline_report.add(
        _fake_step(
            "Pass 2 — Paragraph Content",
            12.8,
            3.9,
            2400,
            980,
            None,
            model="gpt-4o",
        )
    )
    pipeline_report.add(
        _fake_step(
            "Pass 3 — Template and Content",
            15.3,
            4.7,
            3100,
            1400,
            None,
            model="gpt-4o",
        )
    )
    pipeline_report.add(
        _fake_step(
            "Pass 4 — Speaker Notes",
            9.6,
            2.8,
            1800,
            720,
            None,
            model="gpt-4o",
        )
    )
    pipeline_report.add(
        _fake_step("Title Inference", 1.1, 0.4, 180, 20, None, model="gpt-4o")
    )

    print_combined_report([arch_report, pipeline_report])

    failure_report = EvalReport(label="Partial Failure (smoke)")
    failure_report.add(
        _fake_step("Timeout Step", 5.0, 1.2, 300, 0, "Simulated timeout")
    )
    print_report(failure_report)

    print("Smoke test passed.")


if __name__ == "__main__":
    run_smoke_test()
