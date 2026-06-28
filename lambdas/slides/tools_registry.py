"""Agent tools registry for Slides Agent.

Defines all available tools the agent can call, in OpenAI function-calling format.
"""

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "update_slides",
            "description": "Update content on existing slides. Modify titles, bullets, or speaker notes for one or more slides.",
            "parameters": {
                "type": "object",
                "properties": {
                    "changes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "slide_index": {
                                    "type": "integer",
                                    "description": "The index of the slide to update (0-based)",
                                },
                                "new_title": {
                                    "type": "string",
                                    "description": "Optional new title for the slide",
                                },
                                "new_bullets": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Optional new bullet points for the slide",
                                },
                                "new_speaker_notes": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Optional new speaker notes (list of bullet points)",
                                },
                            },
                            "required": ["slide_index"],
                        },
                        "description": "List of slide updates, each with slide_index and optional new_title, new_bullets, new_speaker_notes",
                    }
                },
                "required": ["changes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_slides",
            "description": "Append new slides to the presentation when the user asks for specific NEW content by topic. Do not use this when the user specifies a target total count; use set_slide_count instead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "slides": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Slide title (required)",
                                },
                                "bullets": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Optional bullet points",
                                },
                                "speaker_notes": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Optional speaker notes (list of bullet points)",
                                },
                            },
                            "required": ["title"],
                        },
                        "description": "List of new slides to append, each with title and optional bullets and speaker_notes",
                    }
                },
                "required": ["slides"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_slides",
            "description": "Remove specific named or numbered slides. Do not use this when the user gives a target count; use set_slide_count instead. Never pass an empty slide_indices array.",
            "parameters": {
                "type": "object",
                "properties": {
                    "slide_indices": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of slide indices to delete (0-based, e.g. [1, 3] deletes slides 1 and 3)",
                    }
                },
                "required": ["slide_indices"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_slide_count",
            "description": "Preferred tool for any instruction that mentions a desired total number of slides. Pass target_count as the integer target.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_count": {
                        "type": "integer",
                        "description": "The desired total number of slides (not counting the title slide)",
                    }
                },
                "required": ["target_count"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "respond",
            "description": "Use when the user's request cannot be fulfilled by any available tool. Explain what is not supported and suggest what is possible.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Plain English explanation to show the user.",
                    }
                },
                "required": ["message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reorder_slides",
            "description": "Reorder slides in the presentation by specifying their new order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_order": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of slide indices in desired order (0-based, e.g. [2, 0, 1] moves slide 2 to front)",
                    }
                },
                "required": ["new_order"],
            },
        },
    },
]

DESTRUCTIVE_TOOLS = set()
