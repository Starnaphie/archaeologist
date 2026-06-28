import json
import re
from pathlib import Path
from dataclasses import dataclass

from openai import OpenAI

from .tools_registry import AGENT_TOOLS

from dotenv import load_dotenv

# Walk up to repo root .env regardless of where the process is invoked from
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Pre-flight regex patterns for count-based instructions (case-insensitive).
# Each pattern captures a 1–2 digit number as group 1.
_COUNT_PATTERNS = [
    re.compile(r"\bmake\s+it\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bgive\s+me\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bi\s+want\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\btrim(?:\s+it)?(?:\s+down)?\s+to\s+(\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\bcut(?:\s+down)?\s+to\s+(\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\breduce\s+to\s+(\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\bonly\s+want\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bonly\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bjust\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bchange\s+to\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
    re.compile(r"\bset\s+it\s+to\s+(\d{1,2})\s+slides?\b", re.IGNORECASE),
]


def detect_count_instruction(instruction: str) -> int | None:
    """Detect a target slide-count from a natural-language instruction.

    Returns the target count (1–50) if the instruction matches a known
    count pattern, or ``None`` otherwise.
    """
    for pattern in _COUNT_PATTERNS:
        m = pattern.search(instruction)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 50:
                return n
    return None

def _build_system_prompt(audience: str, tone: str) -> str:
    if tone == "casual":
        tone_block = (
            "Tone: Casual. Be conversational and story-driven. Use first-person "
            "where natural. Anecdotes and concrete scenarios are welcome. Avoid "
            "dense data blocks — if you use a number, give it human context. "
            "Write like you're explaining to a smart friend."
        )
    elif tone == "academic":
        tone_block = (
            "Tone: Academic. Use formal register throughout. Claims should be "
            "hedged appropriately ('evidence suggests', 'findings indicate'). "
            "Be citation-aware — flag where a source would strengthen a claim. "
            "Prefer precision over punchy language."
        )
    else:
        tone_block = (
            "Tone: Professional. Be data-forward and precise. Lead with evidence "
            "and specific figures where possible. Keep language clean and direct. "
            "Avoid jargon unless the audience expects it. Never be conversational "
            "or casual."
        )

    return "\n\n".join(
        [
            (
                "You are an expert presentation designer who has coached TED "
                "speakers and built decks for Fortune 500 keynotes. Your job is "
                "to produce slide content that tells a compelling story, not a "
                "list of subtopics."
            ),
            (
                f"Audience: {audience}\n"
                "Calibrate vocabulary to this audience's expertise level. Assume "
                "only the prior knowledge this audience would have. Surface what "
                "this audience concretely cares about and stands to gain. Avoid "
                "terminology that would alienate or bore them."
            ),
            tone_block,
            (
                "Narrative principles:\n"
                "- Open with a hook: the first content slide should surface a "
                "surprising fact, a provocative question, or a concrete scenario "
                "that makes the audience care.\n"
                "- Build a narrative arc: set up context, introduce tension or a "
                "problem, develop key ideas with evidence, then resolve toward a "
                "clear takeaway.\n"
                "- Each slide should make exactly ONE point. The title of the "
                "slide should be a complete assertion or question, not a vague "
                "label. Bad: \"Benefits\". Good: \"Teams using X ship 40% faster\".\n"
                "- Bullet points are supporting evidence, examples, or short data "
                "points — never restatements of the title.\n"
                "- Speaker notes should be a JSON array of concise bullet-point "
                "strings — each item is one talking point covering what to say, "
                "where to pause, or how to transition to the next slide.\n"
                "- End with a memorable closing slide that drives action or "
                "leaves the audience with a sticky idea."
            ),
            "Return ONLY valid JSON — no markdown fences, no commentary.",
        ]
    )


def _pass_progression(
    topic: str,
    description: str,
    audience: str,
    tone: str,
    max_slides: int = 20,
) -> list[dict]:
    client = OpenAI()
    desc_line = f"Description: {description}\n" if description else ""
    user_prompt = (
        f"Topic: {topic}\n"
        f"{desc_line}"
        f"Maximum slides: {max_slides} (this is a hard ceiling — do not exceed it)\n\n"
        "Generate the narrative progression for this presentation as an ordered "
        "list of slide beats. Each beat is a hidden director's note describing "
        "what this slide is FOR in the story — not the text that will appear on "
        "it. Think in terms of narrative arc: hook → context → tension → "
        "development → resolution → close. Produce as many beats as the topic "
        "genuinely needs. A tight focused arc is better than a padded one. Do "
        "not pad to hit the maximum.\n\n"
        "Return ONLY a JSON array. Each element has exactly two fields: 'index' "
        "(integer, 0-based) and 'narrative_role' (string describing the slide's "
        "purpose in the story).\n\n"
        'Example element: {"index": 0, "narrative_role": "Hook — surface the '
        'surprising fact that reframes the audience\'s assumption about X"}'
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": _build_system_prompt(audience, tone)},
            {"role": "user", "content": user_prompt},
        ],
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()

    try:
        progression = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Pass 1 failed to return valid JSON: {text}") from exc

    if not isinstance(progression, list):
        raise ValueError(f"Pass 1 failed to return valid JSON: {text}")

    if len(progression) > max_slides:
        progression = progression[:max_slides]
        for index, beat in enumerate(progression):
            if isinstance(beat, dict):
                beat["index"] = index

    return progression


def _pass_paragraph_content(
    progression: list[dict],
    topic: str,
    audience: str,
    tone: str,
) -> list[dict]:
    client = OpenAI()
    system_prompt = _build_system_prompt(audience, tone)
    progression_context = "\n".join(
        f"{beat.get('index', index)}. {beat.get('narrative_role', '')}"
        for index, beat in enumerate(progression)
    )
    expanded: list[dict] = []

    for start in range(0, len(progression), 5):
        batch = progression[start:start + 5]
        beats_block = "\n".join(
            f"{beat.get('index', start + index)}. {beat.get('narrative_role', '')}"
            for index, beat in enumerate(batch)
        )
        user_prompt = (
            f"Topic: {topic}\n\n"
            f"Full presentation arc (read-only context):\n{progression_context}\n\n"
            "Generate a paragraph for each of the following slide beats. Each "
            "paragraph should be the information-dense version of that slide — "
            "everything the speaker knows about this beat, written as flowing "
            "prose. This text will never appear on the slide itself; it is what "
            "the speaker knows and what will later be distilled into minimal "
            "slide text.\n\n"
            f"Beats to expand:\n{beats_block}\n\n"
            "Return ONLY a JSON array. Each element has: 'index' (integer "
            "matching the input beat's index), 'narrative_role' (copied from "
            "input), 'paragraph' (the generated prose string)."
        )

        last_error: Exception | None = None
        for _attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=2048,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                text = response.choices[0].message.content.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()

                batch_result = json.loads(text)
                if not isinstance(batch_result, list):
                    raise ValueError("Pass 2 failed to return a JSON array")
                expanded.extend(batch_result)
                last_error = None
                break
            except Exception as exc:
                last_error = exc

        if last_error is not None:
            raise last_error

    paragraphs_by_index = {
        item.get("index"): item.get("paragraph", "")
        for item in expanded
        if isinstance(item, dict)
    }
    roles_by_index = {
        item.get("index"): item.get("narrative_role", "")
        for item in expanded
        if isinstance(item, dict)
    }

    merged: list[dict] = []
    for index, beat in enumerate(progression):
        beat_index = beat.get("index", index)
        merged_beat = dict(beat)
        merged_beat["index"] = beat_index
        if roles_by_index.get(beat_index):
            merged_beat["narrative_role"] = roles_by_index[beat_index]
        merged_beat["paragraph"] = paragraphs_by_index.get(beat_index, "")
        merged.append(merged_beat)

    return sorted(merged, key=lambda item: item.get("index", 0))


def _pass_template_and_content(
    paragraphs: list[dict],
    audience: str,
    tone: str,
) -> list[dict]:
    client = OpenAI()
    system_prompt = _build_system_prompt(audience, tone)
    layout_reference_block = "\n".join(
        [
            'title_and_content — default. Use when no other layout fits better. Content: {"bullets": ["..."]}',
            'two_column — comparisons, before/after, pros/cons. Content: {"left_header": str, "left_bullets": [...], "right_header": str, "right_bullets": [...]}',
            'big_statement — single bold claim, punchy stat, one idea that must land before explanation. Content: {"statement": str}',
            'section_header — transition between major thematic blocks. Content: {"heading": str, "subheading": str}',
            'quote — striking statistic, real quote, thesis restatement. Content: {"quote": str, "attribution": str}',
            'timeline — chronological sequences, roadmaps, step progressions. Content: {"events": [{"label": str, "description": str}]}',
            'image_and_text — spatially or visually described concepts. Content: {"caption": str, "bullets": [...]}',
            'closing — final slide only, call to action. Content: {"headline": str, "cta": str}',
            "data_table — RESERVED. Never assign this layout.",
        ]
    )
    merged: list[dict] = []

    for start in range(0, len(paragraphs), 5):
        batch = paragraphs[start:start + 5]
        batch_block = "\n\n".join(
            (
                f"index: {item.get('index', start + index)}\n"
                f"narrative_role: {item.get('narrative_role', '')}\n"
                f"paragraph: {item.get('paragraph', '')}"
            )
            for index, item in enumerate(batch)
        )
        user_prompt = (
            f"Layout reference:\n{layout_reference_block}\n\n"
            "For each input paragraph, output one or more slides. Rules:\n"
            "  - You may output 1 to 3 slides per paragraph.\n"
            "  - If expanding to multiple slides, the first may be a "
            "section_header to introduce the group.\n"
            "  - Text on every slide must be minimal — the paragraph is what "
            "you know, not what you show.\n"
            "  - title_and_content is always the safe default if nothing fits "
            "more naturally.\n"
            "  - Do not force interesting layouts onto content that does not "
            "clearly warrant them.\n"
            "  - Never assign data_table.\n"
            "  - Preserve source_index from the input so each output slide "
            "carries the index of the paragraph it came from.\n\n"
            f"{batch_block}\n\n"
            "Return ONLY a JSON array of slide objects. Each has: "
            "'source_index' (int), 'layout' (string), 'title' (string — a "
            "complete assertion or question, not a label), 'content' (object "
            "matching the layout schema above)."
        )

        last_error: Exception | None = None
        for _attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=4096,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                text = response.choices[0].message.content.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()

                batch_result = json.loads(text)
                if not isinstance(batch_result, list):
                    raise ValueError("Pass 3 failed to return a JSON array")
                merged.extend(batch_result)
                last_error = None
                break
            except Exception as exc:
                last_error = exc

        if last_error is not None:
            raise last_error

    ordered = sorted(
        enumerate(merged),
        key=lambda pair: (pair[1].get("source_index", 0), pair[0]),
    )
    return [item for _, item in ordered]


def _pass_speaker_notes(
    slides: list[dict],
    paragraphs: list[dict],
    audience: str,
    tone: str,
) -> list[dict]:
    paragraphs_by_index = {
        item.get("index"): item
        for item in paragraphs
        if isinstance(item, dict)
    }
    system_prompt = _build_system_prompt(audience, tone)
    client = OpenAI()

    for start in range(0, len(slides), 5):
        batch = slides[start:start + 5]
        slide_blocks = []
        for batch_index, slide in enumerate(batch):
            source_index = slide.get("source_index")
            source_paragraph = paragraphs_by_index.get(source_index, {}).get(
                "paragraph", ""
            )
            slide_blocks.append(
                "\n".join(
                    [
                        f"batch_index: {batch_index}",
                        f"layout: {slide.get('layout', '')}",
                        f"title: {slide.get('title', '')}",
                        f"content: {json.dumps(slide.get('content', {}))}",
                        f"source paragraph: {source_paragraph}",
                    ]
                )
            )

        user_prompt = (
            "Generate speaker notes for each slide below. Notes should bridge "
            "the gap between the minimal slide text and the full source "
            "paragraph — they are what the speaker says to fill in everything "
            "the audience does not see on screen.\n\n"
            "Rules:\n"
            "  - Each note item is one concise talking point, transition cue, "
            "or emphasis instruction.\n"
            "  - Include where to pause, what to emphasize, and how to "
            "transition to the next slide.\n"
            "  - If multiple slides share a source_index, distribute the source "
            "paragraph's content across their notes — do not repeat the same "
            "points.\n"
            "  - 2 to 4 note items per slide. Never more than 5.\n\n"
            + "\n\n".join(slide_blocks)
            + "\n\nReturn ONLY a JSON array. Each element has: 'batch_index' "
            "(int matching the position in the input list), 'speaker_notes' "
            "(array of strings)."
        )

        batch_notes: list[dict] | None = None
        for _attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=2048,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                text = response.choices[0].message.content.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0].strip()

                parsed = json.loads(text)
                if not isinstance(parsed, list):
                    raise ValueError("Pass 4 failed to return a JSON array")
                batch_notes = parsed
                break
            except Exception:
                batch_notes = None

        if batch_notes is None:
            for slide in batch:
                slide["speaker_notes"] = []
            continue

        for item in batch_notes:
            if not isinstance(item, dict):
                continue
            batch_index = item.get("batch_index")
            if not isinstance(batch_index, int):
                continue
            if 0 <= batch_index < len(batch):
                notes = item.get("speaker_notes", [])
                batch[batch_index]["speaker_notes"] = notes if isinstance(notes, list) else []

        for slide in batch:
            slide.setdefault("speaker_notes", [])

    return slides


