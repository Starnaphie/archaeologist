# Requires LocalStack running with the deck.pptx already uploaded to the test bucket by the slides local_test.

import json
import os

from .handler import handler


def run_local(deck_key: str, execution_id: str = "local-test-001") -> None:
    os.environ["PIPELINE_BUCKET"] = "local-test-bucket"
    os.environ["S3_ENDPOINT_URL"] = "http://localhost:4566"
    os.environ["PRESIGNED_URL_EXPIRY_SECONDS"] = "3600"
    event = {
        "execution_id": execution_id,
        "deck_key": deck_key,
        "repo_source": "local",
        "topic": "local test",
    }
    result = handler(event, None)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import sys

    run_local(sys.argv[1])
