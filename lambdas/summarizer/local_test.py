# Requires LocalStack running locally with findings.json already written to the test bucket by the archaeologist local_test.

import os

from .handler import handler


def run_local(
    findings_key: str,
    topic: str,
    execution_id: str = "local-test-001",
) -> None:
    os.environ["PIPELINE_BUCKET"] = "local-test-bucket"
    os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
    event = {
        "execution_id": execution_id,
        "findings_key": findings_key,
        "repo_source": "local",
        "topic": topic,
        "description": "",
    }
    result = handler(event, None)
    print(result)


if __name__ == "__main__":
    import sys

    run_local(sys.argv[1], sys.argv[2])
