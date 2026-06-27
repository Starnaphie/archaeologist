import os
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from . import embedder


def _load_known_packages() -> set[str]:
    packages = set()
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    try:
        with open(req_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                line = line.split("#")[0].strip()
                line = re.split(r'[=!><~]+', line)[0].strip()
                line = line.split("[")[0].strip()
                normalized = line.replace("-", "_").lower()
                if normalized:
                    packages.add(normalized)
    except FileNotFoundError:
        print("WARNING: requirements.txt not found, dependency filtering may be inaccurate.")
        return set()
    return packages


_KNOWN_THIRD_PARTY = _load_known_packages()

LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)

INCOMPLETE_MARKERS = ("TODO", "FIXME", "NotImplemented", "raise NotImplementedError")

# Matches a function whose entire body is a bare `pass` statement,
# optionally preceded by a docstring. These are treated as stubs —
# the developer declared the function signature but never implemented it.
#
# Pattern breakdown:
#   Line 1 — optional `async`, then `def name(...):` with optional
#             return type annotation
#   Line 2 — optional docstring (single or triple quoted)
#   Line 3 — `pass` as the only statement in the body

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
    purpose_citations: List[dict] = field(default_factory=list)
    module_citations: List[dict] = field(default_factory=list)
    incomplete_citations: List[dict] = field(default_factory=list)


_STDLIB_PREFIXES = set(getattr(sys, "stdlib_module_names", set())) | {
    "__future__", "builtins",
}

_MAX_NODES = 20


def _is_internal_module(name: str) -> bool:
    if not name:
        return False
    if name.startswith("."):
        return True
    first_segment = name.split(".")[0].replace("-", "_").lower()
    return first_segment not in _STDLIB_PREFIXES and first_segment not in _KNOWN_THIRD_PARTY


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
    result = (prompt | LLM.with_structured_output(PurposeOutput, method="function_calling")).invoke(
        {"chunks": _format_chunks(chunks, root)}
    )
    return chunks, result


def _architecture_step(root: str | None) -> tuple[List[dict], ArchitectureOutput]:
    unique_files = list(dict.fromkeys(
        c["file_path"] for c in embedder._chunks
    ))
    per_file: List[tuple[str, List[dict]]] = [
        (fp, _chunks_for_file(fp, 3)) for fp in unique_files
    ]

    all_chunks = []
    blocks = []
    for file_path, chunks in per_file:
        if not chunks:
            continue
        all_chunks.extend(chunks)
        blocks.append(f"## {_rel_path(file_path, root)}\n{_format_chunks(chunks, root)}")
    joined = "\n\n===\n\n".join(blocks)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize each Python module in one sentence based on its representative chunks."),
        ("human",
         "Per-module chunks:\n\n{blocks}\n\n"
         "For each module, return `name` (the relative file path exactly as shown) "
         "and `description` (one sentence)."),
    ])
    result = (prompt | LLM.with_structured_output(ArchitectureOutput, method="function_calling")).invoke({"blocks": joined})
    return all_chunks, result


def run_incomplete_agent(root: str | None) -> tuple[List[dict], IncompleteOutput]:
    matches = [c for c in embedder._chunks if _is_stub(c)]
    if not matches:
        return [], IncompleteOutput(incomplete_features=[])

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You receive code chunks that look incomplete (TODO/FIXME/NotImplementedError/empty pass bodies). "
         "Describe each as a short, user-readable feature gap."),
        ("human",
         "Suspect chunks:\n\n{chunks}\n\n"
         "Return `incomplete_features` as a list of short strings, one per gap."),
    ])
    result = (prompt | LLM.with_structured_output(IncompleteOutput, method="function_calling")).invoke(
        {"chunks": _format_chunks(matches, root)}
    )
    return matches, result


def generate_report(symbol_map: dict | None = None, root: str | None = None) -> ReportJSON:
    seed_chunks, purpose = _purpose_step(root)
    arch_chunks, architecture = _architecture_step(root)
    inc_chunks, incomplete = run_incomplete_agent(root)
    dependency_graph = build_mermaid_graph(symbol_map or {})

    def _to_citations(chunks: List[dict]) -> List[dict]:
        return [
            {
                "file_path": _rel_path(chunk.get("file_path", ""), root),
                "name": chunk.get("name", ""),
                "kind": chunk.get("kind", ""),
                "source": chunk.get("source", "")[:300],
            }
            for chunk in chunks
        ]

    module_file_map = {
        _rel_path(c["file_path"], root): _rel_path(c["file_path"], root)
        for c in arch_chunks
        if c.get("file_path")
    }
    modules = []
    for m in architecture.modules:
        d = asdict(m) if hasattr(m, "__dataclass_fields__") else m.model_dump()
        d["file_path"] = module_file_map.get(d["name"], d["name"])
        modules.append(d)

    print(f"arch_chunks count: {len(arch_chunks)}")
    print(f"arch_chunks file_paths (raw): {[c.get('file_path') for c in arch_chunks[:5]]}")
    print(f"arch_chunks file_paths (rel): {[_rel_path(c.get('file_path',''), root) for c in arch_chunks[:5]]}")
    print(f"module_file_map keys: {list(module_file_map.keys())[:10]}")
    print(f"module names from LLM: {[m['name'] for m in modules]}")
    print(f"file_path values after mapping: {[m['file_path'] for m in modules]}")

    return ReportJSON(
        purpose=purpose.purpose,
        one_liner=purpose.one_liner,
        modules=modules,
        incomplete_features=list(incomplete.incomplete_features),
        dependency_graph=dependency_graph,
        purpose_citations=_to_citations(seed_chunks),
        module_citations=_to_citations(arch_chunks),
        incomplete_citations=_to_citations(inc_chunks),
    )


