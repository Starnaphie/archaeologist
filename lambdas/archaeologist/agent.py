import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import List

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from openai import OpenAI
    from pydantic import BaseModel
except ModuleNotFoundError:
    if __name__ != "__main__":
        raise
    ChatPromptTemplate = None
    ChatOpenAI = None
    OpenAI = None

    class BaseModel:
        pass

try:
    from . import embedder
except ModuleNotFoundError:
    if __name__ != "__main__":
        raise

    class _EmbedderStub:
        _chunks = []

        @staticmethod
        def retrieve(*args, **kwargs):
            raise RuntimeError("embedder dependencies are not installed")

    embedder = _EmbedderStub()


logger = logging.getLogger(__name__)


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

LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0) if ChatOpenAI else None

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
    repo_owner: dict = field(
        default_factory=lambda: {"owner": None, "repo_name": None, "source": "unknown"}
    )
    setup_instructions: dict = field(
        default_factory=lambda: {"setup_markdown": "", "files_used": [], "skipped": True}
    )
    folder_hierarchy: dict = field(
        default_factory=lambda: {"folders": [], "root_files": []}
    )
    was_chunked: bool = False


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


def _architecture_batch(file_paths: list[str], root: str | None) -> tuple[List[dict], ArchitectureOutput]:
    per_file: List[tuple[str, List[dict]]] = [
        (fp, _chunks_for_file(fp, 3)) for fp in file_paths
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


def _architecture_step(root: str | None) -> tuple[List[dict], ArchitectureOutput, bool]:
    unique_files = list(dict.fromkeys(
        c["file_path"] for c in embedder._chunks
    ))
    if len(unique_files) <= 40:
        chunks, result = _architecture_batch(unique_files, root)
        return chunks, result, False

    merged_chunks = []
    merged_modules = []
    seen_names = set()
    for i in range(0, len(unique_files), 20):
        batch_files = unique_files[i:i + 20]
        batch_chunks, batch_result = _architecture_batch(batch_files, root)
        merged_chunks.extend(batch_chunks)
        for module in batch_result.modules:
            name = module.get("name") if isinstance(module, dict) else module.name
            if name in seen_names:
                continue
            seen_names.add(name)
            merged_modules.append(module)

    return merged_chunks, ArchitectureOutput(modules=merged_modules), True


def _meta_summarize_architecture(modules: list[dict], root: str | None) -> list[dict]:
    if len(modules) <= 15:
        return modules

    prompt_block = "\n".join(
        f"Module: {module.get('name', '')}\nDescription: {module.get('description', '')}\n"
        for module in modules
    )
    try:
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=768,
            messages=[
                {
                    "role": "system",
                    "content": "You are analyzing a large software repository. Return raw JSON only — no markdown fences.",
                },
                {
                    "role": "user",
                    "content": (
                        "This is a large codebase with many modules. Given this full module list, identify the 5-8 most architecturally significant modules — the ones a new developer must understand first to navigate the codebase.\n\n"
                        "For the remaining modules, group them into a single entry:\n"
                        "  name: 'Supporting modules'\n"
                        "  description: a single sentence summarizing what the remaining modules collectively do.\n\n"
                        "Return a JSON array of objects with 'name' and 'description'. The most significant modules come first. 'Supporting modules' is always last.\n\n"
                        f"Full module list:\n{prompt_block}"
                    ),
                },
            ],
        )
        raw = (response.choices[0].message.content or "").strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0]
        parsed = json.loads(raw.strip())
        if not isinstance(parsed, list):
            return modules
        condensed = [
            {"name": item["name"], "description": item["description"]}
            for item in parsed
            if isinstance(item, dict) and "name" in item and "description" in item
        ]
        return condensed or modules
    except Exception:
        return modules


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