def generate_outline(
    topic: str,
    audience: str,
    num_slides: int | None = None,
    tone: str = "professional",
    description: str = "",
) -> dict:
    """Generate an outline through a 4-pass narrative pipeline.

    Pass 1 creates narrative beats up to the max_slides ceiling, using
    num_slides when provided and 20 otherwise. Pass 2 expands each beat into
    hidden paragraph knowledge, pass 3 selects slide layouts and minimal slide
    content, and pass 4 adds speaker notes. Each returned slide includes
    _paragraph and _source_index so downstream renderers can trace the compact
    slide text back to its source paragraph.
    """
    max_slides = num_slides if num_slides is not None else 20
    progression = _pass_progression(topic, description, audience, tone, max_slides)
    paragraphs = _pass_paragraph_content(progression, topic, audience, tone)
    expanded_slides = _pass_template_and_content(paragraphs, audience, tone)
    slides_with_notes = _pass_speaker_notes(expanded_slides, paragraphs, audience, tone)

    paragraphs_by_index = {
        item.get("index"): item.get("paragraph", "")
        for item in paragraphs
        if isinstance(item, dict)
    }
    for slide in slides_with_notes:
        source_index = slide.get("source_index")
        slide["_paragraph"] = paragraphs_by_index.get(source_index, "")
        slide["_source_index"] = source_index

    slide_titles = "\n".join(
        f"{index + 1}. {slide.get('title', '')}"
        for index, slide in enumerate(slides_with_notes)
    )
    client = OpenAI()
    title_prompt = (
        f"Topic: {topic}\n"
        f"Audience: {audience}\n"
        f"Tone: {tone}\n\n"
        f"Slide titles:\n{slide_titles}\n\n"
        "Return only a concise compelling presentation title — no punctuation "
        "at the end, no quotes, no explanation. 8 words maximum."
    )
    title_response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=64,
        messages=[
            {"role": "user", "content": title_prompt},
        ],
    )
    inferred_title = title_response.choices[0].message.content.strip().strip('"').strip("'")
    inferred_title = inferred_title.rstrip(".!?")

    return {
        "title": inferred_title,
        "slides": slides_with_notes,
    }


