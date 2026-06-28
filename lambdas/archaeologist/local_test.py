# Requires LocalStack running locally. Start with: docker run -p 4566:4566 localstack/localstack

import os

from .handler import handler


def run_local(repo_path: str, topic: str) -> None:
    event = {
        "execution_id": "local-test-001",
        "repo_source": repo_path,
        "topic": topic,
        "description": "",
    }
    os.environ["PIPELINE_BUCKET"] = "local-test-bucket"
    os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
    result = handler(event, None)
    print(result)


if __name__ == "__main__":
    import sys

    run_local(sys.argv[1], sys.argv[2])