# Parses .git/config to extract GitHub owner and repo name. Handles HTTPS and SSH remote URL formats.
def detect_repo_owner(root: str) -> dict:
    default = {"owner": None, "repo_name": None, "source": "unknown"}
    git_config_path = os.path.join(root, ".git", "config")
    if not os.path.exists(git_config_path):
        return default

    with open(git_config_path, "r", encoding="utf-8") as f:
        config_text = f.read()

    origin_match = re.search(
        r'^\s*\[remote\s+"origin"\]\s*$(.*?)(?=^\s*\[|\Z)',
        config_text,
        re.MULTILINE | re.DOTALL,
    )
    if not origin_match:
        return default

    url_match = re.search(r"^\s*url\s*=\s*(.+?)\s*$", origin_match.group(1), re.MULTILINE)
    if not url_match:
        return default

    url = url_match.group(1).strip()
    https_match = re.match(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if https_match:
        return {
            "owner": https_match.group(1),
            "repo_name": https_match.group(2).removesuffix(".git"),
            "source": "github-https",
        }

    if url.startswith("git@github.com:"):
        path = url.split(":", 1)[1]
        parts = path.split("/")
        if len(parts) >= 2:
            return {
                "owner": parts[0],
                "repo_name": parts[1].removesuffix(".git"),
                "source": "github-ssh",
            }

    return {"owner": None, "repo_name": None, "source": "non-github-remote"}


def _scan_setup_files(root: str) -> dict[str, str]:
    high_priority = {
        ".env.example",
        "start.sh",
        "deploy.md",
        "deployment.md",
        "docker-compose.yml",
        "docker-compose.yaml",
        "makefile",
    }
    standard_priority = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "dockerfile",
        "setup.py",
        "setup.cfg",
        ".nvmrc",
        ".python-version",
    }
    skip_dirs = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".tox",
        "dist",
        "build",
        "cdk.out",
    }

    if not root or not os.path.exists(root):
        return {}

    results: dict[str, str] = {}
    total_chars = 0
    truncated = False

    def _read_file(file_path: str) -> str | None:
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return "\n".join(line.rstrip("\n") for _, line in zip(range(200), f))
        except OSError:
            return None

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in skip_dirs]
        for filename in filenames:
            if filename.lower() not in high_priority:
                continue

            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root)
            content = _read_file(file_path)
            if content is None:
                continue

            if len(content) > 3000:
                content = content[:3000].rstrip() + "\n# ... truncated"

            results[rel_path] = content
            total_chars += len(content)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in skip_dirs]
        for filename in filenames:
            if filename.lower() not in standard_priority:
                continue

            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root)
            if rel_path in results:
                continue

            content = _read_file(file_path)
            if content is None:
                continue

            if total_chars + len(content) > 12000:
                truncated = True
                continue

            results[rel_path] = content
            total_chars += len(content)

    if truncated:
        results["_truncated"] = "# truncated — too many setup files"

    return results


# ── Setup extraction ───────────────────────────────────────────────────────
# Two implementations kept intentionally for eval comparison:
#   _extract_setup_single_pass  — baseline: config files only, single LLM call
#   extract_setup_instructions  — production: two-pass with README validation
# To benchmark both, call each independently in eval_archaeologist.py.
def _extract_setup_single_pass(root: str) -> dict:
    """Single-pass setup extraction from config files only. Kept as eval baseline — do not call from generate_report directly."""
    if root is None:
        return {"setup_markdown": "", "files_used": [], "skipped": True}

    file_contents = _scan_setup_files(root)
    readme_names = {"readme.md", "readme.rst", "readme.txt", "readme"}
    config_files = {
        rel_path: content
        for rel_path, content in file_contents.items()
        if rel_path != "_truncated"
        and os.path.basename(rel_path).lower() not in readme_names
    }
    if not config_files:
        return {
            "setup_markdown": "No setup files found in repo.",
            "files_used": [],
            "skipped": False,
        }

    context_string = "\n---\n".join(
        f"### {rel_path}\n{content}\n"
        for rel_path, content in config_files.items()
    )
    files_used = list(config_files.keys())

    try:
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer. Return raw markdown only — no code fences wrapping the entire response.",
                },
                {
                    "role": "user",
                    "content": (
                        "Given these project files, write a concise setup guide with exactly these four sections in order:\n"
                        "## Prerequisites\n## Installation\n## Environment Variables\n## How to Run\n\n"
                        "Rules:\n"
                        "- Use actual package names, commands, and env var names found in the files.\n"
                        "- If a section has no information, write exactly: 'Not found in repo.'\n"
                        "- Be specific and brief. No filler sentences.\n\n"
                        f"Files:\n{context_string}"
                    ),
                },
            ],
        )
        response_text = response.choices[0].message.content or ""

        response_text = response_text.strip()
        lines = response_text.split("\n")
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned_response_text = "\n".join(lines).strip()

        return {
            "setup_markdown": cleaned_response_text,
            "files_used": files_used,
            "skipped": False,
        }
    except Exception as e:
        return {
            "setup_markdown": f"Setup extraction failed: {str(e)}",
            "files_used": files_used,
            "skipped": False,
        }


