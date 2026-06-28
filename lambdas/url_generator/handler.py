"""Lambda handler for the URL generator. Final step in the Step Functions chain. Receives the S3 deck key, generates a presigned download URL, returns it as the state machine output. The frontend receives this via the GET /status polling endpoint."""

import json
import logging
import os

from lambdas.shared.s3_io import generate_presigned_url


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _parse_event(event: dict) -> dict:
    deck_key = event.get("deck_key")
    if not isinstance(deck_key, str) or not deck_key:
        raise ValueError("event missing required field: deck_key")

    execution_id = event.get("execution_id", "unknown")
    repo_source = event.get("repo_source", "")
    topic = event.get("topic", "")
    return {
        "deck_key": deck_key,
        "execution_id": execution_id,
        "repo_source": repo_source,
        "topic": topic,
    }


def handler(event: dict, context) -> dict:
    try:
        parsed = _parse_event(event)
        logger.info(
            f"Generating URL for: execution_id={parsed['execution_id']}, "
            f"key={parsed['deck_key']}"
        )

        expiry = int(os.environ.get("PRESIGNED_URL_EXPIRY_SECONDS", "3600"))
        url = generate_presigned_url(parsed["deck_key"], expiry_seconds=expiry)
        logger.info(f"Generated presigned URL expiring in {expiry}s")

        return {
            "execution_id": parsed["execution_id"],
            "download_url": url,
            "deck_key": parsed["deck_key"],
            "repo_source": parsed["repo_source"],
            "topic": parsed["topic"],
            "expires_in_seconds": expiry,
            "status": "COMPLETE",
        }
    except Exception as e:
        logger.error(f"URL generator failed: {e}", exc_info=True)
        raise
