"""Shared TypedDict schemas for S3 data contracts. All Lambdas import from here — do not redefine these structures locally."""

from typing import Dict, List, Literal, Optional, TypedDict


class ModuleSummary(TypedDict):
    name: str
    description: str
    file_path: str


class Citation(TypedDict):
    file_path: str
    name: str
    kind: str
    source: str


class RepoOwner(TypedDict):
    owner: Optional[str]
    repo_name: Optional[str]
    source: str


class SetupInstructions(TypedDict):
    setup_markdown: str
    files_used: List[str]
    skipped: bool


class FolderNode(TypedDict):
    path: str
    description: str
    level: int
    children: List[dict]


class FolderHierarchy(TypedDict):
    folders: List[FolderNode]
    root_files: List[Dict[str, str]]


class AcronymEntry(TypedDict):
    acronym: str
    full_name: str


class FindingsSchema(TypedDict):
    purpose: str
    one_liner: str
    modules: List[ModuleSummary]
    incomplete_features: List[str]
    dependency_graph: str
    purpose_citations: List[Citation]
    module_citations: List[Citation]
    incomplete_citations: List[Citation]
    repo_owner: RepoOwner
    setup_instructions: SetupInstructions
    folder_hierarchy: FolderHierarchy
    acronyms: List[AcronymEntry]
    was_chunked: bool


# outline.json — written by summarizer Lambda, read by slides Lambda
class TitleAndContentSlide(TypedDict):
    bullets: List[str]


class TwoColumnSlide(TypedDict):
    left_header: str
    left_bullets: List[str]
    right_header: str
    right_bullets: List[str]


class BigStatementSlide(TypedDict):
    statement: str


class SectionHeaderSlide(TypedDict):
    heading: str
    subheading: str


class QuoteSlide(TypedDict):
    quote: str
    attribution: str


class TimelineEvent(TypedDict):
    label: str
    description: str


class TimelineSlide(TypedDict):
    events: List[TimelineEvent]


class ImageAndTextSlide(TypedDict):
    caption: str
    bullets: List[str]


class ClosingSlide(TypedDict):
    headline: str
    cta: str


class SlideSchema(TypedDict):
    layout: Literal[
        "title_slide",
        "title_and_content",
        "two_column",
        "big_statement",
        "section_header",
        "quote",
        "timeline",
        "image_and_text",
        "closing",
        "data_table",
    ]
    title: str
    content: dict
    speaker_notes: List[str]
    _paragraph: str
    _source_index: int


class OutlineSchema(TypedDict):
    title: str
    slides: List[SlideSchema]
