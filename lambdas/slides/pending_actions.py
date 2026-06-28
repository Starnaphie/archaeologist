"""Pending actions store for confirmations.

Tracks actions that require user confirmation before execution,
keyed by action_id.
"""

import uuid
from typing import Any

# In-memory store: action_id → action dict
_actions: dict[str, dict[str, Any]] = {}


def create_pending_action(
    presentation_id: str,
    action_type: str,
    params: dict,
) -> str:
    """Create a pending action that requires user confirmation.

    Args:
        presentation_id: Optional presentation identifier
        action_type: Type of action requiring confirmation
        params: Parameters for the action

    Returns:
        action_id that can be used to confirm or decline the action
    """
    action_id = str(uuid.uuid4())
    _actions[action_id] = {
        "action_id": action_id,
        "presentation_id": presentation_id,
        "action_type": action_type,
        "params": params,
    }
    return action_id


def get_pending_action(action_id: str) -> dict | None:
    """Retrieve a pending action by ID."""
    return _actions.get(action_id)


def delete_pending_action(action_id: str) -> None:
    """Remove a pending action (after execution or decline)."""
    _actions.pop(action_id, None)
