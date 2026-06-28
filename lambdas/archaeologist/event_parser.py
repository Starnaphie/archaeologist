"""Event parsing for the archaeologist Lambda. Validates the Step Functions input event and extracts typed fields. Call parse_event at the top of handler() before any other logic."""

from dataclasses import dataclass
@dataclass
class ArchaeologistEvent:
    execution_id: str  # Step Functions execution ID — used as S3 key prefix
    repo_source: str  # GitHub URL or local path to analyze
    topic: str  # User-submitted topic — passed through to summarizer for context
    description: str = ""  # Optional additional context about the topic
    audience: str = ""
    tone: str = "professional"
    num_slides: int | None = None


def parse_event(event: dict) -> ArchaeologistEvent:
    execution_id = event.get("execution_id")
    if not isinstance(execution_id, str) or not execution_id:
        raise ValueError("event missing required field: execution_id")

    repo_source = event.get("repo_source")
    if not isinstance(repo_source, str) or not repo_source:
        raise ValueError("event missing required field: repo_source")

    topic = event.get("topic")
    if not isinstance(topic, str) or not topic:
        raise ValueError("event missing required field: topic")

    description = event.get("description", "")
    audience = event.get("audience", "")
    tone = event.get("tone", "professional")
    num_slides = event.get("num_slides", None)
    return ArchaeologistEvent(
        execution_id=execution_id,
        repo_source=repo_source,
        topic=topic,
        description=description,
        audience=audience,
        tone=tone,
        num_slides=num_slides,
    )


def build_output(
    execution_id: str,
    findings_key: str,
    repo_source: str,
    topic: str,
    description: str,
    audience: str = "",
    tone: str = "professional",
    num_slides: int | None = None,
) -> dict:
    """Builds the Step Functions output payload. All fields are passed through to the summarizer Lambda via the state machine."""
    return {
        "execution_id": execution_id,
        "findings_key": findings_key,
        "repo_source": repo_source,
        "topic": topic,
        "description": description,
        "audience": audience,
        "tone": tone,
        "num_slides": num_slides,
    }
