from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS_SCRIPT = ROOT / "shared" / "scripts" / "detect_readiness.py"
SKILLS_SCRIPT = ROOT / "shared" / "scripts" / "discover_skills.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RouterReadinessTests(unittest.TestCase):
    def make_root(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def test_missing_learning_state_requires_setup(self):
        module = load_module("overflow_detect_readiness", READINESS_SCRIPT)
        result = module.detect(self.make_root())
        self.assertEqual(result["status"], "uninitialized")
        self.assertFalse(result["ready"])
        self.assertEqual(result["next_action"], "setup")

    def test_draft_state_requires_resume_setup(self):
        module = load_module("overflow_detect_readiness", READINESS_SCRIPT)
        root = self.make_root()
        (root / ".learning").mkdir()
        (root / ".learning" / "CURRICULUM.draft.md").write_text("# Draft\n", encoding="utf-8")
        result = module.detect(root)
        self.assertEqual(result["status"], "draft")
        self.assertEqual(result["next_action"], "resume-setup")
        self.assertIn("CURRICULUM.draft.md", result["draft_files"])

    def test_partial_state_is_not_ready(self):
        module = load_module("overflow_detect_readiness", READINESS_SCRIPT)
        root = self.make_root()
        state = root / ".learning"
        state.mkdir()
        (state / "CONFIG.md").write_text("# Config\n", encoding="utf-8")
        result = module.detect(root)
        self.assertEqual(result["status"], "partial")
        self.assertFalse(result["ready"])
        self.assertIn("MISSION.md", result["missing_files"])

    def test_complete_state_is_ready(self):
        module = load_module("overflow_detect_readiness", READINESS_SCRIPT)
        root = self.make_root()
        state = root / ".learning"
        state.mkdir()
        for filename in module.REQUIRED_FILES:
            (state / filename).write_text("{}\n" if filename == "progress.json" else "# State\n", encoding="utf-8")
        for dirname in module.REQUIRED_DIRS:
            (state / dirname).mkdir()
        result = module.detect(root)
        self.assertEqual(result["status"], "initialized")
        self.assertTrue(result["ready"])
        self.assertEqual(result["next_action"], "continue")

    def test_skill_discovery_reads_project_skill_metadata(self):
        module = load_module("overflow_discover_skills", SKILLS_SCRIPT)
        root = self.make_root()
        skill_file = root / ".agents" / "skills" / "reviewer" / "SKILL.md"
        skill_file.parent.mkdir(parents=True)
        skill_file.write_text(
            "---\nname: reviewer\ndescription: Review code carefully.\n---\n# Reviewer\n",
            encoding="utf-8",
        )
        result = module.discover(root)
        matches = [row for row in result if row["name"] == "reviewer"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["scope"], "project")
        self.assertEqual(matches[0]["host"], "codex")
        self.assertEqual(matches[0]["description"], "Review code carefully.")

    def test_skill_discovery_is_read_only(self):
        module = load_module("overflow_discover_skills", SKILLS_SCRIPT)
        root = self.make_root()
        before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        module.discover(root)
        after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