def extract_setup_instructions(root: str) -> dict:
    """Two-pass setup extraction. Pass 1 derives ground truth from config files only. Pass 2 compares against the README and either adopts README language where correct or prepends a disclaimer listing specific inaccuracies."""
    if root is None:
        return {"setup_markdown": "", "files_used": [], "skipped": True}

    file_contents = _scan_setup_files(root)
    readme_names = {"readme.md", "readme.rst", "readme.txt", "readme"}
    readme_files = {}
    if root and os.path.isdir(root):
        for filename in os.listdir(root):
            if filename.lower() in readme_names:
                readme_path = os.path.join(root, filename)
                try:
                    with open(readme_path, "r", encoding="utf-8", errors="replace") as f:
                        content = "\n".join(line.rstrip("\n") for _, line in zip(range(300), f))
                    readme_files[filename] = content
                except OSError:
                    pass
    config_files = {
        rel_path: content
        for rel_path, content in file_contents.items()
        if rel_path != "_truncated"
    }
    files_used = list(config_files.keys()) + list(readme_files.keys())
    ground_truth_md = None

    if not config_files and not readme_files:
        return {
            "setup_markdown": "No setup files found in repo.",
            "files_used": [],
            "skipped": False,
        }

    try:
        config_context = "\n---\n".join(
            f"### {rel_path}\n{content}\n"
            for rel_path, content in config_files.items()
        )
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer. Return raw markdown only — no code fences wrapping the entire response.",
                },
                {
                    "role": "user",
                    "content": (
                        "Extract setup instructions from these project config files. Write a setup guide with exactly these five sections:\n"
                        "## Prerequisites\n## Installation\n## Environment Variables\n## How to Run\n## Deployment\n\n"
                        "Rules:\n"
                        "- Use only what is explicitly present in the files. Do not infer or invent.\n"
                        "- Write each section in clean prose or concise steps with no inline citations.\n"
                        "- At the end of each section, add a line: '**Key files:** file1, file2' listing only the source files that contributed information to that section. Omit this line if no files were used.\n"
                        "- Summarize where possible:\n"
                        "  - If multiple requirements.txt files exist across subdirectories, write one instruction covering the pattern rather than listing every file individually.\n"
                        "  - For Environment Variables: ONLY include content if actual environment variable names (e.g. OPENAI_API_KEY, PIPELINE_BUCKET) are explicitly defined in the scanned files. If a .env.example file was not scanned or contains no variable definitions, write exactly: 'Not found in repo.' Do not mention .env.example or .env files unless they were present in the scanned config files and contained real variable names.\n"
                        "  - For deployment: if a DEPLOY.md or similar file is present, write 'See [filename] for full deployment instructions.' followed by a one-line summary of the deploy process.\n"
                        "- If a section has no information, write exactly: 'Not found in repo.'\n\n"
                        f"Config files:\n{config_context}"
                    ),
                },
            ],
        )
        ground_truth_md = response.choices[0].message.content or ""
        ground_truth_md = ground_truth_md.strip()
        if ground_truth_md.startswith("```"):
            ground_truth_md = ground_truth_md.split("\n", 1)[1]
            ground_truth_md = ground_truth_md.rsplit("```", 1)[0]
        ground_truth_md = ground_truth_md.strip()

        if not readme_files:
            return {
                "setup_markdown": ground_truth_md,
                "files_used": files_used,
                "skipped": False,
            }

        readme_context = "\n---\n".join(
            f"### {rel_path}\n{content}\n"
            for rel_path, content in readme_files.items()
        )
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1536,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical writer auditing documentation accuracy. Return raw markdown only.",
                },
                {
                    "role": "user",
                    "content": (
                        "Compare these two sources of setup information and produce a final setup guide.\n\n"
                        "THE CODE (ground truth with key file citations):\n"
                        f"{ground_truth_md}\n\n"
                        "THE README:\n"
                        f"{readme_context}\n\n"
                        "Rules:\n"
                        "1. For each section, if the README is correct and more detailed → use README language.\n"
                        "2. If the README contradicts the code or references something with no matching citation in the code → use the code's version instead.\n"
                        "3. Do not add any new information not already present in one of the two sources.\n"
                        "4. Scan the README for issues that would cause a developer to FAIL when setting up the project. Only flag issues that are actionable and consequential:\n"
                        "   Flag: credentials or API keys for integrations whose packages are absent from all requirements files, wrong or removed commands, dependencies that no longer exist in any requirements file, broken or outdated URLs that are load-bearing for setup.\n"
                        "   Do NOT flag: spelling differences, minor wording variations, cosmetic formatting differences, missing version numbers, extra context the README provides that the code does not contradict.\n"
                        "   If in doubt, do not flag it — only surface issues a developer would actually hit.\n"
                        "5. If ANY issues are found, prepend the entire response with:\n\n"
                        "> ⚠️ **README accuracy issues detected:**\n"
                        "> - [Section or 'General']: [issue — for removed tools/credentials name them explicitly; for version mismatches write 'dependency versions may differ from README']\n\n"
                        "6. If the README is fully accurate, output no disclaimer.\n\n"
                        "Output the final guide with these five sections (and README issues as needed):\n"
                        "## Prerequisites\n## Installation\n## Environment Variables\n## How to Run\n## Deployment\n\n"
                        "Keep the '**Key files:**' lines from the code source at the bottom of each section unchanged"
                    ),
                },
            ],
        )
        final_md = response.choices[0].message.content or ""
        final_md = final_md.strip()
        if final_md.startswith("```"):
            final_md = final_md.split("\n", 1)[1]
            final_md = final_md.rsplit("```", 1)[0]
        final_md = final_md.strip()
        return {
            "setup_markdown": final_md,
            "files_used": files_used,
            "skipped": False,
        }
    except Exception as e:
        if ground_truth_md is not None:
            return {
                "setup_markdown": ground_truth_md,
                "files_used": files_used,
                "skipped": False,
            }
        return {
            "setup_markdown": f"Setup extraction failed: {str(e)}",
            "files_used": files_used if "files_used" in locals() else [],
            "skipped": False,
        }


