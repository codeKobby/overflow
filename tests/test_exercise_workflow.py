from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXERCISE_SCRIPTS = ROOT / "skills" / "exercise" / "scripts"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


scaffold = load("scaffold_exercise", EXERCISE_SCRIPTS / "scaffold_exercise.py")
markers = load("parse_exercise_markers", EXERCISE_SCRIPTS / "parse_exercise_markers.py")
resolver = load("resolve_exercise", EXERCISE_SCRIPTS / "resolve_exercise.py")


class ExerciseWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "practice" / "exercises.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text(
            "# Practice\n\n"
            "1. Return the greeting.\n"
            "2. Handle an empty value.\n"
            "3. Explain the edge case.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_scaffold_creates_manifest_and_stable_ids(self) -> None:
        out = self.root / ".learning" / "exercises" / "day-01"
        prompts, heading = scaffold.extract_prompts(self.source)
        answer_text, regions = scaffold.build_answer_template(prompts, out / "answers.md", None)
        out.mkdir(parents=True)
        (out / "answers.md").write_text(answer_text, encoding="utf-8")
        manifest = scaffold.build_manifest(self.root, self.source, "day-01", heading or "Practice", prompts, regions, out / "answers.md")
        (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        self.assertEqual([item["id"] for item in manifest["questions"]], ["CB-Q01", "CB-Q02", "CB-Q03"])
        self.assertEqual(manifest["active_question"], "CB-Q01")
        self.assertEqual(manifest["questions"][1]["ordinal"], 2)
        self.assertEqual(manifest["questions"][1]["status"], "scaffolded")

    def test_parser_detects_hint_and_answer_state(self) -> None:
        out = self.root / ".learning" / "exercises" / "day-01"
        out.mkdir(parents=True)
        answers = out / "answers.md"
        answers.write_text(
            "<!-- CB-Q01: Return the greeting. -->\n"
            "<!-- CB-HINT-START CB-Q01 level=3 -->\n"
            "<!-- pseudocode: build -> return -->\n"
            "<!-- CB-HINT-END CB-Q01 -->\n"
            "<!-- CB-ANSWER-START CB-Q01 -->\n"
            "def greet(name):\n    return name\n"
            "<!-- CB-ANSWER-END CB-Q01 -->\n"
            "<!-- CB-Q02: Handle an empty value. -->\n"
            "<!-- CB-ANSWER-START CB-Q02 -->\n"
            "<!-- TODO: write your answer here -->\n"
            "<!-- CB-ANSWER-END CB-Q02 -->\n",
            encoding="utf-8",
        )
        result = markers.parse(out)
        regions = {region["id"]: region["status"] for file in result["files"] for region in file["answer_regions"]}
        hints = [hint for file in result["files"] for hint in file["hint_blocks"]]
        self.assertEqual(regions, {"CB-Q01": "contains-content", "CB-Q02": "commented-draft"})
        self.assertEqual(len(hints), 1)
        self.assertEqual(hints[0]["level"], 3)
        self.assertEqual(result["warnings"], [])

    def test_resolver_normalizes_explicit_question(self) -> None:
        out = self.root / ".learning" / "exercises" / "day-01"
        out.mkdir(parents=True)
        manifest = {
            "version": 1,
            "exercise_id": "day-01",
            "active_question": "CB-Q01",
            "questions": [
                {"id": "CB-Q01", "status": "scaffolded"},
                {"id": "CB-Q03", "status": "scaffolded"},
            ],
        }
        (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        active = resolver.resolve(self.root, None, None)
        explicit = resolver.resolve(self.root, "CB-Q003", None)
        self.assertEqual(active["question"]["id"], "CB-Q01")
        self.assertEqual(explicit["question"]["id"], "CB-Q03")


if __name__ == "__main__":
    unittest.main()
