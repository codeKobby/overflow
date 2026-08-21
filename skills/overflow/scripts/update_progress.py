#!/usr/bin/env python3
"""Regenerate .learning/PROGRESS.md from progress.json."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    state = root / ".learning"
    progress_path = state / "progress.json"
    state.mkdir(parents=True, exist_ok=True)
    if progress_path.exists():
        try:
            progress = json.loads(progress_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            parser.error(f"invalid progress.json: {exc}")
    else:
        progress = {"version": 1, "course": "unknown", "current_lesson": None, "topics": {}}
        progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")
    topics = progress.get("topics", {}) if isinstance(progress, dict) else {}
    rows = []
    for name, item in sorted(topics.items()):
        if not isinstance(item, dict):
            item = {}
        rows.append(
            f"| {name} | {item.get('status', 'new')} | {item.get('confidence', 0):.2f} | "
            f"{item.get('next_review', 'not scheduled')} |"
        )
    if not rows:
        rows.append("| No topics recorded | new | 0.00 | not scheduled |")
    markdown = "\n".join([
        "# Overflow Progress",
        "",
        f"- Updated: {date.today().isoformat()}",
        f"- Course: {progress.get('course', 'unknown')}",
        f"- Current lesson: {progress.get('current_lesson') or 'not configured'}",
        "",
        "## Topic evidence",
        "",
        "| Topic | Status | Confidence | Next review |",
        "| --- | --- | ---: | --- |",
        *rows,
        "",
        "## Interpretation",
        "",
        "Confidence is a planning signal, not proof of mastery. Use `/assess` and transfer exercises to establish implementation evidence.",
        "",
    ])
    (state / "PROGRESS.md").write_text(markdown, encoding="utf-8")
    print(f"Updated {state / 'PROGRESS.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
