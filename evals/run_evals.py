"""CLI entrypoint for the eval suite. Run with --mode archaeologist, pipeline, or both. See --help for required arguments per mode."""

import argparse
import sys

from .eval_archaeologist import run_archaeologist_eval
from .eval_pipeline import run_pipeline_eval
from .token_utils import merge_reports
from .reporter import print_report, print_combined_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        required=True,
        choices=["archaeologist", "pipeline", "both"],
        help="Which agent to evaluate",
    )
    parser.add_argument(
        "--repo-root",
        type=str,
        help="Path to local repo to analyze",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Presentation topic",
    )
    parser.add_argument(
        "--audience",
        type=str,
        help="Target audience description",
    )
    parser.add_argument(
        "--tone",
        type=str,
        default="professional",
        choices=["professional", "casual", "academic"],
    )
    parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Optional additional topic description",
    )
    parser.add_argument(
        "--num-slides",
        type=int,
        default=None,
        help="Maximum slide count (default: auto up to 20)",
    )
    return parser


def _validate_args(args: argparse.Namespace) -> list[str]:
    errors = []
    if args.mode in {"archaeologist", "both"} and not args.repo_root:
        errors.append(f"--repo-root is required for mode '{args.mode}'")
    if args.mode in {"pipeline", "both"} and not args.topic:
        errors.append(f"--topic is required for mode '{args.mode}'")
    if args.mode in {"pipeline", "both"} and not args.audience:
        errors.append(f"--audience is required for mode '{args.mode}'")
    return errors


def run(args: argparse.Namespace) -> None:
    if args.mode == "archaeologist":
        print(f"Running archaeologist eval on: {args.repo_root}")
        report = run_archaeologist_eval(args.repo_root)
        print_report(report)

    if args.mode == "pipeline":
        print(
            f"Running pipeline eval: topic='{args.topic}', "
            f"audience='{args.audience}', tone='{args.tone}'"
        )
        report, outline = run_pipeline_eval(
            topic=args.topic,
            audience=args.audience,
            tone=args.tone,
            description=args.description,
            num_slides=args.num_slides,
        )
        print(
            f"  Generated outline: '{outline.get('title', 'untitled')}' "
            f"with {len(outline.get('slides', []))} slides"
        )
        print_report(report)

    if args.mode == "both":
        print("Running combined eval — archaeologist then pipeline")
        arch_report = run_archaeologist_eval(args.repo_root)
        pipeline_report, outline = run_pipeline_eval(
            topic=args.topic,
            audience=args.audience,
            tone=args.tone,
            description=args.description,
            num_slides=args.num_slides,
        )
        print(
            f"  Generated outline: '{outline.get('title', 'untitled')}' "
            f"with {len(outline.get('slides', []))} slides"
        )
        print_combined_report([arch_report, pipeline_report])


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