def _walk_folder_structure(root: str) -> dict:
    if root is None or not os.path.isdir(root):
        return {"folders": [], "root_files": []}

    skip_dirs = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".tox",
        "dist",
        "build",
        "cdk.out",
        "logs",
        "transcripts",
        ".claude",
    }
    sample_priority = [
        "__init__.py",
        "handler.py",
        "main.py",
        "agent.py",
        "index.ts",
        "index.js",
        "app.py",
        "README.md",
        "SKILL.md",
    ]
    root_file_extensions = {".sh", ".md", ".toml", ".yml", ".yaml", ".json", ".txt", ".py", ""}
    setup_files_already_covered = {"requirements.txt", "dockerfile", ".env.example", "package.json", "pyproject.toml"}

    def _read_lines(path: str, max_lines: int) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return "\n".join(line.rstrip("\n") for _, line in zip(range(max_lines), f))
        except OSError:
            return ""

    def _level_for(path: str) -> int:
        rel_path = os.path.relpath(path, root)
        if rel_path == ".":
            return 0
        return len(rel_path.split(os.sep))

    folders = []
    root_files = []

    for filename in os.listdir(root):
        if len(root_files) >= 8:
            break
        filepath = os.path.join(root, filename)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(filename)[1].lower()
        if ext not in root_file_extensions:
            continue
        if ext == "" and filename not in {"Makefile", "Dockerfile", "Procfile"} and not os.access(filepath, os.X_OK):
            continue
        if filename.lower() in setup_files_already_covered:
            continue
        root_files.append({
            "path": filename,
            "first_lines": _read_lines(filepath, 20),
        })

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [dirname for dirname in dirnames if dirname not in skip_dirs]
        level = _level_for(dirpath)
        if level >= 3:
            dirnames[:] = []
        if level == 0:
            continue
        if level > 3:
            continue

        selected = []
        remaining = set(filenames)
        for priority_name in sample_priority:
            if priority_name in remaining and len(selected) < 3:
                selected.append(priority_name)
                remaining.remove(priority_name)
        if len(selected) < 3:
            for filename in filenames:
                if filename in selected:
                    continue
                _, ext = os.path.splitext(filename)
                if ext.lower() in {".py", ".ts", ".js"}:
                    selected.append(filename)
                    if len(selected) >= 3:
                        break

        sample_files = []
        for filename in selected:
            file_path = os.path.join(dirpath, filename)
            sample_files.append({
                "name": filename,
                "preview": _read_lines(file_path, 30),
            })

        folders.append({
            "path": os.path.relpath(dirpath, root),
            "level": level,
            "sample_files": sample_files,
        })

    return {"folders": folders, "root_files": root_files}


