from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from krickstart import worktree


class WorktreeTests(unittest.TestCase):
    def test_is_git_worktree_true(self) -> None:
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="true\n")
            self.assertTrue(worktree.is_git_worktree())

    def test_is_git_worktree_false(self) -> None:
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="false\n")
            self.assertFalse(worktree.is_git_worktree())

    def test_is_git_worktree_handles_error(self) -> None:
        with patch("subprocess.run", side_effect=FileNotFoundError):
            self.assertFalse(worktree.is_git_worktree())

    def test_worktree_hash_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir)
            hash1 = worktree.worktree_hash(path)
            hash2 = worktree.worktree_hash(path)
            self.assertEqual(hash1, hash2)
            self.assertEqual(len(hash1), 6)

    def test_worktree_hash_custom_length(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir)
            short_hash = worktree.worktree_hash(path, length=8)
            self.assertEqual(len(short_hash), 8)

    def test_worktree_port_offset_calculation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir)
            offset = worktree.worktree_port_offset(path, step=50)
            self.assertIsInstance(offset, int)
            self.assertEqual(offset % 50, 0)
            self.assertGreaterEqual(offset, 0)
            self.assertLess(offset, 40 * 50)

    def test_worktree_project_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir)
            suffix = worktree.worktree_project_suffix(path)
            self.assertEqual(suffix, worktree.worktree_hash(path))

