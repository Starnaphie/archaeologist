"""Lambda handler for the slides generator. Reads outline.json from S3, builds a .pptx using python-pptx, uploads deck.pptx to S3, returns the S3 deck key for the URL generator Lambda."""

import json
import logging
import os
import shutil
import tempfile

from lambdas.shared.s3_io import read_json, upload_file, build_key
from lambdas.shared.validation import load_and_validate_outline

from .event_parser import parse_event, build_output
from .slides_builder import build_presentation


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handler(event: dict, context) -> dict:
    tmp_dir = ""
    try:
        parsed = parse_event(event)
        logger.info(
            f"Slides Lambda started: execution_id={parsed.execution_id}, "
            f"outline_key={parsed.outline_key}"
        )

        outline = read_json(parsed.outline_key)
        try:
            load_and_validate_outline(json.dumps(outline))
        except ValueError:
            logger.error("Outline failed validation", exc_info=True)
            raise

        logger.info(
            f"Outline validated: '{outline.get('title')}' "
            f"with {len(outline.get('slides', []))} slides"
        )

        tmp_dir = tempfile.mkdtemp()
        os.environ["SLIDES_OUTPUT_DIR"] = tmp_dir
        result = build_presentation(outline, repo_source=parsed.repo_source)
        logger.info(f"Built presentation: {result.file_path}")

        deck_key = build_key(parsed.execution_id, "deck.pptx")
        upload_file(
            result.file_path,
            deck_key,
            content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

        meta_path = result.file_path.replace(".pptx", ".meta.json")
        if os.path.exists(meta_path):
            upload_file(
                meta_path,
                build_key(parsed.execution_id, "deck.meta.json"),
                content_type="application/json",
            )

        logger.info(f"Uploaded deck to {deck_key}")
        return build_output(parsed.execution_id, deck_key, parsed.repo_source, parsed.topic)
    except Exception as e:
        logger.error(f"Slides Lambda failed: {e}", exc_info=True)
        raise
    finally:
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)
