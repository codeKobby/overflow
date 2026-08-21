---
name: exercise
description: Create or open repository-native coding exercises with stable CB question markers and learner-owned answer regions, then track the active question for `/hint` and `/assess`. Use when the learner asks for practice, a daily exercise file, a question scaffold, help with an exercise, or assessment of completed code.
license: MIT
metadata:
  package: overflow
  version: "0.6.0"
---

# Overflow Exercise

Turn an existing course exercise, TODO, failing test, issue, project milestone, or source-code task into a learner-owned, comment-driven work item. The learner should be able to answer in code, ask `/hint` without repeating the question, run the approved checks, and invoke `/assess` when ready.

## Choose the exercise source

Prefer the repository’s own numbered exercises, `practice/exercises.md`, READMEs, self-check lists, TODOs, failing tests, issue descriptions, examples, and project milestones. Do not invent a competing assignment when an authoritative exercise exists. Read `references/comment-driven-exercises.md` for the marker and manifest contract.

Resolve the learner’s target in this order: explicit file, directory, day, lesson, topic, symbol, test, bug, feature, milestone, then saved current target. Present ambiguous targets as selectable questions or numbered options and ask before continuing.

## Create or open the learner workspace

When the learner asks to start an exercise, present choices for the source, question or range, answer location, hint level, and verification permission. Then:

1. Read the source prompt, relevant lesson, starter files, hints, solution policy, repository standards, tests, and documented commands. Cache only path metadata and source hashes.
2. Keep course-owned files unchanged by default. Create a learner-owned workspace under `.learning/exercises/<exercise-id>/` or a clearly marked reversible patch in a copied starter file.
3. Add stable IDs such as `CB-Q01` and answer delimiters such as `CB-ANSWER-START CB-Q01` and `CB-ANSWER-END CB-Q01`. Use the file’s comment syntax. If it is unknown or insertion would be unsafe, use a companion Markdown answer file.
4. Write `.learning/exercises/<exercise-id>/manifest.json` with the prompt source path, source hash, question IDs, source anchors, target files, answer regions, acceptance criteria, approved checks, active question, hint level, and status.
5. Leave a clear TODO or meaningful blank inside each answer region. Never overwrite a non-empty learner answer without showing a diff and receiving confirmation.
6. Set `active_question` to the first unanswered question and tell the learner exactly which file and marker to edit.

For a numbered Markdown prompt, the deterministic helper can create a first scaffold:

```bash
python3 <overflow-skill>/scripts/scaffold_exercise.py \
  day_1_setup_and_safe_practice/practice/exercises.md \
  --root . \
  --exercise-id day-01-setup \
  --out .learning/exercises/day-01-setup
```

Use `scripts/parse_exercise_markers.py` to inspect existing markers before assessment. Helpers do not decide whether an answer is correct; the agent must still read the prompt and repository standards.

## Learner loop

1. **Attempt.** The learner edits only the answer region or declared target files, keeping the question marker intact.
2. **Ask for help.** `/hint` resolves the active question and provides the lowest useful rung of the progressive hint ladder. Hints may be placed in comments only after the learner confirms the proposed insertion.
3. **Verify.** Offer the documented command or test as a selectable permission question. If the answer is a draft inside comments, ask whether to activate a reversible copy or use a separate executable answer file. Never uncomment arbitrary repository code silently.
4. **Assess.** `/assess` resolves the active marker, inspects the prompt and changed region, runs only approved checks after permission, and writes evidence.
5. **Advance.** On completion, update the question status and move `active_question` to the next unanswered or needs-revision question. Tell the learner what is active now.

A question can be `not-started`, `scaffolded`, `in-progress`, `hinted`, `submitted`, `verified`, `needs-revision`, or `mastered`. A passing check can verify correctness without proving explanation, transfer, or mastery.

## Assessment contract

Assess independent dimensions rather than comparing text with a solution:

| Dimension | Assess |
| --- | --- |
| Correctness | Prompt acceptance criteria and observable behavior. |
| Verification | Actual commands, tests, exit status, and output. |
| Reasoning | Learner explanation of the important decisions. |
| Edge cases | Boundary, invalid, empty, failure, or changed input. |
| Maintainability | Readability, focus, structure, and repository conventions. |
| Complexity | Appropriate time, space, or operational cost when relevant. |
| Modernity | Current idiomatic APIs for this repository’s toolchain, with trade-offs. |
| Transfer | Adaptation to a changed input or adjacent task. |
| Safety | Authorization, scope, privacy, evidence, cleanup, and stop conditions for security work. |

A correct but long approach remains correct. Report `correctness: pass`, then explain a shorter, clearer, or more modern alternative and why it may or may not be preferable. Do not penalize an intentionally taught legacy approach merely for being older, and do not require a newer API without evidence that it improves this task.

## Safety

Inspect the diff before running anything. Ask before changing source files, installing dependencies, accessing services, or executing commands not already documented by the repository or explicitly approved by the learner. Prefer a temporary copy for activation tests. For Python cybersecurity, use only local, synthetic, authorized, bounded targets and preserve evidence, cleanup, privacy, and stop conditions.

Ask the learner to attempt the work before showing a solution. Hints, pseudocode, comparable examples, and solution reviews are distinct levels; never expose `solutions.md` merely because it exists. When Markdown is requested, write an attempt record under `.learning/attempts/` linking the source lesson, question marker, files changed, hints used, checks run, and next assessment path.
