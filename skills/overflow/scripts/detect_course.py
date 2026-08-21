#!/usr/bin/env python3
"""Detect repository type, course signals, project signals, and lesson candidates."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from discover_evidence import discover

EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", ".learning", "dist", "build"}
COURSE_SIGNALS = {
    "DAY_INDEX.md", "CURRICULUM_GUIDE.md", "LESSON_TEMPLATE.md", "LESSON_STANDARD.md",
    "EXERCISE_STANDARD.md", "COURSE_QUALITY_STANDARD.md", "SAFETY_AND_LAB_RULES.md",
}
MANIFEST_NAMES = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Makefile", "Dockerfile"}
SOURCE_DIRS = {"src", "app", "lib", "server", "client", "components", "pages", "cmd", "packages"}
TEST_DIRS = {"test", "tests", "spec", "__tests__"}
DAY_PART_RE = re.compile(r"^(?:(?:0*(\d+))[-_ ]*day|day[-_ ]*0*(\d+))(?:$|[-_ ]|\b)", re.I)
TEST_FILE_RE = re.compile(r"(?:^test_|\.test\.|\.spec\.|_test\.)", re.I)


def files_under(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED for part in path.parts):
            continue
        yield path


def detect_family(names: set[str]) -> list[dict]:
    signals = {
        "javascript-typescript": ["COURSE_QUALITY_STANDARD.md", "LESSON_TEMPLATE.md", "package.json"],
        "python-cybersecurity": ["EXERCISE_STANDARD.md", "SAFETY_AND_LAB_RULES.md", "pyproject.toml"],
        "react-nextjs": ["LESSON_STANDARD.md", "MODERN_TOOLCHAIN.md", "package.json"],
    }
    matches = []
    for family, required in signals.items():
        present = [item for item in required if item in names]
        if present:
            matches.append({"family": family, "score": len(present), "signals": present})
    return sorted(matches, key=lambda item: item["score"], reverse=True)


def lesson_candidates(root: Path):
    candidates = {}
    for path in files_under(root):
        rel_parts = path.relative_to(root).parts
        for index, part in enumerate(rel_parts[:-1]):
            match = DAY_PART_RE.match(part)
            if not match:
                continue
            number = match.group(1) or match.group(2)
            directory = "/".join(rel_parts[: index + 1])
            candidates[(int(number), directory)] = {
                "day": int(number),
                "path": directory,
                "title": part.replace("_", " ").replace("-", " "),
            }
            break
    return sorted(candidates.values(), key=lambda item: (item["day"], item["path"]))


def classify(root: Path, names: set[str], paths: list[Path], lessons: list[dict]) -> str:
    course_markers = len(COURSE_SIGNALS.intersection(names))
    source_markers = sum(1 for path in paths if path.parts and path.parts[0] in SOURCE_DIRS)
    manifest_markers = len(MANIFEST_NAMES.intersection(names))
    project_markers = source_markers + manifest_markers + sum(1 for path in paths if any(part in TEST_DIRS for part in path.parts))
    project_words = sum(1 for name in names if any(word in name.lower() for word in ("project", "capstone", "app")))
    if course_markers >= 2 and len(lessons) >= 3 and project_words:
        return "hybrid"
    if course_markers >= 1 and len(lessons) >= 3:
        return "structured-course"
    if project_markers > 0:
        return "source-project"
    return "sparse"


def project_inventory(root: Path, paths: list[Path]):
    docs = []
    manifests = []
    tests = []
    entry_points = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in {".md", ".rst", ".txt"} and len(docs) < 80:
            docs.append(rel)
        if path.name in MANIFEST_NAMES and len(manifests) < 40:
            manifests.append(rel)
        if any(part in TEST_DIRS for part in path.parts) or TEST_FILE_RE.search(path.name):
            if len(tests) < 80:
                tests.append(rel)
        if path.name in {"main.py", "app.py", "main.ts", "main.tsx", "index.ts", "index.tsx", "main.js", "index.js"}:
            if len(entry_points) < 60:
                entry_points.append(rel)
    return {"documentation": docs, "manifests": manifests, "tests": tests, "entry_points": entry_points}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    paths = list(files_under(root))
    names = {path.name for path in paths}
    lessons = lesson_candidates(root)
    repository_type = classify(root, names, paths, lessons)
    evidence = discover(root, repository_type)
    result = {
        "root": str(root),
        "repository_type": repository_type,
        "families": detect_family(names),
        "signals": sorted(COURSE_SIGNALS.intersection(names)),
        "lessons": lessons,
        "inventory": project_inventory(root, paths),
        "evidence": evidence,
    }
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Root: {root}")
        print(f"Repository type: {result['repository_type']}")
        print("Families:", ", ".join(item["family"] for item in result["families"]) or "unknown")
        print(f"Lesson candidates: {len(result['lessons'])}")
        print(f"Documentation files: {len(result['inventory']['documentation'])}")
        print(f"Test files: {len(result['inventory']['tests'])}")
        print(f"Native evidence sections: {len(result['evidence']['native_sections'])}")
        print(f"Inferred evidence steps: {len(result['evidence']['inferred_evidence'])}")
        for item in result["lessons"][:20]:
            print(f"  Day {item['day']}: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
