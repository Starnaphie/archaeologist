"""GPT-4o-powered presentation rewriter.

Takes an existing outline and a natural-language instruction and returns a
fully revised outline in the same JSON schema.
"""

import json

from openai import OpenAI

_SYSTEM_PROMPT = """\
You are an expert presentation designer who has coached TED speakers and built \
decks for Fortune 500 keynotes. You are given an existing slide deck as JSON \
and a user instruction describing how to revise it.

Apply the instruction thoughtfully and return the complete revised deck. \
Follow these principles:
- Each slide should make exactly ONE point. Titles must be complete assertions \
or questions, not vague labels. Bad: "Benefits". Good: "Teams using X ship 40% faster".
- Bullet points are supporting evidence, examples, or data points — never \
restatements of the title.
- Speaker notes should be a JSON array of concise bullet-point strings, each \
covering one talking point, pause cue, or transition.
- Preserve the overall narrative arc unless the instruction explicitly changes it.
- Return the SAME schema as the input: a JSON object with "title" (string) and \
"slides" (array of objects with "title", "bullets", and "speaker_notes").

Return ONLY valid JSON — no markdown fences, no commentary.\
"""


def rewrite_outline(current_outline: dict, instruction: str) -> dict:
    """Rewrite a presentation outline using GPT-4o.

    Args:
        current_outline: The current outline dict with "title" and "slides".
        instruction: Natural-language instruction describing the desired changes.

    Returns:
        Revised outline dict in the same schema as current_outline.
    """
    client = OpenAI()

    user_message = (
        f"Current presentation:\n\n{json.dumps(current_outline, indent=2)}\n\n"
        f"Instruction:\n{instruction}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()

    return json.loads(text)
