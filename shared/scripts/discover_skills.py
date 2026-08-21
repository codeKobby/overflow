#!/usr/bin/env python3
"""Discover installed Agent Skills without invoking or modifying them."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from detect_hosts import HOSTS, expand
except ImportError:  # pragma: no cover - supports direct module loading in tests
    import importlib.util

    _host_path = Path(__file__).with_name("detect_hosts.py")
    _host_spec = importlib.util.spec_from_file_location("overflow_detect_hosts", _host_path)
    if _host_spec is None or _host_spec.loader is None:
        raise RuntimeError("could not load detect_hosts.py")
    _host_module = importlib.util.module_from_spec(_host_spec)
    _host_spec.loader.exec_module(_host_module)
    HOSTS = _host_module.HOSTS
    expand = _host_module.expand


_FIELD_RE = re.compile(r"^(name|description):\s*[\"']?(.*?)[\"']?\s*$")


def _metadata(skill_file: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return fields
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:80]:
        if line.strip() == "---":
            break
        match = _FIELD_RE.match(line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def discover(root: Path, *, include_global: bool = False) -> list[dict[str, object]]:
    """Return metadata for installed skills visible from the repository."""
    resolved_root = root.expanduser().resolve()
    rows: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for host_id, host in HOSTS.items():
        scopes = [("project", path) for path in host.get("project_paths", [])]
        if include_global:
            scopes.extend(("global", path) for path in host.get("global_paths", []))
        for scope, root_text in scopes:
            skill_root = expand(root_text, resolved_root)
            if not skill_root.is_dir():
                continue
            for skill_file in sorted(skill_root.glob("*/SKILL.md")):
                skill_name = skill_file.parent.name
                key = (scope, str(skill_file.resolve()))
                if key in seen:
                    continue
                seen.add(key)
                metadata = _metadata(skill_file)
                rows.append(
                    {
                        "name": metadata.get("name", skill_name),
                        "directory": skill_name,
                        "description": metadata.get("description", ""),
                        "host": host_id,
                        "scope": scope,
                        "path": str(skill_file),
                    }
                )
    return sorted(rows, key=lambda row: (str(row["name"]), str(row["scope"]), str(row["host"]), str(row["path"])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--include-global", action="store_true", help="also inspect global skill roots")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    rows = discover(args.root, include_global=args.include_global)
    result = {"root": str(args.root.expanduser().resolve()), "skills": rows}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if not rows:
            print("No installed skills found in the selected roots.")
        for row in rows:
            print(f"{row['name']} ({row['scope']}, {row['host']}): {row['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
