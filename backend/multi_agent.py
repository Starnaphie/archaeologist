"""Multi-agent analysis graph for codebase exploration.

This module will replace the linear 3-step chain in agent.py with a
LangGraph multi-agent graph, allowing specialized agents to collaborate
and pass intermediate state between one another. Each agent owns a
distinct slice of the analysis and contributes structured output to the
final report.

Planned agents:
    - historian: reconstructs the project's intent and evolution from
      representative code chunks.
    - architect: maps modules, boundaries, and dependencies.
    - Q&A: answers targeted questions about the codebase using
      retrieval over the embedded chunks.
    - evaluator: critiques and validates the other agents' outputs
      before they are returned to the user.
"""

from typing import Any, List, TypedDict

import git
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from . import embedder
from .agent import _purpose_step, run_incomplete_agent


LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class CommitEntry(BaseModel):
    commit: str
    message: str
    files_changed: List[str]


class HistorianOutput(BaseModel):
    timeline: List[CommitEntry]
    first_commit_summary: str
    last_active_area: str


class CoreClass(BaseModel):
    name: str
    file_path: str
    responsibility: str


class ConfigItem(BaseModel):
    name: str
    description: str


class ArchitectOutput(BaseModel):
    entry_points: List[str]
    core_classes: List[CoreClass]
    config_surface: List[ConfigItem]


def _collect_commits(repo_path: str, limit: int = 20) -> List[dict]:
    repo = git.Repo(repo_path)
    raw: List[dict] = []
    try:
        for commit in repo.iter_commits(max_count=limit):
            files = [f for f in commit.stats.files.keys() if f.endswith(".py")]
            raw.append({
                "commit": commit.hexsha[:8],
                "message": commit.message.strip(),
                "files_changed": files,
            })
    except git.exc.GitCommandError:
        print("WARNING: could not read full commit history (shallow clone)")
    return raw


def _format_commits(commits: List[dict]) -> str:
    blocks = []
    for c in commits:
        files = "\n".join(f"  - {f}" for f in c["files_changed"]) or "  (no .py files)"
        blocks.append(f"{c['commit']}: {c['message']}\n{files}")
    return "\n\n".join(blocks)


def run_historian_agent(manifest: dict, root: str) -> dict:
    """
    Walks commit history to build a timeline of the repo's evolution.
    Returns: {timeline, first_commit_summary, last_active_area}.
    """
    raw_commits = _collect_commits(manifest["temp_dir"], limit=20)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a software historian. Given a list of recent commits and the "
         "Python files they touched, reconstruct the project's evolution."),
        ("human",
         "Recent commits (newest first):\n\n{commits}\n\n"
         "Return three things:\n"
         "- `timeline`: the full list of commits, each with `commit`, `message`, "
         "and `files_changed` preserved exactly as given.\n"
         "- `first_commit_summary`: one sentence describing what the project "
         "looked like at the earliest commit shown.\n"
         "- `last_active_area`: a short string naming the module or area "
         "touched most recently."),
    ])
    result = (prompt | LLM.with_structured_output(HistorianOutput)).invoke(
        {"commits": _format_commits(raw_commits)}
    )
    return result.model_dump()


def _format_chunks(chunks: List[dict]) -> str:
    return "\n\n---\n\n".join(
        f"# {c.get('file_path', '')} :: {c.get('kind')} {c.get('name')}\n{c.get('source', '')}"
        for c in chunks
    )


def run_architect_agent(root: str) -> dict:
    """
    Identifies entry points, core classes, and config surface by
    running three targeted retrievals against the FAISS index
    ("entry point main", "class definitions", "configuration settings"),
    merging the results, and asking gpt-4o-mini to extract structure.
    Returns: {entry_points, core_classes, config_surface}.
    """
    queries = ["entry point main", "class definitions", "configuration settings"]
    merged: dict[tuple, dict] = {}
    for q in queries:
        for chunk in embedder.retrieve(q, k=10):
            key = (chunk.get("file_path"), chunk.get("name"))
            if key not in merged:
                merged[key] = chunk

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a software architect. From the representative code chunks, "
         "identify the project's entry points, core classes, and configuration "
         "surface."),
        ("human",
         "Representative chunks:\n\n{chunks}\n\n"
         "Return three things:\n"
         "- `entry_points`: list of file paths that look like entry points "
         "(e.g. main, CLI, server bootstrap).\n"
         "- `core_classes`: list of objects with `name`, `file_path`, and a "
         "one-sentence `responsibility`.\n"
         "- `config_surface`: list of objects with `name` and `description` "
         "for config variables or environment variables the project exposes."),
    ])
    result = (prompt | LLM.with_structured_output(ArchitectOutput)).invoke(
        {"chunks": _format_chunks(list(merged.values()))}
    )
    return result.model_dump()


class AgentGraphState(TypedDict, total=False):
    manifest: dict
    root: str
    purpose_chunks: List[dict]
    purpose: Any
    historian: dict
    architect: dict
    incomplete_chunks: List[dict]
    incomplete: Any


def _purpose_node(state: AgentGraphState) -> dict:
    chunks, purpose = _purpose_step(state.get("root"))
    return {"purpose_chunks": chunks, "purpose": purpose}


def _historian_node(state: AgentGraphState) -> dict:
    result = run_historian_agent(state["manifest"], state.get("root", ""))
    return {"historian": result}


def _architect_node(state: AgentGraphState) -> dict:
    result = run_architect_agent(state.get("root", ""))
    return {"architect": result}


def _incomplete_node(state: AgentGraphState) -> dict:
    chunks, incomplete = run_incomplete_agent(state.get("root"))
    return {"incomplete_chunks": chunks, "incomplete": incomplete}


def build_agent_graph():
    graph = StateGraph(AgentGraphState)
    graph.add_node("purpose", _purpose_node)
    graph.add_node("historian", _historian_node)
    graph.add_node("architect", _architect_node)
    graph.add_node("incomplete", _incomplete_node)
    graph.add_edge(START, "purpose")
    graph.add_edge("purpose", "historian")
    graph.add_edge("historian", "architect")
    graph.add_edge("architect", "incomplete")
    graph.add_edge("incomplete", END)
    return graph.compile()


def run_qa_agent(query: str, root: str) -> str:
    """
    Answers a natural language question about the repository.
    Returns a plain string answer with cited file paths.
    Planned: will use a LangChain conversational chain with FAISS
    retrieval and memory.
    """
    raise NotImplementedError("Q&A agent not yet implemented")


def evaluate_repo(repo_url: str, rubric: dict) -> dict:
    """
    Critiques and validates the other agents' outputs before they
    are returned to the user.
    Returns: {scores, summary, recommendation}.
    Planned: will inspect the historian, architect, and incomplete
    agent results and ask gpt-4o-mini to flag inconsistencies,
    weak claims, or missing evidence.
    """
    raise NotImplementedError("evaluation harness not yet implemented")
