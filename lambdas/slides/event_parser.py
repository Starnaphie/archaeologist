"""Event parsing for the slides Lambda. Validates the Step Functions input from the summarizer and extracts typed fields."""

from dataclasses import dataclass


@dataclass
class SlidesEvent:
    execution_id: str  # Step Functions execution ID — S3 key prefix
    outline_key: str  # S3 key for outline.json written by summarizer
    repo_source: str  # Original repo URL or local path — embedded in .meta.json sidecar
    topic: str  # User-submitted topic — used for fallback title if needed


def parse_event(event: dict) -> SlidesEvent:
    execution_id = event.get("execution_id")
    if not isinstance(execution_id, str) or not execution_id:
        raise ValueError("event missing required field: execution_id")

    outline_key = event.get("outline_key")
    if not isinstance(outline_key, str) or not outline_key:
        raise ValueError("event missing required field: outline_key")

    repo_source = event.get("repo_source", "")
    topic = event.get("topic", "")
    return SlidesEvent(
        execution_id=execution_id,
        outline_key=outline_key,
        repo_source=repo_source,
        topic=topic,
    )


def build_output(execution_id: str, deck_key: str, repo_source: str, topic: str) -> dict:
    """Builds Step Functions output for the URL generator. deck_key is the S3 key for the uploaded .pptx file."""
    return {
        "execution_id": execution_id,
        "deck_key": deck_key,
        "repo_source": repo_source,
        "topic": topic,
    }
