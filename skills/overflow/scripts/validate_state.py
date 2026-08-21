#!/usr/bin/env python3
"""Validate a repository-local .learning state directory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_DIRS = ["quiz-sessions", "attempts", "assessments", "learning-records"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    state = root / ".learning"
    errors: list[str] = []
    warnings: list[str] = []
    if not state.is_dir():
        errors.append("missing .learning directory")
    else:
        for filename in ["CONFIG.md", "MISSION.md", "PROGRESS.md", "progress.json"]:
            if not (state / filename).exists():
                warnings.append(f"missing {filename}")
        for dirname in REQUIRED_DIRS:
            if not (state / dirname).is_dir():
                warnings.append(f"missing directory {dirname}")
        progress_path = state / "progress.json"
        if progress_path.exists():
            try:
                data = json.loads(progress_path.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    errors.append("progress.json must contain an object")
                elif "topics" in data and not isinstance(data["topics"], dict):
                    errors.append("progress.json topics must be an object")
            except json.JSONDecodeError as exc:
                errors.append(f"invalid progress.json: {exc}")
        for session in (state / "quiz-sessions").glob("*.json") if (state / "quiz-sessions").exists() else []:
            try:
                data = json.loads(session.read_text(encoding="utf-8"))
                for key in ["session_id", "status", "questions"]:
                    if key not in data:
                        errors.append(f"{session.name}: missing {key}")
            except json.JSONDecodeError as exc:
                errors.append(f"{session.name}: invalid JSON: {exc}")
    result = {"root": str(root), "valid": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
