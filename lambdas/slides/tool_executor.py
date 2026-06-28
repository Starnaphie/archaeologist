"""Tool execution engine for slides agent.

Handles executing tool calls from the AI model against the current outline.
"""

from dataclasses import dataclass, field

from .openai_agent import generate_outline


@dataclass
class ExecutionResult:
    """Result of executing a tool call."""

    status: str  # "executed" | "declined" | "responded"
    change_summary: str
    action_id: str | None
    updated_outline: dict | None
    presentation_id: str | None = field(default=None)
    url: str | None = field(default=None)


def execute_tool(tool_call_result, session: dict) -> ExecutionResult:
    """Execute a tool call and update the in-memory outline."""
    tool_name = tool_call_result.tool_name
    tool_args = tool_call_result.tool_args
    current_outline = session.get("outline", {})

    try:
        if tool_name == "respond":
            return ExecutionResult(
                status="responded",
                change_summary=tool_args.get("message", ""),
                action_id=None,
                updated_outline=current_outline,
            )

        if tool_name == "update_slides":
            changes = tool_args.get("changes", [])
            new_outline = _apply_update_slides(current_outline, changes)
            return ExecutionResult(
                status="executed",
                change_summary=f"Updated {len(changes)} slide(s).",
                action_id=None,
                updated_outline=new_outline,
            )

        if tool_name == "add_slides":
            slides = tool_args.get("slides", [])
            new_outline = _apply_add_slides(current_outline, slides)
            return ExecutionResult(
                status="executed",
                change_summary=f"Added {len(slides)} new slide(s).",
                action_id=None,
                updated_outline=new_outline,
            )

        if tool_name == "delete_slides":
            slide_indices = tool_args.get("slide_indices", [])
            new_outline = _apply_delete_slides(current_outline, slide_indices)
            return ExecutionResult(
                status="executed",
                change_summary=f"Deleted {len(slide_indices)} slide(s).",
                action_id=None,
                updated_outline=new_outline,
            )

        if tool_name == "set_slide_count":
            target_count = tool_args.get("target_count", 0)
            current_slides = current_outline.get("slides", [])
            current_count = len(current_slides)

            if target_count == current_count:
                return ExecutionResult(
                    status="executed",
                    change_summary=f"Already at {current_count} slides; no changes needed.",
                    action_id=None,
                    updated_outline=current_outline,
                )

            if target_count < current_count:
                indices_to_delete = list(range(target_count, current_count))
                new_outline = _apply_delete_slides(current_outline, indices_to_delete)
                removed = current_count - target_count
                return ExecutionResult(
                    status="executed",
                    change_summary=f"Removed {removed} slide(s) from the end. Now at {target_count} slides.",
                    action_id=None,
                    updated_outline=new_outline,
                )

            needed = target_count - current_count
            generated_outline = generate_outline(
                topic=current_outline.get("title", "Untitled presentation"),
                audience=tool_args.get("audience", ""),
                num_slides=needed,
                tone=tool_args.get("tone", "professional"),
                description="Generate additional slides that continue the existing deck.",
            )
            new_slides = generated_outline.get("slides", [])[:needed]
            new_outline = _apply_add_slides(current_outline, new_slides)
            return ExecutionResult(
                status="executed",
                change_summary=f"Added {needed} new slide(s). Now at {target_count} slides.",
                action_id=None,
                updated_outline=new_outline,
            )

        if tool_name == "reorder_slides":
            new_order = tool_args.get("new_order", [])
            new_outline = _apply_reorder_slides(current_outline, new_order)
            return ExecutionResult(
                status="executed",
                change_summary="Reordered slides.",
                action_id=None,
                updated_outline=new_outline,
            )

        return ExecutionResult(
            status="declined",
            change_summary=f"Unknown tool: {tool_name}",
            action_id=None,
            updated_outline=None,
        )

    except Exception as e:
        return ExecutionResult(
            status="declined",
            change_summary=f"Error executing {tool_name}: {e}",
            action_id=None,
            updated_outline=None,
        )


