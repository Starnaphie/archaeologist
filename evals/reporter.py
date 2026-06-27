"""Console table formatter for EvalReport. Handles single-agent and combined multi-agent output with section headers and grand totals."""

from .cost_config import format_cost
from .metrics import EvalReport, StepMetrics


COLUMNS = [
    "Step",
    "Runtime (s)",
    "Compute (s)",
    "Prompt Tokens",
    "Completion Tokens",
    "Total Tokens",
    "Cost (USD)",
    "Status",
]

NUMERIC_COLUMNS = {
    "Runtime (s)",
    "Compute (s)",
    "Prompt Tokens",
    "Completion Tokens",
    "Total Tokens",
    "Cost (USD)",
}


def _col_widths(rows: list[dict]) -> dict[str, int]:
    widths = {}
    for column in COLUMNS:
        widths[column] = max(
            [len(column)]
            + [len(str(row.get(column, ""))) for row in rows]
        )
    return widths


def _render_row(row: dict, widths: dict[str, int]) -> str:
    rendered = []
    for column in COLUMNS:
        value = str(row.get(column, ""))
        if column in NUMERIC_COLUMNS:
            rendered.append(value.rjust(widths[column]))
        else:
            rendered.append(value.ljust(widths[column]))
    return " │ ".join(rendered)


def _render_divider(widths: dict[str, int]) -> str:
    return "─┼─".join("─" * widths[column] for column in COLUMNS)


def _render_totals_divider(widths: dict[str, int]) -> str:
    return "═╪═".join("═" * widths[column] for column in COLUMNS)


def print_report(report: EvalReport) -> None:
    if report.label:
        print(f"\n── {report.label} ──")

    step_rows = [step.to_row() for step in report.steps]
    display_step_rows = []
    for step, row in zip(report.steps, step_rows):
        display_row = dict(row)
        if step.error is not None:
            display_row["Step"] = f"{display_row['Step']} ✗"
        display_step_rows.append(display_row)

    totals_row = report.totals_row()
    all_rows = display_step_rows + [totals_row]
    widths = _col_widths(all_rows)

    header = {column: column for column in COLUMNS}
    print(_render_row(header, widths))
    print(_render_divider(widths))

    for row in display_step_rows:
        print(_render_row(row, widths))

    print(_render_totals_divider(widths))
    print(_render_row(totals_row, widths))
    print()


def print_combined_report(reports: list[EvalReport]) -> None:
    print("\n══ COMBINED EVAL REPORT ══\n")
    for report in reports:
        print_report(report)

    total_wall_time_s = round(
        sum(step.wall_time_s for report in reports for step in report.steps), 3
    )
    total_compute_time_s = round(
        sum(step.compute_time_s for report in reports for step in report.steps), 3
    )
    total_prompt_tokens = sum(
        step.prompt_tokens for report in reports for step in report.steps
    )
    total_completion_tokens = sum(
        step.completion_tokens for report in reports for step in report.steps
    )
    total_tokens = sum(
        step.total_tokens for report in reports for step in report.steps
    )
    total_cost_usd = round(
        sum(step.cost_usd for report in reports for step in report.steps), 6
    )
    all_succeeded = all(report.all_succeeded for report in reports)

    print("── Grand Totals ──")
    row = {
        "Step": "ALL STEPS",
        "Runtime (s)": total_wall_time_s,
        "Compute (s)": total_compute_time_s,
        "Prompt Tokens": total_prompt_tokens,
        "Completion Tokens": total_completion_tokens,
        "Total Tokens": total_tokens,
        "Cost (USD)": format_cost(total_cost_usd),
        "Status": "OK" if all_succeeded else "PARTIAL",
    }
    widths = _col_widths([row])
    print(_render_row({column: column for column in COLUMNS}, widths))
    print(_render_divider(widths))
    print(_render_row(row, widths))