@dataclass
class ToolCallResult:
    """Result of a tool-augmented revision request."""
    tool_name: str
    tool_args: dict
    model_message: str | None


@dataclass
class PlanResult:
    """Result of a plan-only revision request (no tool execution)."""
    plan_text: str


PLAN_SYSTEM_PROMPT = (
    "You are a presentation assistant. The user wants to make a change to their "
    "slide deck. Describe in 1-2 plain English sentences exactly what you will do "
    "to fulfill their request. Be specific: name which slides will be affected, "
    "what will change, and how many slides will be added/removed if relevant. "
    "Do not use technical tool names. Do not ask clarifying questions. "
    "Do not make the change yet — just describe the plan.\n\n"
    "If the request is something the agent cannot do (font changes, images, "
    "themes, animations, exports, slide duplication), your plan should start "
    "with \"I can't do that —\" and explain why, then suggest the closest "
    "supported alternative."
)


def plan_revision(
    history: list[dict],
    current_outline: dict,
    instruction: str,
) -> PlanResult:
    """Ask the model to describe its plan in plain English, without executing.

    Args:
        history: Conversation history (list of {"role": str, "content": str})
        current_outline: Current presentation outline dict
        instruction: User's revision instruction

    Returns:
        PlanResult with the plan_text string.
    """
    client = OpenAI()

    slides = current_outline.get("slides", [])
    slide_count = len(slides)
    titles_block = "\n".join(
        f"{i + 1}. {slide.get('title', '(untitled)')}"
        for i, slide in enumerate(slides)
    )

    user_message = (
        f"Current slide count: {slide_count} slides (not counting the title slide).\n\n"
        f"Slide titles:\n{titles_block}\n\n"
        f"User instruction:\n{instruction}"
    )

    messages = [
        {"role": "system", "content": PLAN_SYSTEM_PROMPT},
    ] + history + [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=256,
        messages=messages,
    )

    return PlanResult(
        plan_text=response.choices[0].message.content.strip(),
    )


