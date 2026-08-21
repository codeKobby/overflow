---
name: assess
description: Assess a learner’s comment-marked overflow exercise by resolving its CB question ID, inspecting the linked prompt and answer region, optionally activating a reversible copy, running approved checks, and reporting correctness, reasoning, edge cases, maintainability, complexity, and modernity. Use when the learner asks to assess, grade, examine, verify, or review completed exercise code.
license: MIT
metadata:
  package: overflow
  version: "0.6.0"
---

# Overflow Assessment

Assess the learner’s actual evidence, not confidence or similarity to a canonical solution. Read `references/comment-driven-exercises.md` from the exercise skill when the manifest, marker, answer region, or hint state needs interpretation.

## Resolve the submission

1. Locate `.learning/exercises/*/manifest.json`. If there is no active manifest, ask the learner to run `/exercise` first.
2. Resolve an omitted question from the manifest’s `active_question`. If multiple exercises are active, present them as selectable choices or numbered options. Accept explicit IDs such as `CB-Q03` and normalise `CB-Q3` to the manifest ID.
3. Confirm that the marker exists and is unique. Read the linked prompt, source anchor, relevant lesson section, starter, acceptance criteria, approved checks, hint history, target files, answer region, the selected native-or-inferred evidence plan, and optional `.learning/git-workflow.json`. Detect linked `Practice`, `Prove it`, `Finish line`, self-assessment, verification, hints, solutions, and safety/scope artifacts without assuming fixed filenames.
4. Inspect the learner’s diff and the smallest necessary supporting files. If a branch or worktree is active, compare it with the recorded base commit and report changed paths, commits, and unpushed work. Do not open or reveal a solution file unless the learner explicitly requests a solution review.
5. After implementation and approved checks, ask one due native `Prove it` question or clearly labelled inferred proof question in chat. Then ask unresolved Finish line or self-assessment gates. Do not ask every question after every small attempt; use the repository’s order and the learner’s current evidence gaps.

## Verification permission

Before running code, present a selectable permission question when supported:

> The exercise lists these checks: `<commands>`. May I run them as written, using the current repository or a temporary copy? Choose: **Run all**, **Choose checks**, **Static inspection only**, or **Other**.

Run only documented or explicitly approved checks. If the answer is commented out, do not uncomment arbitrary repository code. Offer a reversible temporary copy or a separate executable answer file, and label the evidence as `draft-answer` until it has executed successfully. Never use a broad search-and-replace to remove comments. Treat staging, committing, pushing, opening a draft pull request, merging, branch deletion, and worktree removal as separate confirmation questions; assessment must never perform them as a side effect.

For security work, require local or synthetic targets, explicit authorization, bounded scope, evidence, cleanup, privacy, and stop conditions. Do not run network-facing or destructive commands by inference.

## Assess in separate dimensions

| Dimension | Required question |
| --- | --- |
| Correctness | Does the implementation satisfy the prompt and acceptance criteria? |
| Verification | Which approved checks actually ran, with their real exit status and output? |
| Reasoning | Can the learner explain the important decisions and behavior? |
| Edge cases | Does it handle a meaningful boundary, invalid input, empty input, or failure path? |
| Maintainability | Is it readable, focused, structured, and consistent with repository conventions? |
| Complexity | Is its time, space, or operational cost appropriate when relevant? |
| Modernity | Does it use current idiomatic APIs for the repository’s language and toolchain? |
| Transfer | Can the learner adapt it to a changed input or nearby task? |
| Safety | Are security boundaries and evidence obligations satisfied? |
| Proof response | Can the learner answer the native or inferred direct question in their own words and connect it to source evidence? |
| Completion gate | Has the learner met the native or inferred Finish line, including reproducibility, repair, limitation, or transfer where required? |

A correct but long implementation is still correct. Report `correctness: pass` when acceptance is met, then give an optional shorter, clearer, or more modern alternative with trade-offs. Do not call a solution wrong only because another implementation is shorter. Do not require a modern API if the exercise intentionally teaches an older API or if the trade-off is not favorable.

## Report and state updates

For substantial work, write `.learning/assessments/YYYY-MM-DD-<exercise-id>-<question-id>.md`:

```md
# Assessment: <exercise title> — <question ID>

- Status: <verified | needs-revision | submitted>
- Correctness: <pass | partial | not-demonstrated>
- Evidence mode: <executed-implementation | draft-answer | static-inspection>
- Source: <relative prompt path and line anchor>
- Answer region: <relative path and marker>
- Hints used: <levels and links>

## What is demonstrated

## Verification

## Quality and maintainability

## Complexity and modernity

## Edge case or limitation

## Explanation check

## Next action
```

Record exact files, source-anchor freshness, hints used, permission, checks actually run, output excerpts, uncertainty, the learner’s explanation, proof responses, source provenance (`native` or `inferred`), unresolved completion gates, branch/worktree, base commit, changed paths, commit SHAs, push status, and optional pull-request URL. Update the question status and `active_question` only after recording the result. Link the report from the attempt record, affected topic, `progress.json`, and `PROGRESS.md` when those files exist.

Use `not-demonstrated`, `emerging`, `reliable`, or `transferable` for the overall learning verdict. `mastered` requires explanation and transfer evidence; a green test alone proves only the tested condition.

Never fabricate output, claim a check ran when it did not, or silently implement the exercise.
