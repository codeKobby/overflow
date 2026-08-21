#!/usr/bin/env python3
"""Plan an Overflow route without changing repository state.

The router is intentionally conservative. It classifies explicit Overflow commands
first, recognizes a small set of natural-language learning intents, and treats
other artifact work as a specialist-handoff candidate. The agent remains
responsible for presenting the route and invoking the selected skill.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
_READINESS_PATH = ROOT / "detect_readiness.py"


def _load_readiness():
    spec = importlib.util.spec_from_file_location("overflow_detect_readiness", _READINESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {_READINESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPLICIT_ROUTES: dict[str, tuple[str, str, bool, bool]] = {
    "help": ("help", "help", False, True),
    "setup-learning": ("initialize", "setup-learning", False, True),
    "teach": ("teach", "teach", True, False),
    "quiz": ("quiz", "quiz", True, False),
    "exercise": ("exercise", "exercise", True, False),
    "hint": ("hint", "hint", True, False),
    "assess": ("assess", "assess", True, False),
    "explain": ("explain", "explain", False, True),
    "review": ("review", "review", True, False),
    "progress": ("progress", "progress", True, False),
    "next": ("next", "next", True, False),
    "learn": ("memory", "learn", True, False),
    "handoff": ("handoff", "handoff", False, True),
}

STATEFUL_INTENTS = {"teach", "quiz", "exercise", "hint", "assess", "review", "progress", "next", "learn", "orient"}


def _first_token(request: str) -> str:
    match = re.match(r"\s*/?([A-Za-z][A-Za-z0-9_-]*)", request)
    return match.group(1).lower() if match else ""


def _explicit_route(request: str) -> tuple[str, str, bool, bool] | None:
    token = _first_token(request)
    if token == "overflow":
        match = re.match(r"/?[A-Za-z][A-Za-z0-9_-]*", request.strip())
        remainder = request.strip()[len(match.group(0)) :] .strip() if match else ""
        if not remainder:
            return ("orient", "next", True, False)
        remainder_token = _first_token(remainder)
        if remainder_token in EXPLICIT_ROUTES:
            return EXPLICIT_ROUTES[remainder_token]
        return _classify_natural(remainder)
    if token in EXPLICIT_ROUTES:
        return EXPLICIT_ROUTES[token]
    return None


def _classify_natural(request: str) -> tuple[str, str, bool, bool]:
    text = request.lower().strip()
    if not text:
        return ("orient", "next", True, False)
    if re.search(r"\b(help|what can you do|commands?)\b", text):
        return ("help", "help", False, True)
    if re.search(r"\b(quiz|test me|questions?)\b", text):
        return ("quiz", "quiz", True, False)
    if re.search(r"\b(hint|stuck|don't know how|do not know how)\b", text):
        return ("hint", "hint", True, False)
    if re.search(r"\b(assess|grade|check my answer|evaluate my)\b", text):
        return ("assess", "assess", True, False)
    if re.search(r"\b(review|revise|refresh|spaced review)\b", text):
        return ("review", "review", True, False)
    if re.search(r"\b(explain|why does|what does|how does|walk me through)\b", text):
        return ("explain", "explain", False, True)
    if re.search(r"\b(teach|learn|study|understand|from this repo|from this codebase|practice)\b", text):
        return ("learn", "next", True, False)
    if re.search(r"\b(progress|how am i doing|what have i learned)\b", text):
        return ("progress", "progress", True, False)
    if re.search(r"\b(implement|build|fix|debug|test|review|refactor|document|deploy|ship|ui|dashboard|security|performance)\b", text):
        return ("specialist-work", "handoff", False, True)
    return ("direct", "direct", False, True)


def _state_transition(status: str, next_action: str, skill: str, requires_init: bool) -> dict[str, Any]:
    if skill in {"help", "explain", "direct", "handoff"} or not requires_init:
        return {
            "route": skill,
            "route_kind": "direct" if skill in {"help", "explain", "direct"} else "specialist-candidate",
            "requires_initialization": False,
            "initializer": None,
        }
    if status == "initialized":
        return {
            "route": skill,
            "route_kind": "overflow",
            "requires_initialization": False,
            "initializer": None,
        }
    if status in {"uninitialized", "draft", "partial"}:
        return {
            "route": "setup-learning",
            "route_kind": "initializer",
            "requires_initialization": True,
            "initializer": {
                "status": status,
                "next_action": next_action,
                "original_route": skill,
                "resume_after_setup": True,
            },
        }
    return {
        "route": "setup-learning",
        "route_kind": "initializer-blocked",
        "requires_initialization": True,
        "initializer": {
            "status": status,
            "next_action": next_action,
            "original_route": skill,
            "resume_after_setup": False,
        },
    }


def plan(root: Path, request: str) -> dict[str, Any]:
    readiness = _load_readiness().detect(root)
    explicit = _explicit_route(request)
    intent, skill, requires_init, can_stateless = explicit or _classify_natural(request)
    transition = _state_transition(str(readiness["status"]), str(readiness["next_action"]), skill, requires_init)

    if transition["route_kind"] == "initializer":
        status = str(readiness["status"])
        if status == "uninitialized":
            announcement = (
                "I’m going to run `/setup-learning` first because this repository has no Overflow learning state. "
                "I’ll inspect the repository, ask the setup questions, and wait for confirmation before writing `.learning/`. "
                f"After setup, I’ll continue with `/{skill}` for your original request."
            )
        else:
            announcement = (
                f"I found {status} Overflow learning state, so I’m going to resume `/setup-learning` before continuing. "
                f"After setup, I’ll continue with `/{skill}` for your original request without discarding existing drafts or records."
            )
    elif transition["route_kind"] == "initializer-blocked":
        announcement = (
            "I found an unusable `.learning/` path. I will not delete or repair it automatically. "
            "I need your confirmation before choosing a repair or another repository."
        )
    elif transition["route_kind"] == "specialist-candidate":
        announcement = (
            "This is implementation or artifact work rather than a core learning command. "
            "I’ll inspect installed skill metadata and propose the closest specialist before invoking anything."
        )
    elif transition["route"] == "direct":
        announcement = "No specific Overflow workflow is required, so I’ll answer directly without creating learning state."
    elif transition["route"] == "explain":
        announcement = "I’ll route this to `/explain` and answer inline without creating learning state. If you want it saved as a lesson, I’ll offer that next."
    elif intent == "orient":
        announcement = "I’ll route `/overflow` to the next smallest learning action for this repository."
    else:
        announcement = f"I’ll route this to `/{transition['route']}` and keep the result connected to Overflow learning evidence."

    return {
        "request": request,
        "intent": intent,
        "readiness": readiness,
        "route": transition["route"],
        "route_kind": transition["route_kind"],
        "requires_initialization": transition["requires_initialization"],
        "can_continue_statelessly": can_stateless,
        "announcement": announcement,
        "continuation": {
            "original_request": request,
            "resume_route": skill if transition["route_kind"] == "initializer" else None,
            "resume_after_setup": bool(transition.get("initializer", {}).get("resume_after_setup", False)) if transition.get("initializer") else False,
        },
        "initializer": transition.get("initializer"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--request", default="", help="the original user request or slash command")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    result = plan(args.root, args.request)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["announcement"])
        print(f"Route: /{result['route']}")
        if result["continuation"]["resume_after_setup"]:
            print(f"Continue after setup: /{result['continuation']['resume_route']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
