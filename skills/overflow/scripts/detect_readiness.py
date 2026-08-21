#!/usr/bin/env python3
"""Report whether a repository is ready for durable Overflow learning workflows."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FILES = (
    "CONFIG.md",
    "MISSION.md",
    "PROJECT_MAP.md",
    "PROJECT_GLOSSARY.md",
    "CURRICULUM.md",
    "PROGRESS.md",
    "progress.json",
)
REQUIRED_DIRS = (
    "quiz-sessions",
    "attempts",
    "assessments",
    "learning-records",
    "lessons",
    "cache",
)
DRAFT_FILES = (
    "CONFIG.draft.md",
    "MISSION.draft.md",
    "PROJECT_MAP.draft.md",
    "PROJECT_GLOSSARY.draft.md",
    "CURRICULUM.draft.md",
)


def detect(root: Path) -> dict[str, object]:
    """Inspect state without creating, deleting, or changing any files."""
    resolved_root = root.expanduser().resolve()
    state = resolved_root / ".learning"
    if not state.exists():
        return _result(resolved_root, "uninitialized", [], [], [], [], "setup")
    if not state.is_dir():
        return _result(
            resolved_root,
            "invalid",
            [".learning must be a directory"],
            [],
            [],
            [],
            "repair-or-reinitialize",
        )

    existing_files = [name for name in REQUIRED_FILES if (state / name).is_file()]
    missing_files = [name for name in REQUIRED_FILES if name not in existing_files]
    existing_dirs = [name for name in REQUIRED_DIRS if (state / name).is_dir()]
    missing_dirs = [name for name in REQUIRED_DIRS if name not in existing_dirs]
    draft_files = [name for name in DRAFT_FILES if (state / name).is_file()]

    if len(existing_files) == len(REQUIRED_FILES) and not missing_dirs:
        status = "initialized"
        next_action = "continue"
    elif draft_files and not existing_files:
        status = "draft"
        next_action = "resume-setup"
    elif existing_files or existing_dirs or draft_files:
        status = "partial"
        next_action = "resume-setup"
    else:
        status = "uninitialized"
        next_action = "setup"

    return _result(
        resolved_root,
        status,
        missing_files,
        missing_dirs,
        existing_files,
        existing_dirs,
        next_action,
        draft_files=draft_files,
    )


def _result(
    root: Path,
    status: str,
    missing_files: list[str],
    missing_dirs: list[str],
    existing_files: list[str],
    existing_dirs: list[str],
    next_action: str,
    *,
    draft_files: list[str] | None = None,
) -> dict[str, object]:
    return {
        "root": str(root),
        "state_directory": str(root / ".learning"),
        "status": status,
        "ready": status == "initialized",
        "missing_files": missing_files,
        "missing_directories": missing_dirs,
        "existing_files": existing_files,
        "existing_directories": existing_dirs,
        "draft_files": draft_files or [],
        "next_action": next_action,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    result = detect(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        label = {
            "initialized": "initialized and ready",
            "uninitialized": "not initialized",
            "draft": "setup drafts found; setup is not confirmed",
            "partial": "partial state found; setup is incomplete",
            "invalid": "invalid .learning path",
        }.get(str(result["status"]), str(result["status"]))
        print(f"Overflow state: {label}")
        if result["missing_files"]:
            print("Missing files: " + ", ".join(result["missing_files"]))
        if result["missing_directories"]:
            print("Missing directories: " + ", ".join(result["missing_directories"]))
        print(f"Next action: {result['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
