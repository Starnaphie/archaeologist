import argparse
import sys
from .eval_archaeologist import run_archaeologist_eval
from .eval_pipeline import run_pipeline_eval
from .tool_call_evals import run_tool_call_evals
from .token_utils import merge_reports
from .reporter import print_report, print_combined_report, print_tool_call_summary
from .cost_config import format_cost
from .metrics import EvalReport


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Eval suite for archaeologist and slides pipeline."
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["archaeologist", "pipeline", "both", "tool-calls"],
        help="Which agent to evaluate. 'tool-calls' runs the tool selection eval suite.",
    )
    parser.add_argument("--repo-root", type=str, default=None, help="Path to local repo to analyze")
    parser.add_argument("--topic", type=str, default=None, help="Presentation topic")
    parser.add_argument("--audience", type=str, default=None, help="Target audience description")
    parser.add_argument("--tone", type=str, default="professional", choices=["professional", "casual", "academic"])
    parser.add_argument("--description", type=str, default="")
    parser.add_argument("--num-slides", type=int, default=None, help="Maximum slide count (default: auto up to 20)")
    return parser


def _validate_args(args: argparse.Namespace) -> list[str]:
    errors = []
    if args.mode in ("archaeologist", "both") and not args.repo_root:
        errors.append(f"--repo-root is required for mode '{args.mode}'")
    if args.mode in ("pipeline", "both") and not args.topic:
        errors.append(f"--topic is required for mode '{args.mode}'")
    if args.mode in ("pipeline", "both") and not args.audience:
        errors.append(f"--audience is required for mode '{args.mode}'")
    return errors


def _print_setup_comparison(arch_report: EvalReport) -> None:
    pass1 = next((s for s in arch_report.steps if "Pass 1" in s.step_name), None)
    pass2 = next((s for s in arch_report.steps if "Pass 2" in s.step_name), None)
    if pass1 and pass2:
        print("\n── Setup Extraction Comparison ──")
        print(f"  Pass 1 (baseline):          {pass1.wall_time_s}s  {pass1.total_tokens} tokens  {format_cost(pass1.cost_usd)}")
        print(f"  Pass 2 (with README):        {pass2.wall_time_s}s  {pass2.total_tokens} tokens  {format_cost(pass2.cost_usd)}")
        overhead_tokens = pass2.total_tokens - pass1.total_tokens
        overhead_cost = pass2.cost_usd - pass1.cost_usd
        print(f"  README validation overhead:  +{overhead_tokens} tokens  +{format_cost(overhead_cost)}")


def run(args: argparse.Namespace) -> None:
    if args.mode == "archaeologist":
        print(f"Running archaeologist eval on: {args.repo_root}")
        arch_report = run_archaeologist_eval(args.repo_root)
        print_report(arch_report)
        _print_setup_comparison(arch_report)

    elif args.mode == "pipeline":
        print(f"Running pipeline eval: topic='{args.topic}', audience='{args.audience}', tone='{args.tone}'")
        pipeline_report, outline = run_pipeline_eval(
            topic=args.topic,
            audience=args.audience,
            tone=args.tone,
            description=args.description,
            num_slides=args.num_slides,
        )
        print(f"  Generated outline: '{outline.get('title', 'untitled')}' with {len(outline.get('slides', []))} slides")
        print_report(pipeline_report)

    elif args.mode == "both":
        print("Running combined eval — archaeologist then pipeline")
        arch_report = run_archaeologist_eval(args.repo_root)
        pipeline_report, outline = run_pipeline_eval(
            topic=args.topic,
            audience=args.audience,
            tone=args.tone,
            description=args.description,
            num_slides=args.num_slides,
        )
        print(f"  Generated outline: '{outline.get('title', 'untitled')}' with {len(outline.get('slides', []))} slides")
        print_combined_report([arch_report, pipeline_report])
        _print_setup_comparison(arch_report)

    elif args.mode == "tool-calls":
        print("Running tool call evals (18 test cases)…")
        report = EvalReport(label="Tool Call Evals")
        result = run_tool_call_evals(report)
        print_report(report)
        print_tool_call_summary(result)


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()
    errors = _validate_args(args)
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        parser.print_usage(sys.stderr)
        sys.exit(1)
    run(args)