REVISE_SYSTEM_PROMPT = """\
You are editing a freshly generated presentation. There is no existing deck to load or create — one has already been produced for this session.

You are an expert presentation assistant. You refine slide content based on user instructions.

Available tools and when to use them:

TOOL SELECTION RULES
- set_slide_count: resize to a target total. Use ONLY when a number appears with no topic content ("make it 6 slides", "trim to 10"). NEVER if a subject is named.
- add_slides: add new content by topic. Use when a subject is named, even if a number appears ("add two slides about X" → add_slides, not set_slide_count).
- delete_slides: remove specific named or numbered slides only.
- update_slides: change content on existing slides.
- reorder_slides: rearrange slide order.
- respond: anything unsupported (fonts, images, PDF export, themes, animations). Explain and offer the closest supported alternative.

KEY: number + topic = add_slides. Number alone = set_slide_count.

UNSUPPORTED REQUESTS
If the user asks for something none of the available tools can do, do NOT pick the closest-sounding tool as a fallback. Instead use the respond tool to explain what you can't do and what you CAN offer instead. Examples:

- 'change the font' → not supported. Respond: 'I can't change fonts through this agent. I can update slide content, titles, and structure.'
- 'add an image' → not supported. Respond: 'Image insertion isn't supported. I can add a new slide with text content about that topic instead.'
- 'export as PDF' → not supported. Respond: 'I can't export files from this editor.'
- 'change the theme or colors' → not supported.
- 'add animations or transitions' → not supported.
- 'duplicate a slide' → not supported directly; offer to add_slides with the same content instead.

Never silently pick delete_slides, update_slides, or any other tool when the request doesn't match. An honest 'I can't do that' is always better than a wrong action.

Be precise with tool arguments and think through the changes carefully.
"""


