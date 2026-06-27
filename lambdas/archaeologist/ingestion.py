import os
import tempfile
from pathlib import Path
from git import Repo

EXCLUDE_SEGMENTS = ("__pycache__", "venv", ".git", "node_modules", "/test")


def _should_skip(path: str) -> bool:
    return any(segment in Path(path).parts for segment in EXCLUDE_SEGMENTS)


def clone_and_manifest(github_url: str) -> dict:
    repo_name = github_url.rstrip("/").split("/")[-1].removesuffix(".git")
    temp_dir = tempfile.mkdtemp(prefix=f"archaeologist_{repo_name}_")

    Repo.clone_from(github_url, temp_dir, depth=1)

    files = []
    for root, dirs, filenames in os.walk(temp_dir):
        dirs[:] = [d for d in dirs if not _should_skip(os.path.join(root, d))]
        for name in filenames:
            if not name.endswith(".py"):
                continue
            full_path = os.path.join(root, name)
            if _should_skip(full_path):
                continue
            files.append(os.path.abspath(full_path))
    print(f"Found {len(files)} .py files: {files[:5]}")

    print(f"temp_dir: {temp_dir}")
    print(f"First 10 files: {files[:10]}")

    return {
        "repo_name": repo_name,
        "temp_dir": temp_dir,
        "files": files,
        "file_count": len(files),
    }