def build_folder_hierarchy(root: str) -> dict:
    if root is None or not os.path.isdir(root):
        return {"folders": [], "root_files": []}

    structure = _walk_folder_structure(root)
    folders = structure.get("folders", [])
    root_files = structure.get("root_files", [])
    if not folders and not root_files:
        return {"folders": [], "root_files": []}

    def _strip_json_fences(raw: str) -> str:
        text = (raw or "").strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return text.strip()

    def _folder_prompt_block(batch: list[dict]) -> str:
        blocks = []
        for folder in batch:
            lines = [f"Folder: {folder.get('path', '')}"]
            for sample_file in folder.get("sample_files", []):
                lines.append(f"  [{sample_file.get('name', '')}]\n{sample_file.get('preview', '')}\n")
            blocks.append("\n".join(lines))
        return "\n---\n".join(blocks)

    folder_descriptions = {}
    for i in range(0, len(folders), 8):
        batch = folders[i:i + 8]
        prompt_block = _folder_prompt_block(batch)
        try:
            response = OpenAI().chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=512,
                messages=[
                    {
                        "role": "system",
                        "content": "You are analyzing a software repository. Return raw JSON only — no markdown fences.",
                    },
                    {
                        "role": "user",
                        "content": (
                            "For each folder below, write a one-sentence description of its role in the project.\n"
                            "Return a JSON array of objects with 'path' (string, exactly as shown) and 'description' (string).\n\n"
                            f"{prompt_block}"
                        ),
                    },
                ],
            )
            raw = response.choices[0].message.content or ""
            parsed = json.loads(_strip_json_fences(raw))
            if not isinstance(parsed, list):
                raise ValueError("folder descriptions response was not a list")
            for item in parsed:
                if isinstance(item, dict) and "path" in item:
                    folder_descriptions[item["path"]] = item.get("description", "")
        except json.JSONDecodeError:
            for folder in batch:
                folder_descriptions[folder.get("path", "")] = "Could not determine folder purpose."
        except Exception:
            for folder in batch:
                folder_descriptions[folder.get("path", "")] = ""

    root_file_descriptions = {}
    if root_files:
        prompt_block = "\n---\n".join(
            f"File: {root_file.get('path', '')}\n{root_file.get('first_lines', '')}\n"
            for root_file in root_files
        )
        try:
            response = OpenAI().chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=256,
                messages=[
                    {
                        "role": "system",
                        "content": "You are analyzing a software repository. Return raw JSON only — no markdown fences.",
                    },
                    {
                        "role": "user",
                        "content": (
                            "For each root-level file below, write a one-line description of its purpose.\n"
                            "Return a JSON array of objects with 'path' and 'description'.\n\n"
                            f"{prompt_block}"
                        ),
                    },
                ],
            )
            raw = response.choices[0].message.content or ""
            parsed = json.loads(_strip_json_fences(raw))
            if not isinstance(parsed, list):
                raise ValueError("root file descriptions response was not a list")
            for item in parsed:
                if isinstance(item, dict) and "path" in item:
                    root_file_descriptions[item["path"]] = item.get("description", "")
        except json.JSONDecodeError:
            for root_file in root_files:
                root_file_descriptions[root_file.get("path", "")] = "See file for details."
        except Exception:
            for root_file in root_files:
                root_file_descriptions[root_file.get("path", "")] = ""

    return {
        "folders": [
            {
                "path": folder.get("path", ""),
                "description": folder_descriptions.get(folder.get("path", ""), ""),
                "level": folder.get("level", 0),
                "children": [],
            }
            for folder in folders
        ],
        "root_files": [
            {
                "path": root_file.get("path", ""),
                "description": root_file_descriptions.get(root_file.get("path", ""), ""),
            }
            for root_file in root_files
        ],
    }


