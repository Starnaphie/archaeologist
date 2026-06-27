"""Event parsing for the summarizer Lambda. Validates the Step Functions input from the archaeologist and extracts typed fields."""

from dataclasses import dataclass


@dataclass
class SummarizerEvent:
    execution_id: str  # Step Functions execution ID — S3 key prefix
    findings_key: str  # S3 key for findings.json written by archaeologist
    repo_source: str  # Original repo URL or local path — passed through to slides Lambda
    topic: str  # User-submitted topic
    description: str = ""  # Optional additional context


def parse_event(event: dict) -> SummarizerEvent:
    execution_id = event.get("execution_id")
    if not isinstance(execution_id, str) or not execution_id:
        raise ValueError("event missing required field: execution_id")

    findings_key = event.get("findings_key")
    if not isinstance(findings_key, str) or not findings_key:
        raise ValueError("event missing required field: findings_key")

    topic = event.get("topic")
    if not isinstance(topic, str) or not topic:
        raise ValueError("event missing required field: topic")

    repo_source = event.get("repo_source", "")
    description = event.get("description", "")
    return SummarizerEvent(
        execution_id=execution_id,
        findings_key=findings_key,
        repo_source=repo_source,
        topic=topic,
        description=description,
    )


def build_output(
    execution_id: str,
    outline_key: str,
    repo_source: str,
    topic: str,
) -> dict:
    """Builds Step Functions output for the slides Lambda. outline_key is the S3 key for the generated outline.json."""
    return {
        "execution_id": execution_id,
        "outline_key": outline_key,
        "repo_source": repo_source,
        "topic": topic,
    }
