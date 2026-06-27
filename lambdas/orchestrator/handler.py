"""Lambda handler for the orchestrator. Receives API Gateway POST /generate, validates topic and repo_source, starts a Step Functions execution, returns the execution ARN for polling."""

import json
import logging
import os
import uuid

import boto3
from botocore.config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _get_sfn_client():
    state_machine_arn = os.environ.get("STATE_MACHINE_ARN", "")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    endpoint_url = os.environ.get("SFN_ENDPOINT_URL", None)
    return boto3.client(
        "stepfunctions",
        region_name=aws_region,
        endpoint_url=endpoint_url,
        config=Config(retries={"mode": "adaptive", "max_attempts": 3}),
    )


def _parse_body(event: dict) -> dict:
    raw_body = event.get("body", "{}")
    if raw_body is None:
        body = {}
    elif isinstance(raw_body, str):
        body = json.loads(raw_body)
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        body = {}

    topic = body.get("topic", "")
    if not topic:
        raise ValueError("Request body missing required field: topic")

    repo_source = body.get("repo_source", "")
    if not repo_source:
        raise ValueError("Request body missing required field: repo_source")

    return {
        "topic": topic,
        "repo_source": repo_source,
        "description": body.get("description", ""),
    }


def _response(status_code: int, payload: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(payload),
    }


def handler(event: dict, context) -> dict:
    try:
        body = _parse_body(event)
        execution_id = str(uuid.uuid4())[:8]
        logger.info(
            f"Starting execution: id={execution_id}, "
            f"topic='{body['topic']}', repo={body['repo_source']}"
        )

        state_machine_arn = os.environ.get("STATE_MACHINE_ARN", "")
        if not state_machine_arn:
            raise ValueError("STATE_MACHINE_ARN environment variable not set")

        sfn_input = json.dumps(
            {
                "execution_id": execution_id,
                "topic": body["topic"],
                "repo_source": body["repo_source"],
                "description": body["description"],
            }
        )
        response = _get_sfn_client().start_execution(
            stateMachineArn=state_machine_arn,
            name=f"exec-{execution_id}",
            input=sfn_input,
        )
        execution_arn = response["executionArn"]
        logger.info(f"Started execution: arn={execution_arn}")

        return _response(
            202,
            {
                "execution_id": execution_id,
                "execution_arn": execution_arn,
                "status": "STARTED",
            },
        )
    except ValueError as e:
        return _response(400, {"error": str(e)})
    except Exception:
        logger.error("Orchestrator failed", exc_info=True)
        return _response(500, {"error": "Internal server error"})
