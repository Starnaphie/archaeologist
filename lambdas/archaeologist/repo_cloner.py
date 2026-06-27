"""Repo cloning utility for the archaeologist Lambda. Clones remote repos to /tmp for analysis then cleans up after the handler completes. Pass a local path instead of a URL to skip cloning during local testing."""

import os
import shutil
import subprocess
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


def is_url(source: str) -> bool:
    return source.startswith(("https://", "http://", "git@"))


def clone_repo(source: str, dest_dir: str) -> str:
    if not is_url(source):
        if not os.path.isdir(source):
            raise ValueError(f"Local repo path does not exist: {source}")
        return source

    clone_path = os.path.join(dest_dir, "repo")
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    result = subprocess.run(
        ["git", "clone", "--depth", "1", source, clone_path],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed: {result.stderr.strip()}")

    logger.info(f"Cloned {source} to {clone_path}")
    return clone_path


def cleanup_repo(clone_path: str, source: str) -> None:
    if is_url(source) and os.path.exists(clone_path):
        shutil.rmtree(clone_path, ignore_errors=True)
        logger.info(f"Cleaned up {clone_path}")
