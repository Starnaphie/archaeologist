import os
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from . import embedder

LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)

INCOMPLETE_MARKERS = ("TODO", "FIXME", "NotImplemented", "raise NotImplementedError")

_PASS_STUB_RE = re.compile(
    r'^\s*(?:async\s+)?def\s+\w+\([^)]*\)\s*(?:->[^:]+)?:\s*\n'
    r'(?:\s*(?:"""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\'\'\')\s*\n)?'
    r'\s*pass\s*$',
    re.MULTILINE,
)


class PurposeOutput(BaseModel):
    purpose: str
    one_liner: str


class ModuleSummary(BaseModel):
    name: str
    description: str


class ArchitectureOutput(BaseModel):
    modules: List[ModuleSummary]


class IncompleteOutput(BaseModel):
    incomplete_features: List[str]


@dataclass
class ReportJSON:
    purpose: str
    one_liner: str
    modules: List[dict] = field(default_factory=list)
    incomplete_features: List[str] = field(default_factory=list)
    dependency_graph: str = ""


_STDLIB_PREFIXES = set(getattr(sys, "stdlib_module_names", set())) | {
    "__future__", "builtins",
}

_THIRD_PARTY_PREFIXES = {
    "anyio", "attr", "attrs", "boto3", "botocore", "certifi", "click",
    "dotenv", "faiss", "fastapi", "git", "h11", "httpx", "httpcore",
    "jinja2", "jiter", "jsonpatch", "jsonpointer", "langchain",
    "langchain_core", "langchain_openai", "langgraph", "langsmith",
    "markdown", "markupsafe", "numpy", "openai", "orjson", "ormsgpack",
    "packaging", "pallets_sphinx_themes", "pandas", "pluggy", "pydantic",
    "pydantic_core", "pytest", "regex", "requests", "rich", "smmap",
    "sniffio", "sphinx", "sphinxcontrib", "sqlalchemy", "sse_starlette",
    "starlette", "tenacity", "tiktoken", "tornado", "tqdm",
    "tree_sitter", "tree_sitter_python", "uvicorn", "websockets", "werkzeug",
    "yaml", "pyyaml",
}

_EXTERNAL_PREFIXES = _STDLIB_PREFIXES | _THIRD_PARTY_PREFIXES

_MAX_NODES = 20


def _is_internal_module(name: str) -> bool:
    if not name:
        return False
    if name.startswith("."):
        return True
    return name.split(".")[0] not in _EXTERNAL_PREFIXES


def _normalize_module(name: str) -> str:
    return name.lstrip(".") or name


def _mermaid_id(name: str) -> str:
    return "n_" + re.sub(r"[^A-Za-z0-9_]", "_", name)


