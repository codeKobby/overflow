# Repository Detection

Use this procedure before teaching, quizzing, assessing, or reporting progress.

## Locate the worktree

1. Identify the Git worktree root.
2. Search for README files, documentation, source directories, tests, examples, issue descriptions, package manifests, build scripts, day indexes, curriculum guides, lesson standards, exercises, hints, solutions, practice directories, starter files, self-check lists, and verification commands.
3. Search `.learning/exercises/*/manifest.json` for an existing active exercise and record its `exercise_id`, `active_question`, source hash, and status before creating another scaffold.
4. Run `scripts/discover_evidence.py` on the selected lesson or project slice. Record native section roles, source paths, headings, line ranges, links, source hashes, confidence, and inferred evidence steps in `.learning/cache/evidence-map.json` after learner confirmation.
5. Record only relevant paths and small metadata in `.learning/cache/course-map.json`; do not copy the whole repository into context.

## Classify the workspace

### `structured-course`

Signals include an ordered day index, lesson files, exercise/hint/solution separation, lesson templates, quality standards, or a course README. Preserve its sequence and standards.

### `source-project`

Signals include source code, tests, README/docs, manifests, build scripts, examples, issues, and project milestones without a formal course sequence. Create a project map and propose a compact daily curriculum from dependency order and learner goals.

### `hybrid`

Signals include a course sequence plus an application or capstone. Keep the course map and connect it to project milestones.

### `sparse`

Signals include an unclear entry point, little documentation, missing tests, or an incomplete project. Ask the learner for a goal and starting path; mark assumptions and unknowns.

Always show the evidence used for classification and allow correction. Distinguish `native` sections found in the repository from `inferred` evidence steps proposed for a source project. Never claim that a repository contains a `Prove it` or `Finish line` section when discovery did not find one.

## Recognize known repositories

### JavaScript/TypeScript

Look for `COURSE_QUALITY_STANDARD.md`, `LESSON_TEMPLATE.md`, `package.json`, day folders, matched JavaScript and TypeScript examples, and separate practice files. Preserve runtime parity and use the documented project check.

### Python cybersecurity

Look for `EXERCISE_STANDARD.md`, `SAFETY_AND_LAB_RULES.md`, `SECURITY.md`, `pyproject.toml`, day folders, `practice/exercises.md`, `practice/hints.md`, `practice/solutions.md`, starter files, and local fixtures. Before any security exercise, read the safety and scope documents.

### React/Next.js

Look for `LESSON_STANDARD.md`, `MODERN_TOOLCHAIN.md`, `PROJECT_STRUCTURE_GUIDE.md`, `package.json`, day folders, separate practice files, starter files, and self-check lists. Distinguish JavaScript, React, and Next.js behavior.

## Resolve a target

Normalize explicit input in this order:

1. Direct file, directory, or URL-like repository-relative path.
2. Course selector.
3. Integer day/lesson number.
4. Number words such as `one`, `two`, or `twenty-one`.
5. Title, heading, symbol, function, test, keyword, topic, bug, feature, or milestone.
6. Saved current target.

Accept `day`, `lesson`, `d`, and common separators. Normalize leading zeroes, case, punctuation, and whitespace. For an invalid explicit number, show the nearest valid lessons and ask. For multiple title/topic matches, show the candidates and ask. Never silently select a different target.
