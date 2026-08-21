#!/usr/bin/env python3
"""Validate the public code-buddy distribution compatibility contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_HOSTS = {
    "claude-code",
    "codex",
    "cline",
    "opencode",
    "antigravity",
    "copilot-vscode",
    "cursor",
    "factory",
    "kiro",
    "slate",
    "hermes",
    "openclaw",
    "gbrain",
}
REQUIRED_SKILLS = {
    "code-buddy",
    "setup-learning",
    "teach",
    "quiz",
    "exercise",
    "hint",
    "assess",
    "explain",
    "review",
    "progress",
    "next",
    "learn",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "manifest.json"
    hosts_path = root / "compatibility" / "hosts.json"
    plugin_path = root / ".claude-plugin" / "plugin.json"

    if not manifest_path.is_file():
        fail("missing manifest.json", errors)
        return errors
    if not hosts_path.is_file():
        fail("missing compatibility/hosts.json", errors)
    if not (root / "compatibility" / "README.md").is_file():
        fail("missing compatibility/README.md", errors)
    if not (root / "AGENTS.md").is_file():
        fail("missing AGENTS.md", errors)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid manifest.json: {exc}", errors)
        return errors

    version = manifest.get("version")
    if version != "0.5.0":
        fail(f"manifest version must be 0.5.0, got {version!r}", errors)
    skills = set(manifest.get("skills", []))
    missing_skills = REQUIRED_SKILLS - skills
    if missing_skills:
        fail(f"manifest missing skills: {sorted(missing_skills)}", errors)

    for skill in REQUIRED_SKILLS:
        skill_file = root / "skills" / skill / "SKILL.md"
        if not skill_file.is_file():
            fail(f"missing skill file: skills/{skill}/SKILL.md", errors)
        metadata = root / "skills" / skill / "agents" / "openai.yaml"
        if not metadata.is_file():
            fail(f"missing Codex metadata: skills/{skill}/agents/openai.yaml", errors)

    if plugin_path.is_file():
        try:
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid .claude-plugin/plugin.json: {exc}", errors)
        else:
            if plugin.get("version") != version:
                fail("Claude plugin version does not match manifest version", errors)
            for relative in plugin.get("skills", []):
                if not (root / relative).is_dir():
                    fail(f"Claude plugin skill path does not exist: {relative}", errors)
    else:
        fail("missing optional Claude plugin manifest", errors)

    if hosts_path.is_file():
        try:
            host_data = json.loads(hosts_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid compatibility/hosts.json: {exc}", errors)
        else:
            if host_data.get("version") != version:
                fail("host matrix version does not match manifest version", errors)
            hosts = {host.get("id") for host in host_data.get("hosts", [])}
            missing_hosts = REQUIRED_HOSTS - hosts
            if missing_hosts:
                fail(f"host matrix missing hosts: {sorted(missing_hosts)}", errors)
            for host in host_data.get("hosts", []):
                if host.get("tier") not in {"A", "B", "C"}:
                    fail(f"invalid support tier for host {host.get('id')!r}", errors)
                if not host.get("project_paths") or not host.get("global_paths"):
                    fail(f"host lacks project/global path guidance: {host.get('id')!r}", errors)
                if not host.get("install"):
                    fail(f"host lacks install guidance: {host.get('id')!r}", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="code-buddy distribution root")
    parser.add_argument("--json", action="store_true", help="emit structured JSON")
    args = parser.parse_args()

    errors = validate(args.root.resolve())
    payload = {"valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(payload, indent=2))
    elif errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
    else:
        print("VALID: code-buddy compatibility contract")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