def build_mermaid_graph(symbol_map: dict) -> str:
    internal = sorted({
        _normalize_module(m)
        for m in symbol_map.keys()
        if _is_internal_module(m) and _normalize_module(m)
    })

    truncated = False
    if len(internal) > _MAX_NODES:
        internal = internal[:_MAX_NODES]
        truncated = True

    internal_set = set(internal)
    edges: List[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for module in internal:
        parts = module.split(".")
        for i in range(1, len(parts)):
            parent = ".".join(parts[:i])
            if parent in internal_set:
                edge = (parent, module)
                if edge not in seen:
                    edges.append(edge)
                    seen.add(edge)

    lines = ["graph LR"]
    declared: set[str] = set()
    for src, dst in edges:
        if src not in declared:
            lines.append(f'    {_mermaid_id(src)}["{src}"]')
            declared.add(src)
        if dst not in declared:
            lines.append(f'    {_mermaid_id(dst)}["{dst}"]')
            declared.add(dst)
        lines.append(f"    {_mermaid_id(src)} --> {_mermaid_id(dst)}")
    for module in internal:
        if module not in declared:
            lines.append(f'    {_mermaid_id(module)}["{module}"]')
            declared.add(module)

    if truncated:
        lines.append(f'    %% truncated to {_MAX_NODES} nodes')

    graph_string = "\n".join(lines)
    print(f"symbol_map: {symbol_map}")
    print(f"mermaid output: {graph_string}")
    return graph_string


def _format_chunks(chunks: List[dict], root: str | None = None) -> str:
    return "\n\n---\n\n".join(
        f"# {_rel_path(c.get('file_path', ''), root)} :: {c.get('kind')} {c.get('name')}\n{c.get('source', '')}"
        for c in chunks
    )


def _rel_path(file_path: str, root: str | None) -> str:
    if not file_path:
        return ""
    if root:
        try:
            return os.path.relpath(file_path, root)
        except ValueError:
            return file_path
    return file_path


def _is_stub(chunk: dict) -> bool:
    src = chunk.get("source", "")
    if any(marker in src for marker in INCOMPLETE_MARKERS):
        return True
    if chunk.get("kind") == "function" and _PASS_STUB_RE.search(src):
        return True
    return False


def _chunks_for_file(file_path: str, limit: int = 3) -> List[dict]:
    matches = [c for c in embedder._chunks if c.get("file_path") == file_path]
    return matches[:limit]


def _purpose_step(root: str | None) -> tuple[List[dict], PurposeOutput]:
    chunks = embedder.retrieve("what does this project do", k=10)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are analyzing a codebase. Infer the project's purpose from representative chunks."),
        ("human",
         "Representative code chunks:\n\n{chunks}\n\n"
         "Return `purpose` (1-3 sentences) and `one_liner` (≤15 words)."),
    ])
    result = (prompt | LLM.with_structured_output(PurposeOutput)).invoke(
        {"chunks": _format_chunks(chunks, root)}
    )
    return chunks, result


def _architecture_step(seed_chunks: List[dict], root: str | None) -> ArchitectureOutput:
    unique_files = list(dict.fromkeys(c["file_path"] for c in seed_chunks))
    per_file: List[tuple[str, List[dict]]] = [
        (fp, _chunks_for_file(fp, 3)) for fp in unique_files
    ]

    blocks = []
    for file_path, chunks in per_file:
        if not chunks:
            continue
        blocks.append(f"## {_rel_path(file_path, root)}\n{_format_chunks(chunks, root)}")
    joined = "\n\n===\n\n".join(blocks)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize each Python module in one sentence based on its representative chunks."),
        ("human",
         "Per-module chunks:\n\n{blocks}\n\n"
         "For each module, return `name` (the relative file path exactly as shown) "
         "and `description` (one sentence)."),
    ])
    return (prompt | LLM.with_structured_output(ArchitectureOutput)).invoke({"blocks": joined})


def _incomplete_step(root: str | None) -> IncompleteOutput:
    matches = [c for c in embedder._chunks if _is_stub(c)]
    if not matches:
        return IncompleteOutput(incomplete_features=[])

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You receive code chunks that look incomplete (TODO/FIXME/NotImplementedError/empty pass bodies). "
         "Describe each as a short, user-readable feature gap."),
        ("human",
         "Suspect chunks:\n\n{chunks}\n\n"
         "Return `incomplete_features` as a list of short strings, one per gap."),
    ])
    return (prompt | LLM.with_structured_output(IncompleteOutput)).invoke(
        {"chunks": _format_chunks(matches, root)}
    )


def generate_report(symbol_map: dict | None = None, root: str | None = None) -> ReportJSON:
    seed_chunks, purpose = _purpose_step(root)
    architecture = _architecture_step(seed_chunks, root)
    incomplete = _incomplete_step(root)
    dependency_graph = build_mermaid_graph(symbol_map or {})

    return ReportJSON(
        purpose=purpose.purpose,
        one_liner=purpose.one_liner,
        modules=[asdict(m) if hasattr(m, "__dataclass_fields__") else m.model_dump()
                 for m in architecture.modules],
        incomplete_features=list(incomplete.incomplete_features),
        dependency_graph=dependency_graph,
    )
