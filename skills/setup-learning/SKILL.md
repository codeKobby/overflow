---
name: setup-learning
description: Initialize code-buddy in any local repository or programming-course codebase by classifying the workspace, interviewing the learner, mapping documentation and source structure, creating a lightweight daily curriculum, and preparing durable .learning state without generating every lesson. Use when starting code-buddy or when the user asks to set up learning progress.
license: MIT
metadata:
  package: code-buddy
  version: "0.2.0"
---

# Setup Learning

Initialize a repository-local learning workspace. Create the map and roadmap first; generate full lessons only when the learner selects a day, topic, file, symbol, test, bug, feature, or milestone. Present every meaningful setup choice as a selectable question when the agent supports interactive options; otherwise show numbered or lettered options and accept text equivalents. Read [interactive-choices.md](references/interactive-choices.md).

## Classify the repository

1. Identify the Git worktree root.
2. Inspect README files, documentation, source directories, tests, examples, issue descriptions, package configuration, build scripts, curriculum files, lesson standards, exercise files, and documented checks.
3. Classify the workspace as `structured-course`, `source-project`, `hybrid`, or `sparse`.
4. Show the evidence used for classification and ask the learner to select the correct classification or choose `Other/Not sure`.

A structured course has an ordered day index, lessons, exercises, hints, solutions, or standards. A source project has source code, tests, documentation, manifests, build scripts, issues, or examples without a formal course sequence. A hybrid has both. A sparse repository has an unclear entry point or insufficient documentation.

## Interview the learner

Ask progressively rather than presenting one large questionnaire. Render each item as selectable options when possible, with `Other`, `Not sure`, and `Skip for now` where appropriate:

1. What should you be able to do with this repository? Offer `understand`, `contribute`, `debug`, `extend`, `maintain`, `prepare for interviews`, and `Other`.
2. What is your programming experience and experience with the main technologies? Offer beginner, familiar, intermediate, advanced, and `Not sure`.
3. Which concepts do you already know? Offer a repository-derived multi-select list plus `None yet`, `All of these`, and `Other`.
4. How much time can you study per day and how many days per week? Offer short, moderate, and extended schedules.
5. Do you prefer reading, building, debugging, or a mixture? Offer single or multiple selections.
6. Should generated lessons be Markdown, inline, or both? Recommend Markdown and explain why.
7. Which commands, files, services, dependencies, or external systems must not be touched? Offer detected risky areas plus `None` and `Other`.

Accept `unknown`, record assumptions, and let the learner revise the answers later. Do not ask again when a stored answer is still valid.

## Build the lightweight plan

For a structured course, import and map the existing sequence instead of rewriting it. For a source project, inspect dependency order, entry points, concepts, symbols, tests, milestones, and likely prerequisites, then propose a 7-, 14-, 21-, or 30-day curriculum based on the learner’s available time and goal. For a hybrid project, connect the course sequence to project milestones. For a sparse repository, create only a provisional map and ask for a starting path.

Create these planning artifacts:

```text
.learning/
├── CONFIG.md
├── MISSION.md
├── PROJECT_MAP.md
├── CURRICULUM.md
├── PROGRESS.md
├── progress.json
├── quiz-sessions/
├── attempts/
├── assessments/
├── learning-records/
├── lessons/
└── cache/
```

`PROJECT_MAP.md` records repository structure, entry points, technologies, important symbols, tests, commands, risks, and unknowns. `CURRICULUM.md` records daily outcomes, concepts, source anchors, prerequisites, activities, evidence, verification, and review targets.

Do **not** generate all future lessons, full code walkthroughs, complete solutions, or large quiz banks during setup. The initializer creates planning metadata only. Lesson generation is on demand.

## Configure output

Store the learner’s default in `.learning/CONFIG.md`. Present output mode as a selectable question. Use Markdown by default because it is durable, searchable, citable, and reviewable. Support overrides such as:

```text
/teach day 03
/teach day 03 --inline
/teach day 03 --both
```

End setup by showing `/teach`, `/quiz`, `/exercise`, `/assess`, `/progress`, and `/next` examples for the detected workspace.

## Safety and boundaries

For Python cybersecurity, read and record the repository’s safety and lab rules before enabling command execution. Default to local, synthetic, bounded practice and ask before running checks.

For any repository, preserve existing files and learner records. Ask before installing dependencies, modifying source code, running commands with side effects, accessing services, or reading sensitive files. Never copy secrets, tokens, private keys, or sensitive personal data into generated lessons.
