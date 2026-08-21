#!/usr/bin/env python3
"""Inspect and optionally create isolated Git branches or worktrees for Overflow exercises."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

STATE_FILE = ".learning/git-workflow.json"
DEFAULT_BRANCH_PREFIX = "overflow/exercise"


def run_git(root: Path, args: Iterable[str], *, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise RuntimeError(detail)
    return completed.stdout.strip()


def ensure_git_root(root: Path) -> Path:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise RuntimeError(f"not a directory: {root}")
    try:
        git_root = Path(run_git(root, ["rev-parse", "--show-toplevel"]))
    except RuntimeError as exc:
        raise RuntimeError(f"not a Git worktree: {root}: {exc}") from exc
    return git_root.resolve()


def safe_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[: sixty] if (sixty := 60) else value


def current_branch(root: Path) -> str:
    branch = run_git(root, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)
    return branch or "HEAD-detached"


def default_branch(root: Path) -> str | None:
    remote_head = run_git(root, ["symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"], check=False)
    if remote_head.startswith("origin/"):
        return remote_head.split("/", 1)[1]
    for candidate in ("main", "master", current_branch(root)):
        if candidate and run_git(root, ["show-ref", "--verify", f"refs/heads/{candidate}"], check=False):
            return candidate
    return None


def status_lines(root: Path) -> list[str]:
    output = run_git(root, ["status", "--porcelain=v1"], check=False)
    return [line for line in output.splitlines() if line.strip()]


def branch_exists(root: Path, branch: str) -> bool:
    return bool(run_git(root, ["show-ref", "--verify", f"refs/heads/{branch}"], check=False))


def worktree_paths(root: Path) -> list[dict[str, str]]:
    output = run_git(root, ["worktree", "list", "--porcelain"], check=False)
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in output.splitlines() + [""]:
        if not line:
            if current:
                records.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    return records


def inspect(root: Path) -> dict[str, object]:
    root = ensure_git_root(root)
    head = run_git(root, ["rev-parse", "HEAD"], check=False)
    return {
        "root": str(root),
        "current_branch": current_branch(root),
        "default_branch": default_branch(root),
        "head": head,
        "clean": not status_lines(root),
        "status": status_lines(root),
        "branches": run_git(root, ["branch", "--format=%(refname:short)"], check=False).splitlines(),
        "remotes": run_git(root, ["remote", "-v"], check=False).splitlines(),
        "worktrees": worktree_paths(root),
        "state_file": str(root / STATE_FILE),
    }


def branch_for(slug: str, branch: str | None) -> str:
    if branch:
        candidate = branch.strip()
        if candidate.startswith("-") or ".." in candidate or candidate.endswith("."):
            raise RuntimeError("unsafe branch name")
        return candidate
    normalized = safe_slug(slug)
    if not normalized:
        raise RuntimeError("exercise slug must contain letters or numbers")
    return f"{DEFAULT_BRANCH_PREFIX}/{normalized}"


def plan(root: Path, *, mode: str, slug: str, branch: str | None, worktree: str | None, base: str | None) -> dict[str, object]:
    info = inspect(root)
    target_branch = branch_for(slug, branch)
    base_branch = base or info["current_branch"]
    clean = bool(info["clean"])
    exists = branch_exists(Path(info["root"]), target_branch)
    if mode == "branch":
        command = ["git", "switch", "--create", target_branch, str(base_branch)]
    else:
        worktree_path = worktree or str(Path(info["root"]).parent / f"{Path(info['root']).name}-overflow-{safe_slug(slug)}")
        command = ["git", "worktree", "add", "-b", target_branch, worktree_path, str(base_branch)]
    return {
        "mode": mode,
        "root": info["root"],
        "current_branch": info["current_branch"],
        "base_branch": base_branch,
        "base_commit": info["head"],
        "clean": clean,
        "target_branch": target_branch,
        "target_exists": exists,
        "worktree_path": worktree if mode == "worktree" else None,
        "safe_to_apply": clean and not exists and info["current_branch"] != "HEAD-detached",
        "command": " ".join(command),
        "warnings": [
            "Uncommitted changes must be preserved or resolved before branching." if not clean else "",
            "The target branch already exists; choose it explicitly or use another slug." if exists else "",
            "Creating a branch does not commit, push, or open a pull request." if clean and not exists else "",
        ],
    }


def write_state(root: Path, *, mode: str, target_branch: str, base_branch: str, base_commit: str, worktree_path: str | None) -> Path:
    state_path = root / STATE_FILE
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "mode": mode,
        "base_branch": base_branch,
        "base_commit": base_commit,
        "exercise_branch": target_branch,
        "worktree_path": worktree_path,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "commit_status": "not-requested",
        "push_status": "not-requested",
        "pull_request_status": "not-requested",
    }
    state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return state_path


def apply(root: Path, *, mode: str, slug: str, branch: str | None, worktree: str | None, base: str | None) -> dict[str, object]:
    root = ensure_git_root(root)
    proposal = plan(root, mode=mode, slug=slug, branch=branch, worktree=worktree, base=base)
    if not proposal["safe_to_apply"]:
        raise RuntimeError("refusing to apply Git workflow: " + "; ".join(item for item in proposal["warnings"] if item))
    target_branch = str(proposal["target_branch"])
    base_branch = str(proposal["base_branch"])
    if mode == "branch":
        run_git(root, ["switch", "--create", target_branch, base_branch])
        worktree_path = None
    else:
        worktree_path = str(proposal["worktree_path"] or (root.parent / f"{root.name}-overflow-{safe_slug(slug)}"))
        run_git(root, ["worktree", "add", "-b", target_branch, worktree_path, base_branch])
    state_path = write_state(root, mode=mode, target_branch=target_branch, base_branch=base_branch, base_commit=str(proposal["base_commit"]), worktree_path=worktree_path)
    return {**inspect(root), "created": True, "mode": mode, "exercise_branch": target_branch, "worktree_path": worktree_path, "state_file": str(state_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--mode", choices=["inspect", "plan", "branch", "worktree"], default="inspect")
    parser.add_argument("--slug", default="exercise", help="short exercise identifier used in the branch name")
    parser.add_argument("--branch", help="explicit branch name; defaults to overflow/exercise/<slug>")
    parser.add_argument("--base", help="base branch or commit; defaults to the current branch")
    parser.add_argument("--worktree", help="path for --mode worktree")
    parser.add_argument("--apply", action="store_true", help="required to create a branch or worktree")
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        if args.mode == "inspect":
            result = inspect(root)
        elif args.mode == "plan":
            result = plan(root, mode="branch", slug=args.slug, branch=args.branch, worktree=args.worktree, base=args.base)
        else:
            if not args.apply:
                raise RuntimeError("creation requires --apply after the agent has obtained learner confirmation")
            result = apply(root, mode=args.mode, slug=args.slug, branch=args.branch, worktree=args.worktree, base=args.base)
    except (OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
