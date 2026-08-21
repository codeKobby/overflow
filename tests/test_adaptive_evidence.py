from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "shared" / "scripts" / "discover_evidence.py"


def load_module():
    spec = importlib.util.spec_from_file_location("overflow_discover_evidence", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load discover_evidence.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AdaptiveEvidenceTests(unittest.TestCase):
    def test_native_sections_keep_roles_and_source_provenance(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "lesson.md").write_text(
                """# Lesson\n\n## Practice\n\nImplement it.\n\n## Prove it\n\nExplain it in your own words.\n\n## Finish line\n\nYou are done when you can repair it.\n""",
                encoding="utf-8",
            )
            result = module.discover(root, "structured-course")
            roles = {role for item in result["native_sections"] for role in item["role"]}
            self.assertTrue({"practice", "proof", "verification", "finish"}.issubset(roles))
            self.assertEqual(result["inferred_evidence"], [])
            self.assertTrue(all(item["source_kind"] == "native" for item in result["native_sections"]))

    def test_source_project_gets_labelled_inferred_evidence(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "tests").mkdir()
            (root / "src" / "parser.py").write_text("def parse(value):\n    return value\n", encoding="utf-8")
            (root / "tests" / "test_parser.py").write_text("def test_parse():\n    assert True\n", encoding="utf-8")
            result = module.discover(root, "source-project")
            roles = {item["role"] for item in result["inferred_evidence"]}
            self.assertEqual(roles, {"practice", "proof", "verification", "finish"})
            self.assertTrue(all(item["source_kind"] == "inferred" for item in result["inferred_evidence"]))
            self.assertTrue(all(item["anchors"] for item in result["inferred_evidence"]))


if __name__ == "__main__":
    unittest.main()
