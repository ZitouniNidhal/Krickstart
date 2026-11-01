"""Worktree-aware helpers for Krickstart.

Detects Git worktrees and computes per-worktree port offsets and project suffixes
so that multiple checkouts of the same project can run in parallel without
conflicting on host ports or Docker Compose project names.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

DEFAULT_PORT_OFFSET = 100


def is_git_worktree(path: Path | None = None) -> bool:
    """Return True if the specified path is inside a Git worktree."""
    root = path or Path.cwd()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def worktree_hash(path: Path | None = None, length: int = 6) -> str:
    """Return a short stable hash of the worktree's absolute path."""
    root = (path or Path.cwd()).resolve()
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()
    return digest[:length]


def worktree_port_offset(path: Path | None = None, step: int = DEFAULT_PORT_OFFSET) -> int:
    """Return a deterministic port offset based on the worktree path.

    Each worktree gets a multiple of ``step`` derived from its short hash,
    so that N parallel checkouts land on different port ranges.
    """
    root = (path or Path.cwd()).resolve()
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()
    return (int(digest, 16) % 40) * step


def worktree_project_suffix(path: Path | None = None, length: int = 6) -> str:
    """Return a short suffix derived from the worktree's path hash."""
    return worktree_hash(path, length=length)
