"""In-memory session store for the Slides Agent.

Each session is keyed by a UUID session_id and tracks conversation history,
the current JSON outline, an optional presentation_id, and a mapping
from slide index to shape object IDs.

History entry shapes:
    {"role": "user",      "content": str}
    {"role": "assistant", "content": str, "snapshot": dict}

The ``snapshot`` on an assistant entry is the outline as it existed
immediately BEFORE the assistant's action was applied. It acts as the
undo target for that turn. The store itself does not enforce a max
length — callers (e.g. the /revise endpoint) trim history to bound the
undo stack.
"""

from __future__ import annotations

import uuid
from typing import Any


# slide index → {"title_shape_id": str, "body_shape_id": str}
ObjectIdMap = dict[int, dict[str, str]]

_store: dict[str, dict[str, Any]] = {}


def _blank_session(session_id: str) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "history": [],            # list of {"role": str, "content": str, "snapshot"?: dict}
        "outline": None,          # current JSON outline dict
        "presentation_id": None,  # optional generated presentation ID
        "object_id_map": {},      # {slide_index: {"title_shape_id": ..., "body_shape_id": ...}}
    }


def create_session() -> dict[str, Any]:
    """Create a new session with a fresh UUID and return it."""
    session_id = str(uuid.uuid4())
    session = _blank_session(session_id)
    _store[session_id] = session
    return session


def get_session(session_id: str) -> dict[str, Any] | None:
    """Return the session for *session_id*, or ``None`` if it doesn't exist."""
    return _store.get(session_id)


def update_session(session_id: str, **fields: Any) -> dict[str, Any]:
    """Merge *fields* into an existing session and return the updated session.

    Raises ``KeyError`` if the session does not exist.
    """
    session = _store.get(session_id)
    if session is None:
        raise KeyError(f"Session {session_id!r} not found")
    session.update(fields)
    return session


def delete_session(session_id: str) -> None:
    """Delete a session by ID.

    Raises ``KeyError`` if the session does not exist.
    """
    if session_id not in _store:
        raise KeyError(f"Session {session_id!r} not found")
    del _store[session_id]
