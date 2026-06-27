"""Runtime validation for S3 data contracts. Call load_and_validate_* at the top of each Lambda handler before processing."""

import json
import typing

from lambdas.shared.schemas import FindingsSchema, OutlineSchema


def _check_required_types(
    data: dict, required_types: dict[str, type], label: str | None = None
) -> list[str]:
    violations: list[str] = []
    prefix = f"{label}." if label else ""

    for key, expected_type in required_types.items():
        if key not in data:
            violations.append(f"missing key: {prefix}{key}")
        elif not isinstance(data[key], expected_type):
            violations.append(
                f"wrong type for key: {prefix}{key} expected {expected_type.__name__}"
            )

    return violations


def validate_findings(data: dict) -> tuple[bool, list[str]]:
    required_types = {
        "purpose": str,
        "one_liner": str,
        "modules": list,
        "incomplete_features": list,
        "dependency_graph": str,
        "repo_owner": dict,
        "was_chunked": bool,
    }
    violations = _check_required_types(data, required_types)
    return len(violations) == 0, violations


def validate_outline(data: dict) -> tuple[bool, list[str]]:
    violations = _check_required_types(
        data,
        {
            "title": str,
            "slides": list,
        },
    )

    slides = data.get("slides")
    if isinstance(slides, list):
        if not slides:
            violations.append("slides must be non-empty")

        for index, slide in enumerate(slides):
            label = f"slides[{index}]"
            if not isinstance(slide, dict):
                violations.append(f"wrong type for key: {label} expected dict")
                continue

            violations.extend(
                _check_required_types(
                    slide,
                    {
                        "layout": str,
                        "title": str,
                        "content": dict,
                        "speaker_notes": list,
                    },
                    label=label,
                )
            )

    return len(violations) == 0, violations


def load_and_validate_findings(raw: str) -> FindingsSchema:
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Invalid findings.json: ['wrong type for root expected dict']")

    is_valid, violations = validate_findings(parsed)
    if not is_valid:
        raise ValueError(f"Invalid findings.json: {violations}")

    return typing.cast(FindingsSchema, parsed)


def load_and_validate_outline(raw: str) -> OutlineSchema:
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Invalid outline.json: ['wrong type for root expected dict']")

    is_valid, violations = validate_outline(parsed)
    if not is_valid:
        raise ValueError(f"Invalid outline.json: {violations}")

    return typing.cast(OutlineSchema, parsed)