def generate_report_multi_agent(
    state: dict, symbol_map: dict | None = None, root: str | None = None
) -> ReportJSON:
    purpose_out = state.get("purpose")
    purpose = purpose_out.purpose if purpose_out else ""
    one_liner = purpose_out.one_liner if purpose_out else ""

    architect = state.get("architect", {})
    core_classes = architect.get("core_classes", [])
    modules = [
        {
            "name": c["name"] if isinstance(c, dict) else c.name,
            "description": c["responsibility"] if isinstance(c, dict) else c.responsibility,
            "file_path": _rel_path(
                c["file_path"] if isinstance(c, dict) else c.file_path,
                root
            ),
        }
        for c in core_classes
    ]

    incomplete_out = state.get("incomplete")
    incomplete_features = (
        list(incomplete_out.incomplete_features)
        if hasattr(incomplete_out, "incomplete_features")
        else incomplete_out.get("incomplete_features", [])
        if incomplete_out else []
    )

    purpose_chunks = state.get("purpose_chunks", [])
    incomplete_chunks = state.get("incomplete_chunks", [])

    def _to_citations(chunks: List[dict]) -> List[dict]:
        return [
            {
                "file_path": _rel_path(chunk.get("file_path", ""), root),
                "name": chunk.get("name", ""),
                "kind": chunk.get("kind", ""),
                "source": chunk.get("source", "")[:300],
            }
            for chunk in chunks
        ]

    # TODO: architect_chunks are not currently stored in state; once the
    # architect node persists them, populate module_citations here.
    module_citations: List[dict] = []

    return ReportJSON(
        purpose=purpose,
        one_liner=one_liner,
        modules=modules,
        incomplete_features=incomplete_features,
        dependency_graph=build_mermaid_graph(symbol_map or {}),
        purpose_citations=_to_citations(purpose_chunks),
        module_citations=module_citations,
        incomplete_citations=_to_citations(incomplete_chunks),
    )


def generate_readme(root: str | None = None) -> str:
    from langchain_core.output_parsers import StrOutputParser
    local_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=4096)

    seed_chunks, purpose = _purpose_step(root)
    _, architecture = _architecture_step(root)
    _, incomplete = run_incomplete_agent(root)

    modules_text = "\n".join(
        f"- **{m.name}**: {m.description}" for m in architecture.modules
    )
    gaps_text = "\n".join(
        f"- {f}" for f in incomplete.incomplete_features
    ) or "None identified."

    prompt_part1 = ChatPromptTemplate.from_messages([
        ("system",
         "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Write exactly two sections of a README.md:\n\n"
         "## Overview\n"
         "Write 2-3 sentences expanding on this purpose:\n{purpose}\n\n"
         "## Modules\n"
         "Write each of these as a bullet with name bolded and description after colon:\n{modules}\n\n"
         "Output only these two sections. Start with ## Overview."),
    ])
    part1 = (prompt_part1 | local_llm | StrOutputParser()).invoke({
        "purpose": purpose.purpose,
        "modules": modules_text,
    })

    prompt_part2 = ChatPromptTemplate.from_messages([
        ("system",
         "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Write exactly two sections of a README.md:\n\n"
         "## Known Gaps\n"
         "Write each of these as a bullet:\n{gaps}\n\n"
         "## Getting Started\n"
         "Write exactly: TODO: fill in setup instructions\n\n"
         "Output only these two sections. Start with ## Known Gaps."),
    ])
    part2 = (prompt_part2 | local_llm | StrOutputParser()).invoke({
        "gaps": gaps_text,
    })

    def _strip_fence(s: str) -> str:
        s = s.strip()
        lines = s.split('\n')
        if lines and lines[0].strip().startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        return '\n'.join(lines).strip()

    part1 = _strip_fence(part1)
    part2 = _strip_fence(part2)

    result = f"# {purpose.one_liner}\n\n{part1.strip()}\n\n{part2.strip()}"
    print(f"part1 length: {len(part1)}")
    print(f"part2 length: {len(part2)}")
    print(f"result first 300 chars: {result[:300]}")
    return result
