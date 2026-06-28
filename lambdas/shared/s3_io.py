"""S3 I/O helpers for the research-to-deck pipeline. All Lambdas import read_json, write_json, and upload_file from here. Set S3_ENDPOINT_URL to http://localhost:4566 to target LocalStack for local testing. Set PIPELINE_BUCKET to the CDK-provisioned bucket name."""

import os
import json
import logging
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

# Set PIPELINE_BUCKET in Lambda environment via CDK. All helpers default to this bucket if bucket argument is not provided.
BUCKET = os.environ.get("PIPELINE_BUCKET", "")


def _get_client():
    endpoint_url = os.environ.get("S3_ENDPOINT_URL", None)
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    config = Config(
        retries={
            "mode": "adaptive",
            "max_attempts": 5,
        }
    )
    return boto3.client(
        "s3",
        region_name=aws_region,
        endpoint_url=endpoint_url,
        config=config,
    )


def _resolve_bucket(bucket: str) -> str:
    resolved_bucket = bucket or BUCKET
    if not resolved_bucket:
        raise ValueError("No bucket specified and PIPELINE_BUCKET env var is not set")
    return resolved_bucket


def read_json(key: str, bucket: str = "") -> Any:
    bucket = _resolve_bucket(bucket)
    try:
        response = _get_client().get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)
    except ClientError as e:
        logger.error(f"Failed to read s3://{bucket}/{key}: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON at s3://{bucket}/{key}")
        raise json.JSONDecodeError(
            f"Invalid JSON at s3://{bucket}/{key}", e.doc, e.pos
        ) from e


def write_json(key: str, data: Any, bucket: str = "") -> None:
    bucket = _resolve_bucket(bucket)
    body = json.dumps(data, indent=2, ensure_ascii=False)
    try:
        _get_client().put_object(
            Bucket=bucket,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json",
        )
        logger.info(f"Wrote {len(body)} bytes to s3://{bucket}/{key}")
    except ClientError as e:
        logger.error(f"Failed to write s3://{bucket}/{key}: {e}")
        raise


def upload_file(
    local_path: str,
    key: str,
    bucket: str = "",
    content_type: str = "application/octet-stream",
) -> None:
    bucket = _resolve_bucket(bucket)
    try:
        _get_client().upload_file(
            Filename=local_path,
            Bucket=bucket,
            Key=key,
            ExtraArgs={"ContentType": content_type},
        )
        logger.info(f"Uploaded {local_path} to s3://{bucket}/{key}")
    except ClientError as e:
        logger.error(f"Failed to upload {local_path} to s3://{bucket}/{key}: {e}")
        raise


def download_file(key: str, local_path: str, bucket: str = "") -> None:
    bucket = _resolve_bucket(bucket)
    try:
        _get_client().download_file(Bucket=bucket, Key=key, Filename=local_path)
        logger.info(f"Downloaded s3://{bucket}/{key} to {local_path}")
    except ClientError as e:
        logger.error(f"Failed to download s3://{bucket}/{key} to {local_path}: {e}")
        raise


def build_key(execution_id: str, filename: str) -> str:
    """Build an execution-scoped artifact key.

    execution_id should be the Step Functions execution ID passed through the
    event, which namespaces all artifacts from one pipeline run under a single
    prefix.

    Examples:
        build_key("abc123", "findings.json") -> "executions/abc123/findings.json"
        build_key("abc123", "outline.json")  -> "executions/abc123/outline.json"
        build_key("abc123", "deck.pptx")     -> "executions/abc123/deck.pptx"
    """
    return f"executions/{execution_id}/{filename}"


def generate_presigned_url(
    key: str,
    bucket: str = "",
    expiry_seconds: int = 3600,
) -> str:
    bucket = _resolve_bucket(bucket)
    try:
        url = _get_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiry_seconds,
        )
        logger.info(
            f"Generated presigned URL for s3://{bucket}/{key} "
            f"expiring in {expiry_seconds}s"
        )
        return url
    except ClientError as e:
        logger.error(f"Failed to generate presigned URL for s3://{bucket}/{key}: {e}")
        raise
