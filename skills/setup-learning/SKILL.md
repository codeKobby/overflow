---
name: setup-learning
description: Initialize code-buddy in any local repository or programming-course codebase by detecting documentation, source structure, tests, verification commands, safety rules, learner mission, output preferences, and durable .learning progress state. Use when starting code-buddy or when the user asks to set up learning progress.
license: MIT
metadata:
  package: code-buddy
  version: "0.1.0"
---

# Setup Learning

Initialize a repository-local learning workspace without changing course-owned curriculum files.

## Workflow

1. Identify the Git worktree root.
2. Inspect `DAY_INDEX.md`, curriculum guides, lesson standards, `README.md`, package configuration, source directories, tests, issue descriptions, lesson folders, exercise files, and documented checks.
3. Detect whether the repository is JavaScript/TypeScript, Python cybersecurity, React/Next.js, or another language/framework; if no course structure exists, create a project map from the codebase.
4. Report the detected course, root, lesson count, current lesson evidence, runtime, and safety documents before writing state.
5. Ask the learner for the concrete mission, available study time, preferred output mode (`inline`, `md`, or `both`), and whether documented local checks may run automatically.
6. Create `.learning/CONFIG.md`, `.learning/MISSION.md`, `.learning/progress.json`, `.learning/PROGRESS.md`, and lazy directories for sessions, attempts, assessments, records, and cache.
7. Preserve existing files. If state already exists, summarize it and ask before reconciling conflicting values.

## Initial state

Use this minimum structure:

```text
.learning/
├── CONFIG.md
├── MISSION.md
├── PROGRESS.md
├── progress.json
├── quiz-sessions/
├── attempts/
├── assessments/
└── learning-records/
```

Start `progress.json` with `version`, `course`, `current_lesson`, and an empty `topics` object. Do not claim mastery from setup. End by showing the learner how to run `/quiz`, `/teach`, `/exercise`, `/assess`, `/progress`, and `/next`.

## Safety

For a Python cybersecurity repository, read and record the repository’s safety and lab rules before enabling any command execution. Default to local, synthetic, bounded practice and ask before running checks.
