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
        git_workflow = state / "git-workflow.json"
        if git_workflow.exists():
            try:
                git_data = json.loads(git_workflow.read_text(encoding="utf-8"))
                if not isinstance(git_data, dict):
                    errors.append(".learning/git-workflow.json must contain an object")
                else:
                    if git_data.get("version") not in {None, 1}:
                        errors.append("git-workflow.json version must be 1")
                    if git_data.get("mode") not in {"branch", "worktree", "current", None}:
                        errors.append("git-workflow.json has invalid mode")
                    for key in ["base_branch", "base_commit", "exercise_branch"]:
                        if key in git_data and git_data[key] is not None and not isinstance(git_data[key], str):
                            errors.append(f"git-workflow.json {key} must be a string")
                    if "worktree_path" in git_data and git_data["worktree_path"] is not None and not isinstance(git_data["worktree_path"], str):
                        errors.append("git-workflow.json worktree_path must be a string or null")
                    for key in ["commit_status", "push_status", "pull_request_status"]:
                        if key in git_data and not isinstance(git_data[key], str):
                            errors.append(f"git-workflow.json {key} must be a string")
            except json.JSONDecodeError as exc:
                errors.append(f"invalid git-workflow.json: {exc}")
        evidence_map = state / "cache" / "evidence-map.json"
        if evidence_map.exists():
            try:
                evidence_data = json.loads(evidence_map.read_text(encoding="utf-8"))
                if not isinstance(evidence_data, dict):
                    errors.append(".learning/cache/evidence-map.json must contain an object")
                else:
                    for key in ["native_sections", "inferred_evidence"]:
                        if key in evidence_data and not isinstance(evidence_data[key], list):
                            errors.append(f"evidence-map.json {key} must be a list")
                    for section in evidence_data.get("native_sections", []):
                        if not isinstance(section, dict):
                            errors.append("evidence-map.json native section must be an object")
                        elif section.get("source_kind") not in {None, "native"}:
                            errors.append("evidence-map.json native section has invalid source_kind")
                    for item in evidence_data.get("inferred_evidence", []):
                        if not isinstance(item, dict):
                            errors.append("evidence-map.json inferred item must be an object")
                        elif item.get("source_kind") not in {None, "inferred"}:
                            errors.append("evidence-map.json inferred item has invalid source_kind")
            except json.JSONDecodeError as exc:
                errors.append(f"invalid evidence-map.json: {exc}")
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
        exercises_dir = state / "exercises"
        if exercises_dir.exists() and not exercises_dir.is_dir():
            errors.append(".learning/exercises must be a directory")
        for manifest in exercises_dir.glob("*/manifest.json") if exercises_dir.is_dir() else []:
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{manifest}: invalid JSON: {exc}")
                continue
            if not isinstance(data, dict):
                errors.append(f"{manifest}: manifest must contain an object")
                continue
            questions = data.get("questions")
            if not isinstance(questions, list) or not questions:
                errors.append(f"{manifest}: questions must be a non-empty list")
                continue
            question_ids = [item.get("id") for item in questions if isinstance(item, dict)]
            if len(question_ids) != len(set(question_ids)):
                errors.append(f"{manifest}: duplicate question IDs")
            active = data.get("active_question")
            if active is not None and active not in question_ids:
                errors.append(f"{manifest}: active_question does not match a question")
            evidence_plan = data.get("evidence_plan")
            if evidence_plan is not None:
                if not isinstance(evidence_plan, dict):
                    errors.append(f"{manifest}: evidence_plan must be an object")
                else:
                    for key in ["native", "inferred", "proof_questions", "finish_gates"]:
                        if key in evidence_plan and not isinstance(evidence_plan[key], list):
                            errors.append(f"{manifest}: evidence_plan {key} must be a list")
                    for item in evidence_plan.get("native", []) + evidence_plan.get("inferred", []):
                        if not isinstance(item, dict):
                            errors.append(f"{manifest}: evidence_plan section must be an object")
                    for response in evidence_plan.get("proof_responses", []):
                        if not isinstance(response, dict):
                            errors.append(f"{manifest}: proof response must be an object")
            allowed_statuses = {"not-started", "scaffolded", "in-progress", "hinted", "submitted", "verified", "needs-revision", "mastered"}
            for item in questions:
                if not isinstance(item, dict):
                    errors.append(f"{manifest}: each question must be an object")
                elif item.get("status") not in allowed_statuses:
                    errors.append(f"{manifest}: invalid question status for {item.get('id')!r}")
    result = {"root": str(root), "valid": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