def generate_report(symbol_map: dict | None = None, root: str | None = None) -> ReportJSON:
    seed_chunks, purpose = _purpose_step(root)
    arch_chunks, architecture, was_chunked = _architecture_step(root)
    if was_chunked:
        module_list = [
            m if isinstance(m, dict)
            else m.model_dump() if hasattr(m, "model_dump")
            else asdict(m)
            for m in architecture.modules
        ]
        condensed = _meta_summarize_architecture(module_list, root)
        architecture = ArchitectureOutput(
            modules=[ModuleSummary(name=m["name"], description=m["description"]) for m in condensed]
        )
    inc_chunks, incomplete = run_incomplete_agent(root)
    dependency_graph = build_mermaid_graph(symbol_map or {})
    repo_owner = detect_repo_owner(root) if root else {"owner": None, "repo_name": None, "source": "unknown"}
    logger.info(f"Repo owner: {repo_owner}")
    setup_instructions = extract_setup_instructions(root)
    folder_hierarchy = build_folder_hierarchy(root) if root else {"folders": [], "root_files": []}

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
        repo_owner=repo_owner,
        setup_instructions=setup_instructions,
        folder_hierarchy=folder_hierarchy,
        was_chunked=was_chunked,
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
    repo_owner = detect_repo_owner(root) if root else {"owner": None, "repo_name": None, "source": "unknown"}
    logger.info(f"Repo owner: {repo_owner}")
    setup_instructions = extract_setup_instructions(root)
    folder_hierarchy = build_folder_hierarchy(root) if root else {"folders": [], "root_files": []}
    _, architecture, was_chunked = _architecture_step(root) if root else ([], ArchitectureOutput(modules=[]), False)
    if was_chunked:
        module_list = [
            m if isinstance(m, dict)
            else m.model_dump() if hasattr(m, "model_dump")
            else asdict(m)
            for m in architecture.modules
        ]
        condensed = _meta_summarize_architecture(module_list, root)
        architecture = ArchitectureOutput(
            modules=[ModuleSummary(name=m["name"], description=m["description"]) for m in condensed]
        )
        modules = [
            {
                "name": module.name,
                "description": module.description,
                "file_path": module.name,
            }
            for module in architecture.modules
        ]

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
        repo_owner=repo_owner,
        setup_instructions=setup_instructions,
        folder_hierarchy=folder_hierarchy,
        was_chunked=was_chunked,
    )


