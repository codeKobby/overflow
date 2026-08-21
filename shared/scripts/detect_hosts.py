#!/usr/bin/env python3
"""Detect coding-agent hosts and report their expected skill roots."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


HOSTS = {
    "claude-code": {
        "display_name": "Claude Code",
        "commands": ["claude"],
        "project_paths": [".claude/skills"],
        "global_paths": ["~/.claude/skills"],
    },
    "codex": {
        "display_name": "OpenAI Codex CLI",
        "commands": ["codex"],
        "project_paths": [".agents/skills"],
        "global_paths": ["~/.agents/skills"],
    },
    "cline": {
        "display_name": "Cline",
        "commands": [],
        "project_paths": [".cline/skills", ".clinerules/skills", ".claude/skills"],
        "global_paths": ["~/.cline/skills"],
    },
    "opencode": {
        "display_name": "OpenCode",
        "commands": ["opencode"],
        "project_paths": [".opencode/skills", ".agents/skills", ".claude/skills"],
        "global_paths": ["~/.config/opencode/skills", "~/.agents/skills", "~/.claude/skills"],
    },
    "antigravity": {
        "display_name": "Google Antigravity",
        "commands": [],
        "project_paths": [".agents/skills", ".agent/skills"],
        "global_paths": ["~/.gemini/config/skills"],
    },
    "copilot-vscode": {
        "display_name": "GitHub Copilot / VS Code",
        "commands": ["code"],
        "project_paths": [".github/skills"],
        "global_paths": [],
    },
    "cursor": {
        "display_name": "Cursor",
        "commands": ["cursor"],
        "project_paths": [],
        "global_paths": [],
    },
    "factory": {
        "display_name": "Factory Droid",
        "commands": ["droid"],
        "project_paths": [],
        "global_paths": [],
    },
    "kiro": {
        "display_name": "Kiro",
        "commands": ["kiro"],
        "project_paths": [],
        "global_paths": [],
    },
    "slate": {
        "display_name": "Slate",
        "commands": ["slate"],
        "project_paths": [],
        "global_paths": [],
    },
    "hermes": {
        "display_name": "Hermes",
        "commands": ["hermes"],
        "project_paths": [],
        "global_paths": [],
    },
    "openclaw": {
        "display_name": "OpenClaw",
        "commands": ["openclaw"],
        "project_paths": [],
        "global_paths": [],
    },
    "gbrain": {
        "display_name": "GBrain",
        "commands": ["gbrain"],
        "project_paths": [],
        "global_paths": [],
    },
}


def expand(path_text: str, root: Path) -> Path:
    if path_text.startswith("~/"):
        return Path.home() / path_text[2:]
    if path_text.startswith("."):
        return root / path_text
    return Path(path_text).expanduser()


def detect(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for host_id, data in HOSTS.items():
        commands = {command: shutil.which(command) for command in data["commands"]}
        command_found = any(value for value in commands.values())
        project_paths = [
            {"path": path, "exists": expand(path, root).exists()}
            for path in data["project_paths"]
        ]
        global_paths = [
            {"path": path, "exists": expand(path, root).exists()}
            for path in data["global_paths"]
        ]
        rows.append(
            {
                "id": host_id,
                "display_name": data["display_name"],
                "detected": bool(command_found or any(item["exists"] for item in project_paths + global_paths)),
                "commands": commands,
                "project_paths": project_paths,
                "global_paths": global_paths,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    rows = detect(args.root.resolve())
    if args.json:
        print(json.dumps({"root": str(args.root.resolve()), "hosts": rows}, indent=2))
    else:
        for row in rows:
            state = "detected" if row["detected"] else "not detected"
            print(f"{row['id']}: {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
