# Requires LocalStack running with a state machine already deployed. Start LocalStack: docker run -p 4566:4566 localstack/localstack. Deploy state machine first via: cdklocal deploy.

import json
import os

from .handler import handler


def run_local(topic: str, repo_source: str) -> None:
    os.environ["STATE_MACHINE_ARN"] = (
        "arn:aws:states:us-east-1:000000000000:stateMachine:ResearchToDeckPipeline"
    )
    os.environ["SFN_ENDPOINT_URL"] = "http://localhost:4566"
    os.environ["AWS_REGION"] = "us-east-1"
    event = {
        "body": json.dumps(
            {
                "topic": topic,
                "repo_source": repo_source,
                "description": "",
            }
        )
    }
    result = handler(event, None)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import sys

    run_local(sys.argv[1], sys.argv[2])