def generate_readme(root: str | None = None) -> str:
    from langchain_core.output_parsers import StrOutputParser
    local_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=4096)

    _, purpose_out = _purpose_step(root)
    _, incomplete_out = run_incomplete_agent(root)
    setup_result = extract_setup_instructions(root) if root else {}

    gaps_text = "\n".join(f"- {f}" for f in incomplete_out.incomplete_features) or "None identified."

    setup_md = setup_result.get("setup_markdown", "") if not setup_result.get("skipped") else ""
    if setup_md:
        setup_md_clean = "\n".join(
            line for line in setup_md.split("\n")
            if not line.strip().startswith("**Key files:**")
            and not line.strip().startswith("> ⚠️")
            and not line.strip().startswith("> -")
        ).strip()
    else:
        setup_md_clean = "TODO: fill in setup instructions"

    # Section 1 — Title + description
    # Section 2 — Highlights
    highlights_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Based on this project purpose, write a ## Highlights section for a README.\n\n"
         "Purpose: {purpose}\n\n"
         "Write 4-6 bullet points covering:\n"
         "- What problem does this project solve?\n"
         "- What unique approach or solution does it provide?\n"
         "- What can a user do with it? (concrete capabilities)\n\n"
         "Rules:\n"
         "- Each bullet should be one punchy sentence.\n"
         "- Do not use filler phrases like 'This project...' or 'It allows...'.\n"
         "- Lead each bullet with the capability or outcome, not the implementation.\n\n"
         "Output only the ## Highlights section."),
    ])
    highlights = (highlights_prompt | local_llm | StrOutputParser()).invoke({
        "purpose": purpose_out.purpose,
    })

    # Section 3 — Known holes
    gaps_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Write a ## Known Gaps section for a README.\n\n"
         "Write each of these as a bullet:\n{gaps}\n\n"
         "Output only the ## Known Gaps section. Start with ## Known Gaps."),
    ])
    gaps_section = (gaps_prompt | local_llm | StrOutputParser()).invoke({
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

    highlights = _strip_fence(highlights)
    gaps_section = _strip_fence(gaps_section)

    return (
        f"# {purpose_out.one_liner}\n\n"
        f"{purpose_out.purpose}\n\n"
        f"{highlights}\n\n"
        f"## Setup\n\n{setup_md_clean}\n\n"
        f"{gaps_section}"
    )


def generate_readme_from_report(report_dict: dict) -> str:
    from langchain_core.output_parsers import StrOutputParser
    local_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=4096)

    purpose_text = report_dict.get("purpose", "")
    one_liner = report_dict.get("one_liner", "")
    incomplete_features = report_dict.get("incomplete_features", [])
    setup_instructions = report_dict.get("setup_instructions", {})

    gaps_text = "\n".join(f"- {f}" for f in incomplete_features) or "None identified."

    setup_md = setup_instructions.get("setup_markdown", "") if not setup_instructions.get("skipped") else ""
    if setup_md:
        setup_md_clean = "\n".join(
            line for line in setup_md.split("\n")
            if not line.strip().startswith("**Key files:**")
            and not line.strip().startswith("> ⚠️")
            and not line.strip().startswith("> -")
        ).strip()
    else:
        setup_md_clean = "TODO: fill in setup instructions"

    highlights_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Based on this project purpose, write a ## Highlights section for a README.\n\n"
         "Purpose: {purpose}\n\n"
         "Write 4-6 bullet points covering:\n"
         "- What problem does this project solve?\n"
         "- What unique approach or solution does it provide?\n"
         "- What can a user do with it? (concrete capabilities)\n\n"
         "Rules:\n"
         "- Each bullet should be one punchy sentence.\n"
         "- Do not use filler phrases like 'This project...' or 'It allows...'.\n"
         "- Lead each bullet with the capability or outcome, not the implementation.\n\n"
         "Output only the ## Highlights section."),
    ])
    highlights = (highlights_prompt | local_llm | StrOutputParser()).invoke({
        "purpose": purpose_text,
    })

    gaps_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical writer. Return raw markdown only, no code fences."),
        ("human",
         "Write a ## Known Gaps section for a README.\n\n"
         "Write each of these as a bullet:\n{gaps}\n\n"
         "Output only the ## Known Gaps section. Start with ## Known Gaps."),
    ])
    gaps_section = (gaps_prompt | local_llm | StrOutputParser()).invoke({
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

    highlights = _strip_fence(highlights)
    gaps_section = _strip_fence(gaps_section)

    return (
        f"# {one_liner}\n\n"
        f"{purpose_text}\n\n"
        f"{highlights}\n\n"
        f"## Setup\n\n{setup_md_clean}\n\n"
        f"{gaps_section}"
    )


if __name__ == "__main__":
    repo_owner_result = detect_repo_owner(".")
    assert all(key in repo_owner_result for key in ("owner", "repo_name", "source"))
    print(repo_owner_result)
