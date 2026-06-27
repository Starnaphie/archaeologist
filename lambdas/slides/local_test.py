# Run with --fixture to generate a .pptx from the shared fixture outline without any AWS or OpenAI calls. Useful for verifying layout builders work correctly.

import json
import os
from pathlib import Path

from .slides_builder import build_presentation


def run_local(
    outline_key: str = "",
    execution_id: str = "local-test-001",
    use_fixture: bool = False,
) -> None:
    if use_fixture or not outline_key:
        fixture_path = (
            Path(__file__).resolve().parents[1]
            / "shared"
            / "fixtures"
            / "outline_example.json"
        )
        with open(fixture_path, "r", encoding="utf-8") as fixture_file:
            outline = json.load(fixture_file)

        result = build_presentation(outline, repo_source="local-fixture")
        print(f"Generated: {result.file_path}")
        print(f"Title: {result.title}")
        return

    os.environ["PIPELINE_BUCKET"] = "local-test-bucket"
    os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
    event = {
        "execution_id": execution_id,
        "outline_key": outline_key,
        "repo_source": "local",
        "topic": "local test",
    }
    from .handler import handler

    result = handler(event, None)
    print(result)


if __name__ == "__main__":
    import sys

    if "--fixture" in sys.argv:
        run_local(use_fixture=True)
    elif len(sys.argv) >= 2:
        run_local(outline_key=sys.argv[1])
    else:
        print("Usage: python -m lambdas.slides.local_test --fixture")
        print("       python -m lambdas.slides.local_test executions/local-test-001/outline.json")
