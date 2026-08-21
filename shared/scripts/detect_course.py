#!/usr/bin/env python3
"""Detect a repository's learning-course signals and lesson candidates."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", ".learning"}
SIGNALS = {
    "javascript-typescript": ["COURSE_QUALITY_STANDARD.md", "LESSON_TEMPLATE.md", "package.json"],
    "python-cybersecurity": ["EXERCISE_STANDARD.md", "SAFETY_AND_LAB_RULES.md", "pyproject.toml"],
    "react-nextjs": ["LESSON_STANDARD.md", "MODERN_TOOLCHAIN.md", "package.json"],
}
DAY_PART_RE = re.compile(r"^(?:(?:0*(\d+))[-_ ]*day|day[-_ ]*0*(\d+))(?:$|[-_ ]|\b)", re.I)


def files_under(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED for part in path.parts):
            continue
        yield path


def detect_family(names: set[str]) -> list[dict]:
    matches = []
    all_signals = {item for values in SIGNALS.values() for item in values}
    for family, required in SIGNALS.items():
        score = sum(name in names for name in required)
        if score:
            matches.append({"family": family, "score": score, "signals": [x for x in required if x in names]})
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    names = {path.name for path in files_under(root)}
    result = {
        "root": str(root),
        "families": detect_family(names),
        "signals": sorted(name for name in names if any(name in values for values in SIGNALS.values())),
        "lessons": lesson_candidates(root),
    }
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Root: {root}")
        print("Families:", ", ".join(item["family"] for item in result["families"]) or "unknown")
        print(f"Lesson candidates: {len(result['lessons'])}")
        for item in result["lessons"][:20]:
            print(f"  Day {item['day']}: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
