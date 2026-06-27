"""Lambda handler for the summarizer. Reads archaeologist findings from S3, runs the 4-pass outline generation pipeline, writes outline.json to S3, returns the S3 key for the slides Lambda."""

import logging

from .event_parser import parse_event, build_output
from .summarizer import run_summarizer


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handler(event: dict, context) -> dict:
    try:
        parsed = parse_event(event)
        logger.info(
            f"Summarizer started: execution_id={parsed.execution_id}, "
            f"topic='{parsed.topic}'"
        )

        outline_key = run_summarizer(
            parsed.execution_id,
            parsed.findings_key,
            parsed.topic,
            parsed.description,
            parsed.repo_source,
            parsed.audience,
            parsed.tone,
            parsed.num_slides,
        )

        return build_output(
            parsed.execution_id,
            outline_key,
            parsed.repo_source,
            parsed.topic,
            parsed.audience,
            parsed.tone,
            parsed.num_slides,
        )
    except Exception as e:
        logger.error(f"Summarizer failed: {e}", exc_info=True)
        raise
