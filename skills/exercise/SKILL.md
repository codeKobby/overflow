---
name: exercise
description: Select or create a concrete programming exercise from the current repository or existing codebase, with inputs, outputs, acceptance criteria, evidence requirements, progressive hints, edge cases, and optional local verification. Use when the user asks for practice, wants to build a lesson’s exercise, fix a bug, or practise a project feature.
license: MIT
metadata:
  package: code-buddy
  version: "0.2.0"
---

# Code Buddy Exercise

Prefer the repository’s existing exercises, TODOs, failing tests, issue descriptions, examples, and project milestones over inventing a competing assignment. Resolve a requested day, lesson, topic, file, bug, feature, or current exercise. Present exercise type, difficulty, help level, verification permission, and output format as selectable questions when supported; otherwise use numbered or lettered text.

## Exercise contract

State the starting input or project state, the expected output or behavior, concepts already available, acceptance condition, evidence to save, and progressive hints. Use this progression when it matches the lesson:

1. Run the starter and record output.
2. Answer a question about values, control flow, state, or data shape.
3. Write or modify code against supplied input.
4. Apply the concept to a local, synthetic, or bounded problem.
5. Handle an edge case, malformed input, failure path, or negative test.
6. Attempt a stretch challenge only after the core task.

Ask the learner to attempt the work before showing a solution. Present the exercise’s next-step choices and help ladder interactively when supported: question, reminder, targeted hint, partial scaffold, comparable example, solution review.
 Inspect diffs and run documented checks only when allowed; do not silently implement the task.

For Python cybersecurity, require local or synthetic targets, explicit authorization, permitted actions, evidence, cleanup, and stop conditions. Do not use real credentials, public targets, private logs, or unauthorized systems. For other repositories, follow the project’s documented conventions and ask before modifying files or accessing external services.

Write an attempt record under `.learning/attempts/` when `--md` is requested. Tell the learner to use `/assess` with the file, diff, output, or explanation when they are ready.