def _apply_update_slides(outline: dict, changes: list[dict]) -> dict:
    """Apply update_slides changes to outline dict."""
    new_outline = dict(outline)
    slides = list(new_outline.get("slides", []))

    for change in changes:
        slide_index = change.get("slide_index")
        if 0 <= slide_index < len(slides):
            slide = dict(slides[slide_index])
            content = dict(slide.get("content", {}))
            if "new_title" in change:
                slide["title"] = change["new_title"]
            if "new_speaker_notes" in change:
                slide["speaker_notes"] = change["new_speaker_notes"]

            layout = slide.get("layout", "title_and_content")
            if "new_bullets" in change:
                if layout in {"title_and_content", "image_and_text"}:
                    content["bullets"] = change["new_bullets"]
                elif layout == "two_column":
                    if "new_left_bullets" in change:
                        content["left_bullets"] = change["new_left_bullets"]
                    if "new_right_bullets" in change:
                        content["right_bullets"] = change["new_right_bullets"]
                    if (
                        "new_left_bullets" not in change
                        and "new_right_bullets" not in change
                    ):
                        bullets = change["new_bullets"]
                        midpoint = (len(bullets) + 1) // 2
                        content["left_bullets"] = bullets[:midpoint]
                        content["right_bullets"] = bullets[midpoint:]
                elif layout == "big_statement":
                    if "new_statement" in change:
                        content["statement"] = change["new_statement"]
                    else:
                        content["statement"] = " ".join(change["new_bullets"])
                elif layout == "section_header":
                    if "new_heading" in change:
                        content["heading"] = change["new_heading"]
                    if "new_subheading" in change:
                        content["subheading"] = change["new_subheading"]
                elif layout == "quote":
                    if "new_quote" in change:
                        content["quote"] = change["new_quote"]
                elif layout == "closing":
                    if "new_headline" in change:
                        content["headline"] = change["new_headline"]
                    if "new_cta" in change:
                        content["cta"] = change["new_cta"]
                elif layout == "timeline":
                    if "new_events" in change:
                        content["events"] = change["new_events"]
                else:
                    try:
                        content["bullets"] = change["new_bullets"]
                    except KeyError:
                        pass
            else:
                if layout == "two_column":
                    if "new_left_bullets" in change:
                        content["left_bullets"] = change["new_left_bullets"]
                    if "new_right_bullets" in change:
                        content["right_bullets"] = change["new_right_bullets"]
                elif layout == "big_statement" and "new_statement" in change:
                    content["statement"] = change["new_statement"]
                elif layout == "section_header":
                    if "new_heading" in change:
                        content["heading"] = change["new_heading"]
                    if "new_subheading" in change:
                        content["subheading"] = change["new_subheading"]
                elif layout == "quote" and "new_quote" in change:
                    content["quote"] = change["new_quote"]
                elif layout == "closing":
                    if "new_headline" in change:
                        content["headline"] = change["new_headline"]
                    if "new_cta" in change:
                        content["cta"] = change["new_cta"]
                elif layout == "timeline" and "new_events" in change:
                    content["events"] = change["new_events"]

            slide["content"] = content
            slides[slide_index] = slide

    new_outline["slides"] = slides
    return new_outline


def _apply_add_slides(outline: dict, new_slides: list[dict]) -> dict:
    """Apply add_slides changes to outline dict."""
    new_outline = dict(outline)
    slides = list(new_outline.get("slides", []))
    normalized_slides = []
    for slide in new_slides:
        normalized_slide = dict(slide)
        if "layout" not in normalized_slide:
            normalized_slide["layout"] = "title_and_content"
        if "content" not in normalized_slide:
            normalized_slide["content"] = {"bullets": []}
        normalized_slides.append(normalized_slide)
    slides.extend(normalized_slides)
    new_outline["slides"] = slides
    return new_outline


def _apply_delete_slides(outline: dict, slide_indices: list[int]) -> dict:
    """Apply delete_slides changes to outline dict."""
    new_outline = dict(outline)
    slides = list(new_outline.get("slides", []))
    for idx in sorted(slide_indices, reverse=True):
        if 0 <= idx < len(slides):
            slides.pop(idx)
    new_outline["slides"] = slides
    return new_outline


def _apply_reorder_slides(outline: dict, new_order: list[int]) -> dict:
    """Apply reorder_slides changes to outline dict."""
    new_outline = dict(outline)
    slides = list(new_outline.get("slides", []))
    reordered_slides = [slides[i] for i in new_order if 0 <= i < len(slides)]
    new_outline["slides"] = reordered_slides
    return new_outline
