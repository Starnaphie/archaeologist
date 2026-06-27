"""Core summarizer logic. Reads findings.json from S3, enriches it with repo context, calls the 4-pass generate_outline pipeline, validates the result against OutlineSchema, and writes outline.json to S3."""

import logging
import json

from lambdas.shared.s3_io import read_json, write_json, build_key
from lambdas.shared.validation import load_and_validate_outline
from lambdas.slides.openai_agent import generate_outline

from .context_builder import build_description


logger = logging.getLogger(__name__)


def run_summarizer(
    execution_id: str,
    findings_key: str,
    topic: str,
    description: str,
    repo_source: str,
    audience: str,
    tone: str,
    num_slides: int | None,
) -> str:
    findings_raw = read_json(findings_key)
    logger.info(
        f"Read findings from {findings_key}: "
        f"purpose length={len(findings_raw.get('purpose', ''))}"
    )

    enriched_description = build_description(findings_raw, topic)
    if description:
        enriched_description = description + "\n\n" + enriched_description

    logger.info(
        f"Built context: audience='{audience}', "
        f"description length={len(enriched_description)}"
    )

    outline = generate_outline(
        topic=topic,
        audience=audience,
        num_slides=num_slides,
        tone=tone,
        description=enriched_description,
    )
    logger.info(
        f"Generated outline: '{outline.get('title')}' "
        f"with {len(outline.get('slides', []))} slides"
    )

    outline_json_str = json.dumps(outline)
    try:
        load_and_validate_outline(outline_json_str)
    except ValueError:
        logger.error("Generated outline failed validation", exc_info=True)
        raise

    outline_key = build_key(execution_id, "outline.json")
    write_json(outline_key, outline)
    logger.info(f"Wrote outline to {outline_key}")
    return outline_key
