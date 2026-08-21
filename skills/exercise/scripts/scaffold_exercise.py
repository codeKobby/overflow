#!/usr/bin/env python3
"""Create a learner-owned, comment-marked exercise scaffold from numbered Markdown prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

NUMBERED_ITEM_RE = re.compile(r"^(?P<indent>\s{0,3})(?P<number>\d{1,4})[.)]\s+(?P<prompt>\S.*)$")
HEADING_RE = re.compile(r"^#{1,6}\s+(?P<title>\S.*)$")

COMMENT_STYLES = {
    ".c": ("//", "//"),
    ".cc": ("//", "//"),
    ".cpp": ("//", "//"),
    ".css": ("/*", "*/"),
    ".go": ("//", "//"),
    ".html": ("<!--", "-->"),
    ".java": ("//", "//"),
    ".js": ("//", "//"),
    ".jsx": ("//", "//"),
    ".mjs": ("//", "//"),
    ".php": ("//", "//"),
    ".py": ("#", "#"),
    ".rb": ("#", "#"),
    ".rs": ("//", "//"),
    ".sh": ("#", "#"),
    ".sql": ("--", "--"),
    ".swift": ("//", "//"),
    ".ts": ("//", "//"),
    ".tsx": ("//", "//"),
    ".vue": ("//", "//"),
    ".xml": ("<!--", "-->"),
}


@dataclass(frozen=True)
class Prompt:
    ordinal: int
    source_line: int
    text: str
    heading: str | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def extract_prompts(source: Path) -> tuple[list[Prompt], str | None]:
    prompts: list[Prompt] = []
    heading: str | None = None
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = heading_match.group("title").strip()
        item_match = NUMBERED_ITEM_RE.match(line)
        if not item_match or item_match.group("indent"):
            continue
        prompts.append(
            Prompt(
                ordinal=int(item_match.group("number")),
                source_line=line_number,
                text=item_match.group("prompt").strip(),
                heading=heading,
            )
        )
    return prompts, heading


def question_id(sequence: int) -> str:
    return f"CB-Q{sequence:02d}"


def comment_style(answer_path: Path, requested: str | None) -> tuple[str, str]:
    if requested:
        styles = {
            "hash": ("#", "#"),
            "slash": ("//", "//"),
            "html": ("<!--", "-->"),
            "block": ("/*", "*/"),
            "sql": ("--", "--"),
        }
        if requested not in styles:
            raise ValueError(f"unknown comment style: {requested}")
        return styles[requested]
    if answer_path.suffix.lower() in COMMENT_STYLES:
        return COMMENT_STYLES[answer_path.suffix.lower()]
    return ("<!--", "-->")


def wrapped_comment(prefix: str, suffix: str, text: str) -> str:
    if prefix in {"<!--", "/*"}:
        return f"{prefix} {text} {suffix}"
    return f"{prefix} {text}"


def build_answer_template(prompts: list[Prompt], answer_path: Path, style: str | None) -> tuple[str, list[dict[str, object]]]:
    prefix, suffix = comment_style(answer_path, style)
    lines: list[str] = []
    regions: list[dict[str, object]] = []
    for sequence, prompt in enumerate(prompts, start=1):
        question = question_id(sequence)
        lines.append(wrapped_comment(prefix, suffix, f"{question}: {prompt.text}"))
        lines.append(wrapped_comment(prefix, suffix, f"CB-ANSWER-START {question}"))
        start_line = len(lines)
        lines.append(wrapped_comment(prefix, suffix, "TODO: write your answer here; keep this line until you replace it."))
        end_line = len(lines) + 1
        lines.append(wrapped_comment(prefix, suffix, f"CB-ANSWER-END {question}"))
        regions.append({
            "path": str(answer_path),
            "start_marker": f"CB-ANSWER-START {question}",
            "end_marker": f"CB-ANSWER-END {question}",
            "start_line": start_line + 1,
            "end_line": end_line,
        })
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", regions


def build_manifest(root: Path, source: Path, exercise_id: str, title: str, prompts: list[Prompt], answer_regions: list[dict[str, object]], answer_path: Path) -> dict[str, object]:
    relative_source = str(source.relative_to(root))
    relative_answer = str(answer_path.relative_to(root))
    questions: list[dict[str, object]] = []
    for sequence, (prompt, region) in enumerate(zip(prompts, answer_regions), start=1):
        question = question_id(sequence)
        questions.append({
            "id": question,
            "ordinal": prompt.ordinal,
            "sequence": sequence,
            "prompt": prompt.text,
            "source_anchor": f"{relative_source}#L{prompt.source_line}",
            "heading": prompt.heading,
            "targets": [relative_answer],
            "answer_regions": [region],
            "acceptance": [],
            "checks": [],
            "hint_level": 0,
            "status": "scaffolded",
            "attempts": 0,
            "last_evidence": None,
        })
    return {
        "version": 1,
        "exercise_id": exercise_id,
        "title": title,
        "created": date.today().isoformat(),
        "source": {
            "prompt_path": relative_source,
            "source_hash": sha256_file(source),
            "source_anchor": f"{relative_source}#L{prompts[0].source_line}" if prompts else relative_source,
        },
        "status": "in-progress",
        "active_question": question_id(1) if prompts else None,
        "questions": questions,
        "answer_file": relative_answer,
        "notes": [
            "Generated by code-buddy from numbered prompts.",
            "Review and complete acceptance/check fields before relying on automated assessment.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="repository-relative Markdown exercise or lesson file")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--exercise-id", required=True, help="stable exercise identifier")
    parser.add_argument("--title", help="display title; defaults to the source filename")
    parser.add_argument("--out", type=Path, required=True, help="learner-owned exercise directory")
    parser.add_argument("--answer-file", default="answers.md", help="answer filename inside --out")
    parser.add_argument("--comment-style", choices=["hash", "slash", "html", "block", "sql"], help="override comment syntax")
    parser.add_argument("--force", action="store_true", help="replace generated files if they already exist")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    source = args.source.expanduser()
    if not source.is_absolute():
        source = root / source
    source = source.resolve()
    out = args.out.expanduser()
    if not out.is_absolute():
        out = root / out
    out = out.resolve()
    answer_path = out / args.answer_file
    manifest_path = out / "manifest.json"
    if not source.is_file():
        parser.error(f"source is not a file: {source}")
    try:
        source.relative_to(root)
        out.relative_to(root)
    except ValueError:
        parser.error("source and output must be inside --root")
    if (answer_path.exists() or manifest_path.exists()) and not args.force:
        parser.error("output already exists; use --force only after reviewing the diff")

    prompts, heading = extract_prompts(source)
    if not prompts:
        parser.error("no top-level numbered prompts found; create a manual manifest instead")
    title = args.title or heading or source.stem.replace("_", " ").replace("-", " ").title()
    answer_text, regions = build_answer_template(prompts, answer_path, args.comment_style)
    manifest = build_manifest(root, source, args.exercise_id, title, prompts, regions, answer_path)
    out.mkdir(parents=True, exist_ok=True)
    answer_path.write_text(answer_text, encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "exercise_id": args.exercise_id,
        "title": title,
        "question_count": len(prompts),
        "answer_file": str(answer_path.relative_to(root)),
        "manifest": str(manifest_path.relative_to(root)),
        "source_hash": manifest["source"]["source_hash"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
