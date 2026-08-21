#!/usr/bin/env python3
"""Parse overflow question, answer, and hint markers from a file or repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

QUESTION_RE = re.compile(r"\bCB-Q(?P<number>\d{1,6})(?P<suffix>-[A-Za-z0-9][A-Za-z0-9_-]*)?\b")
ANSWER_START_RE = re.compile(r"\bCB-ANSWER-START\s+(?P<id>CB-Q\d{1,6}(?:-[A-Za-z0-9][A-Za-z0-9_-]*)?)\b")
ANSWER_END_RE = re.compile(r"\bCB-ANSWER-END\s+(?P<id>CB-Q\d{1,6}(?:-[A-Za-z0-9][A-Za-z0-9_-]*)?)\b")
HINT_START_RE = re.compile(r"\bCB-HINT-START\s+(?P<id>CB-Q\d{1,6}(?:-[A-Za-z0-9][A-Za-z0-9_-]*)?)\b(?:\s+level=(?P<level>[0-5]))?")
HINT_END_RE = re.compile(r"\bCB-HINT-END\s+(?P<id>CB-Q\d{1,6}(?:-[A-Za-z0-9][A-Za-z0-9_-]*)?)\b")

SKIP_DIRS = {".git", ".learning/cache", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}
COMMENT_PREFIXES = ("#", "//", "/*", "*", "--", "<!--", ";", "'")

TEXT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".css", ".go", ".html", ".java", ".js", ".jsx", ".md",
    ".mjs", ".php", ".py", ".rb", ".rs", ".sh", ".sql", ".swift", ".ts", ".tsx",
    ".txt", ".vue", ".xml", ".yaml", ".yml", ".json", ".toml",
}


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    parts = relative.parts
    if any(part in {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"} for part in parts):
        return True
    if ".learning" in parts:
        return True
    return False


def iter_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        yield target
        return
    root = target
    for path in sorted(root.rglob("*")):
        if path.name == "manifest.json" or not path.is_file() or should_skip(path, root):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"Dockerfile", "Makefile", "Gemfile", "Procfile"}:
            yield path


def line_window(text: str, line_number: int, radius: int = 1) -> list[str]:
    lines = text.splitlines()
    start = max(0, line_number - 1 - radius)
    end = min(len(lines), line_number + radius)
    return lines[start:end]


def answer_status(lines: list[str], start_line: int, end_line: int) -> str:
    content = [line.strip() for line in lines[start_line:end_line - 1] if line.strip()]
    if not content:
        return "empty"
    if any("TODO:" in line or "replace this" in line.lower() for line in content):
        return "commented-draft"
    if all(line.startswith(COMMENT_PREFIXES) for line in content):
        return "commented-draft"
    return "contains-content"


def parse_file(path: Path, root: Path) -> tuple[dict[str, object], list[str]]:
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"path": str(path.relative_to(root)), "questions": [], "answer_regions": [], "hint_blocks": []}, [f"skipped non-UTF-8 file: {path}"]
    except OSError as exc:
        return {"path": str(path.relative_to(root)), "questions": [], "answer_regions": [], "hint_blocks": []}, [f"could not read {path}: {exc}"]

    lines = text.splitlines()
    questions: list[dict[str, object]] = []
    answer_stacks: dict[str, list[dict[str, object]]] = {}
    hint_stacks: dict[str, list[dict[str, object]]] = {}
    answer_regions: list[dict[str, object]] = []
    hint_blocks: list[dict[str, object]] = []

    for line_number, line in enumerate(lines, start=1):
        marker_delimiter_line = any(token in line for token in ("CB-ANSWER-START", "CB-ANSWER-END", "CB-HINT-START", "CB-HINT-END"))
        if not marker_delimiter_line:
            for match in QUESTION_RE.finditer(line):
                question_id = f"CB-Q{int(match.group('number')):02d}{match.group('suffix') or ''}"
                questions.append({
                    "id": question_id,
                    "line": line_number,
                    "text": line.strip(),
                    "context": line_window(text, line_number),
                })
        for match in ANSWER_START_RE.finditer(line):
            question_id = match.group("id")
            answer_stacks.setdefault(question_id, []).append({"id": question_id, "start_line": line_number})
        for match in ANSWER_END_RE.finditer(line):
            question_id = match.group("id")
            stack = answer_stacks.get(question_id, [])
            if not stack:
                warnings.append(f"unmatched answer end for {question_id} at {path}:{line_number}")
                continue
            region = stack.pop()
            region["end_line"] = line_number
            region["status"] = answer_status(lines, region["start_line"], line_number)
            answer_regions.append(region)
        for match in HINT_START_RE.finditer(line):
            question_id = match.group("id")
            level = int(match.group("level")) if match.group("level") is not None else None
            hint_stacks.setdefault(question_id, []).append({"id": question_id, "level": level, "start_line": line_number})
        for match in HINT_END_RE.finditer(line):
            question_id = match.group("id")
            stack = hint_stacks.get(question_id, [])
            if not stack:
                warnings.append(f"unmatched hint end for {question_id} at {path}:{line_number}")
                continue
            block = stack.pop()
            block["end_line"] = line_number
            hint_blocks.append(block)

    for question_id, stack in answer_stacks.items():
        for region in stack:
            warnings.append(f"unclosed answer region for {question_id} at {path}:{region['start_line']}")
    for question_id, stack in hint_stacks.items():
        for block in stack:
            warnings.append(f"unclosed hint block for {question_id} at {path}:{block['start_line']}")

    seen: set[str] = set()
    duplicate_ids: set[str] = set()
    for question in questions:
        question_id = str(question["id"])
        if question_id in seen:
            duplicate_ids.add(question_id)
        seen.add(question_id)
    for question_id in sorted(duplicate_ids):
        warnings.append(f"duplicate question marker {question_id} in {path}")

    return {
        "path": str(path.relative_to(root)),
        "questions": questions,
        "answer_regions": sorted(answer_regions, key=lambda item: (item["start_line"], item["id"])),
        "hint_blocks": sorted(hint_blocks, key=lambda item: (item["start_line"], item["id"])),
    }, warnings


def parse(target: Path) -> dict[str, object]:
    root = target if target.is_dir() else target.parent
    files: list[dict[str, object]] = []
    warnings: list[str] = []
    for path in iter_files(target):
        result, file_warnings = parse_file(path, root)
        if result["questions"] or result["answer_regions"] or result["hint_blocks"] or file_warnings:
            files.append(result)
        warnings.extend(file_warnings)

    question_ids: dict[str, list[str]] = {}
    for result in files:
        for question in result["questions"]:  # type: ignore[index]
            question_id = str(question["id"])
            question_ids.setdefault(question_id, []).append(str(result["path"]))
    for question_id, paths in sorted(question_ids.items()):
        if len(paths) > 1:
            warnings.append(f"question marker {question_id} appears in multiple files: {', '.join(paths)}")

    return {
        "root": str(root.resolve()),
        "files": files,
        "question_ids": sorted(question_ids),
        "answer_region_count": sum(len(item["answer_regions"]) for item in files),
        "hint_block_count": sum(len(item["hint_blocks"]) for item in files),
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="file or repository root to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    if not target.exists():
        parser.error(f"target does not exist: {target}")
    result = parse(target)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Questions: {len(result['question_ids'])}")
        print(f"Answer regions: {result['answer_region_count']}")
        print(f"Hint blocks: {result['hint_block_count']}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    return 0 if not result["warnings"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
