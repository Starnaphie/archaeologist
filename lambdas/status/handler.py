"""Lambda handler for GET /status. Polls Step Functions DescribeExecution and returns the current status. When SUCCEEDED, includes the presigned download URL from the state machine output."""

import json
import logging
import os

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _get_sfn_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    endpoint_url = os.environ.get("SFN_ENDPOINT_URL", None)
    return boto3.client(
        "stepfunctions",
        region_name=aws_region,
        endpoint_url=endpoint_url,
        config=Config(retries={"mode": "adaptive", "max_attempts": 3}),
    )


def _response(status_code: int, headers: dict, payload: dict | str) -> dict:
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": payload if isinstance(payload, str) else json.dumps(payload),
    }


def handler(event: dict, context) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    execution_arn = (event.get("queryStringParameters") or {}).get("arn", "")
    if not execution_arn:
        return _response(400, headers, {"error": "Missing required query parameter: arn"})

    logger.info(f"Status check for: {execution_arn}")

    try:
        response = _get_sfn_client().describe_execution(executionArn=execution_arn)
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "ExecutionDoesNotExist":
            return _response(
                404,
                headers,
                {"error": "Execution not found", "arn": execution_arn},
            )
        logger.error("Failed to describe execution", exc_info=True)
        return _response(500, headers, {"error": "Failed to describe execution"})
    except Exception:
        logger.error("Failed to describe execution", exc_info=True)
        return _response(500, headers, {"error": "Failed to describe execution"})

    status = response["status"]
    start_date = response.get("startDate", "")
    payload = {
        "arn": execution_arn,
        "status": status,
        "started_at": (
            start_date.isoformat() if hasattr(start_date, "isoformat") else str(start_date)
        ),
    }

    if status == "SUCCEEDED":
        output = json.loads(response.get("output", "{}"))
        payload.update(
            {
                "download_url": output.get("download_url", ""),
                "topic": output.get("topic", ""),
                "deck_key": output.get("deck_key", ""),
                "expires_in_seconds": output.get("expires_in_seconds", 3600),
            }
        )
    elif status in ("FAILED", "TIMED_OUT", "ABORTED"):
        payload["error"] = response.get("cause", "Unknown error")

    return _response(200, headers, payload)
