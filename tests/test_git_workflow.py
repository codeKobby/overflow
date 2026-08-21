from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "shared" / "scripts" / "git_workflow.py"


def load_module():
    spec = importlib.util.spec_from_file_location("overflow_git_workflow", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load git_workflow.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return result.stdout.strip()


class GitWorkflowTests(unittest.TestCase):
    def make_repo(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        git(root, "init", "-b", "main")
        git(root, "config", "user.email", "overflow@example.invalid")
        git(root, "config", "user.name", "Overflow Test")
        (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
        git(root, "add", "README.md")
        git(root, "commit", "-m", "fixture")
        return root

    def test_plan_and_apply_branch_records_state(self):
        module = load_module()
        root = self.make_repo()
        proposal = module.plan(root, mode="branch", slug="day-01-q03", branch=None, worktree=None, base=None)
        self.assertEqual(proposal["target_branch"], "overflow/exercise/day-01-q03")
        self.assertTrue(proposal["safe_to_apply"])
        result = module.apply(root, mode="branch", slug="day-01-q03", branch=None, worktree=None, base=None)
        self.assertEqual(result["exercise_branch"], "overflow/exercise/day-01-q03")
        state = json.loads((root / ".learning" / "git-workflow.json").read_text(encoding="utf-8"))
        self.assertEqual(state["base_branch"], "main")
        self.assertEqual(state["exercise_branch"], "overflow/exercise/day-01-q03")
        self.assertEqual(state["mode"], "branch")

    def test_dirty_tree_is_not_safe_to_apply(self):
        module = load_module()
        root = self.make_repo()
        (root / "keep.txt").write_text("preserve\n", encoding="utf-8")
        proposal = module.plan(root, mode="branch", slug="dirty", branch=None, worktree=None, base=None)
        self.assertFalse(proposal["safe_to_apply"])
        with self.assertRaises(RuntimeError):
            module.apply(root, mode="branch", slug="dirty", branch=None, worktree=None, base=None)

    def test_worktree_creation_is_linked_and_isolated(self):
        module = load_module()
        root = self.make_repo()
        worktree = root.parent / "fixture-overflow-worktree"
        self.addCleanup(lambda: subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root, check=False, capture_output=True))
        result = module.apply(root, mode="worktree", slug="parser-basics", branch=None, worktree=str(worktree), base=None)
        self.assertEqual(result["exercise_branch"], "overflow/exercise/parser-basics")
        self.assertTrue(worktree.is_dir())
        self.assertIn("overflow/exercise/parser-basics", git(root, "branch", "--list"))


if __name__ == "__main__":
    unittest.main()
