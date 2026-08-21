#!/usr/bin/env python3
"""Resolve an active overflow exercise question from learner manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

QUESTION_ID_RE = re.compile(r"^CB-Q0*(?P<number>\d+)(?P<suffix>-[A-Za-z0-9][A-Za-z0-9_-]*)?$", re.IGNORECASE)


def normalize_question_id(value: str) -> str:
    match = QUESTION_ID_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid question ID: {value!r}; expected CB-Q01 or CB-Q01-a")
    suffix = match.group("suffix") or ""
    return f"CB-Q{int(match.group('number')):02d}{suffix}"


def manifests(root: Path) -> list[tuple[Path, dict[str, object]]]:
    result: list[tuple[Path, dict[str, object]]] = []
    for path in sorted((root / ".learning" / "exercises").glob("*/manifest.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid exercise manifest {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"exercise manifest must be an object: {path}")
        result.append((path, data))
    return result


def resolve(root: Path, question: str | None, exercise_id: str | None) -> dict[str, object]:
    candidates = manifests(root)
    if exercise_id:
        candidates = [(path, data) for path, data in candidates if data.get("exercise_id") == exercise_id or path.parent.name == exercise_id]
    if not candidates:
        raise ValueError("no matching exercise manifest found under .learning/exercises/")

    normalized = normalize_question_id(question) if question else None
    matches: list[dict[str, object]] = []
    for path, data in candidates:
        questions = data.get("questions", [])
        if not isinstance(questions, list):
            raise ValueError(f"questions must be a list in {path}")
        if normalized:
            for item in questions:
                if isinstance(item, dict) and item.get("id") == normalized:
                    matches.append({"manifest_path": str(path.relative_to(root)), "manifest": data, "question": item})
        else:
            active = data.get("active_question")
            if active:
                for item in questions:
                    if isinstance(item, dict) and item.get("id") == active:
                        matches.append({"manifest_path": str(path.relative_to(root)), "manifest": data, "question": item})
                        break

    if len(matches) == 1:
        return matches[0]
    if not matches:
        if normalized:
            raise ValueError(f"question {normalized} was not found in the matching manifest(s)")
        raise ValueError("no active question is recorded; choose a question explicitly")
    ids = [f"{item['manifest'].get('exercise_id')}:{item['question'].get('id')}" for item in matches]
    raise ValueError("multiple active questions found; choose one explicitly: " + ", ".join(ids))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("question", nargs="?", help="question ID such as CB-Q03")
    parser.add_argument("--exercise", dest="exercise_id", help="exercise ID or directory name")
    args = parser.parse_args()
    try:
        result = resolve(args.root.expanduser().resolve(), args.question, args.exercise_id)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