def revise_with_tools(
    history: list[dict],
    current_outline: dict,
    instruction: str,
) -> ToolCallResult:
    """Revise a presentation using tool-augmented API calls.

    Args:
        history: Conversation history (list of {"role": str, "content": str})
        current_outline: Current presentation outline dict
        instruction: User's revision instruction

    Returns:
        ToolCallResult with tool_name, tool_args, and optional model_message
    """
    client = OpenAI()

    # Build the user message with current outline context
    slide_count = len(current_outline.get("slides", []))
    user_message = (
        f"Current slide count: {slide_count} slides (not counting the title slide).\n\n"
        f"Current presentation:\n\n{json.dumps(current_outline, indent=2)}\n\n"
        f"User instruction:\n{instruction}"
    )

    # Prepare messages: system prompt first, then history, then new instruction
    messages = [
        {"role": "system", "content": REVISE_SYSTEM_PROMPT},
    ] + history + [{"role": "user", "content": user_message}]

    # Call with tool_choice="required" to force tool use
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2048,
        tools=AGENT_TOOLS,
        tool_choice="required",
        messages=messages,
    )

    # Extract the first tool call from the response
    choice = response.choices[0]
    model_message = choice.message.content

    # Check for tool calls
    if choice.message.tool_calls:
        tool_call = choice.message.tool_calls[0]
        return ToolCallResult(
            tool_name=tool_call.function.name,
            tool_args=json.loads(tool_call.function.arguments),
            model_message=model_message,
        )
    else:
        # No tool call returned (shouldn't happen with tool_choice="required")
        return ToolCallResult(
            tool_name="",
            tool_args={},
            model_message=model_message,
        )
