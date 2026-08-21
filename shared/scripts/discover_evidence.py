#!/usr/bin/env python3
"""Discover repository-native and inferred learning evidence sections."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", ".learning", "dist", "build"}
TEXT_SUFFIXES = {".md", ".markdown", ".rst", ".txt"}
SOURCE_SUFFIXES = TEXT_SUFFIXES | {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".php", ".css", ".html"}
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>\S.*?)\s*$")
LINK_RE = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")

ROLE_PATTERNS: dict[str, tuple[str, ...]] = {
    "practice": (
        "practice", "independent exercise", "exercises", "workshop", "try it", "tasks", "challenge", "guided practice"
    ),
    "proof": (
        "prove it", "prove", "check your understanding", "comprehension", "answer these", "questions", "self check", "self-check"
    ),
    "finish": (
        "finish line", "completion", "done when", "ready when", "complete when", "exit criteria", "definition of done"
    ),
    "reflection": (
        "self-assessment", "self assessment", "reflection", "review note", "what you learned", "limitation", "limitations"
    ),
    "verification": (
        "verify", "verification", "expected output", "run it", "check", "test", "assertion", "expected result", "prove it"
    ),
    "hints": ("hint", "help", "clue"),
    "solutions": ("solution", "solutions", "finished", "answer key", "answers"),
    "safety": ("safety", "scope", "authorization", "authorized", "lab rules", "out of scope", "boundaries"),
}

ROLE_EVIDENCE: dict[str, str] = {
    "practice": "implementation",
    "proof": "reasoning",
    "finish": "completion",
    "reflection": "transfer",
    "verification": "verification",
    "hints": "support",
    "solutions": "reference-only",
    "safety": "safety",
}


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED for part in path.parts):
            continue
        if path.suffix.lower() in SOURCE_SUFFIXES:
            yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def normalize(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def roles_for(title: str) -> tuple[list[str], dict[str, float]]:
    normalized = normalize(title)
    words = normalized.split()
    roles: list[str] = []
    confidence: dict[str, float] = {}
    for role, patterns in ROLE_PATTERNS.items():
        exact = [pattern for pattern in patterns if normalize(pattern) == normalized]
        contains = [
            pattern
            for pattern in patterns
            if normalize(pattern) in normalized
            and normalize(pattern) not in exact
            and (len(words) <= 8 or normalized.startswith(normalize(pattern)))
        ]
        if exact:
            roles.append(role)
            confidence[role] = 1.0
        elif contains:
            roles.append(role)
            confidence[role] = 0.8
    return roles, confidence


def section_records(path: Path, root: Path) -> list[dict[str, object]]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    headings: list[tuple[int, int, str]] = []
    for line_number, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_number, len(match.group("marks")), match.group("title").strip()))
    sections: list[dict[str, object]] = []
    for index, (start, level, title) in enumerate(headings):
        end = len(lines)
        for next_start, next_level, _ in headings[index + 1 :]:
            if next_level <= level:
                end = next_start - 1
                break
        roles, confidence = roles_for(title)
        if not roles:
            continue
        body = [line.strip() for line in lines[start:end] if line.strip() and not HEADING_RE.match(line)]
        links = [match.group("target") for line in lines[start:end] for match in LINK_RE.finditer(line)]
        sections.append({
            "role": roles,
            "evidence_types": sorted({ROLE_EVIDENCE[role] for role in roles}),
            "confidence": confidence,
            "source_kind": "native",
            "path": str(path.relative_to(root).as_posix()),
            "title": title,
            "level": level,
            "start_line": start,
            "end_line": end,
            "source_hash": sha256(path),
            "preview": " ".join(body)[:360],
            "links": links[:20],
        })
    return sections


def project_inventory(root: Path, paths: list[Path]) -> dict[str, list[str]]:
    docs: list[str] = []
    tests: list[str] = []
    source_files: list[str] = []
    entry_points: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in {".md", ".markdown", ".rst", ".txt"} and len(docs) < 80:
            docs.append(relative)
        if any(part.lower() in {"test", "tests", "spec", "__tests__"} for part in path.parts) or re.search(r"(?:^test_|\.test\.|\.spec\.|_test\.)", path.name, re.I):
            if len(tests) < 80:
                tests.append(relative)
        if path.suffix.lower() in {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".php", ".css", ".html"} and len(source_files) < 80:
            source_files.append(relative)
        if path.name in {"main.py", "app.py", "main.ts", "main.tsx", "index.ts", "index.tsx", "main.js", "index.js"} and len(entry_points) < 60:
            entry_points.append(relative)
    return {"documentation": docs, "tests": tests, "source_files": source_files, "entry_points": entry_points}


def inferred_plan(root: Path, sections: list[dict[str, object]], inventory: dict[str, list[str]], repository_type: str | None) -> list[dict[str, object]]:
    present = {role for section in sections for role in section["role"]}
    if repository_type not in {"source-project", "hybrid", None}:
        return []
    plan: list[dict[str, object]] = []
    if "practice" not in present:
        anchors = inventory["entry_points"][:3] or inventory["source_files"][:3] or inventory["documentation"][:3]
        plan.append({"role": "practice", "source_kind": "inferred", "prompt_seed": "Change one small behavior in the selected source slice and show the evidence.", "anchors": anchors})
    if "proof" not in present:
        anchors = inventory["entry_points"][:3] or inventory["source_files"][:3] or inventory["documentation"][:3]
        plan.append({"role": "proof", "source_kind": "inferred", "prompt_seed": "In your own words, what does the selected symbol or flow do, and which source lines prove it?", "anchors": anchors})
    if "verification" not in present:
        plan.append({"role": "verification", "source_kind": "inferred", "prompt_seed": "Run the repository’s documented test or check for the selected behavior and record what it proves.", "anchors": inventory["tests"][:5] or inventory["source_files"][:3]})
    if "finish" not in present:
        plan.append({"role": "finish", "source_kind": "inferred", "prompt_seed": "Explain the normal case, one boundary or failure case, one limitation, and the next evidence needed.", "anchors": inventory["tests"][:3] + (inventory["entry_points"][:3] or inventory["source_files"][:3])})
    return plan


def discover(root: Path, repository_type: str | None = None) -> dict[str, object]:
    paths = list(iter_text_files(root))
    sections = [section for path in paths for section in section_records(path, root)]
    inventory = project_inventory(root, paths)
    role_counts: dict[str, int] = {}
    for section in sections:
        for role in section["role"]:
            role_counts[role] = role_counts.get(role, 0) + 1
    inferred = inferred_plan(root, sections, inventory, repository_type)
    return {
        "root": str(root.resolve()),
        "repository_type": repository_type,
        "native_sections": sections,
        "native_role_counts": role_counts,
        "inferred_evidence": inferred,
        "evidence_order": ["implementation", "verification", "reasoning", "edge-case", "completion", "transfer", "safety"],
        "inventory": inventory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--repository-type", choices=["structured-course", "source-project", "hybrid", "sparse"])
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    result = discover(root, args.repository_type)
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Native evidence sections: {len(result['native_sections'])}")
        print("Roles:", ", ".join(f"{key}={value}" for key, value in sorted(result["native_role_counts"].items())) or "none")
        print(f"Inferred evidence steps: {len(result['inferred_evidence'])}")
        for section in result["native_sections"][:30]:
            print(f"  {section['path']}:{section['start_line']} — {section['title']} [{', '.join(section['role'])}]")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
