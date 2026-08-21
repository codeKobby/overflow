---
name: setup-learning
description: Initialize overflow in any local repository or programming-course codebase by classifying the workspace, interviewing the learner, mapping documentation and source structure, drafting a project map, glossary, and lightweight daily curriculum, and asking for confirmation before writing durable .learning state. Use when starting overflow or when the user asks to set up learning progress.
license: MIT
metadata:
  package: overflow
  version: "0.3.0"
---

# Setup Learning

Initialize a repository-local learning workspace. Create the map, glossary, and roadmap first; generate full lessons only when the learner selects a day, topic, file, symbol, test, bug, feature, or milestone. Present every meaningful choice as a selectable question when the agent supports interactive options; otherwise show numbered or lettered options and accept text equivalents. Read [interactive-choices.md](references/interactive-choices.md).

## Classify the repository

1. Identify the Git worktree root.
2. Inspect README files, documentation, source directories, tests, examples, issue descriptions, package configuration, build scripts, curriculum files, lesson standards, exercise files, hints, solutions, self-checks, `Prove it`, `Finish line`, reflection, verification, and documented checks.
3. Run the evidence-section detector on the selected course or source-project slice and classify each match as native or inferred.
4. Classify the workspace as `structured-course`, `source-project`, `hybrid`, or `sparse`.
5. Show the evidence used for classification and ask the learner to select the correct classification or choose `Other/Not sure`.

A structured course has an ordered day index, lessons, exercises, hints, solutions, standards, or native evidence sections such as Practice, Prove it, Finish line, or self-assessment. A source project has source code, tests, documentation, manifests, build scripts, issues, or examples without a formal course sequence; propose clearly labelled inferred proof and completion evidence from those artifacts. A hybrid has both. A sparse repository has an unclear entry point or insufficient documentation.

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

## Draft the project artifacts

For a structured course, import and map the existing sequence instead of rewriting it. For a source project, inspect dependency order, entry points, concepts, symbols, tests, milestones, and likely prerequisites, then propose a 7-, 14-, 21-, or 30-day curriculum based on the learner’s available time and goal. For a hybrid project, connect the course sequence to project milestones. For a sparse repository, create only a provisional map and ask for a starting path.

Draft these files before writing their durable versions:

```text
.learning/PROJECT_MAP.draft.md
.learning/PROJECT_GLOSSARY.draft.md
.learning/CURRICULUM.draft.md
```

`PROJECT_MAP.draft.md` records repository structure, entry points, technologies, important symbols, tests, commands, risks, and unknowns. `PROJECT_GLOSSARY.draft.md` records project terms, abbreviations, symbols, aliases, plain-language definitions, and source anchors. `CURRICULUM.draft.md` records daily outcomes, concepts, source anchors, prerequisites, activities, a native-or-inferred evidence plan, verification, proof questions, finish-line gates, and review targets.

Show a compact summary of each draft. Then ask a selectable confirmation question:

- Accept all drafts and create the learning workspace (recommended).
- Revise the project map.
- Revise the glossary.
- Revise the curriculum.

If the agent limits a question to four options, ask revision questions sequentially. Do not write `PROJECT_MAP.md`, `PROJECT_GLOSSARY.md`, or `CURRICULUM.md` until the learner accepts the drafts. If state already exists, show the proposed diff and ask before reconciling it.

## Create durable state after confirmation

After acceptance, rename or rewrite the approved drafts as:

```text
.learning/
├── CONFIG.md
├── MISSION.md
├── PROJECT_MAP.md
├── PROJECT_GLOSSARY.md
├── CURRICULUM.md
├── PROGRESS.md
├── progress.json
├── quiz-sessions/
├── attempts/
├── assessments/
├── learning-records/
├── lessons/
└── cache/
    └── evidence-map.json
```

Initialize `progress.json` with repository type, current target, empty topics, and version 3. After learner confirmation, cache the compact native/inferred evidence inventory at `.learning/cache/evidence-map.json`. Do not claim mastery from setup. The plan is metadata only: do not generate all future lessons, full walkthroughs, complete solutions, or large quiz banks.

## Configure output and next steps

Store the learner’s default in `.learning/CONFIG.md`. Present output mode as a selectable question. Use Markdown by default because it is durable, searchable, citable, and reviewable. Support overrides such as:

```text
/teach day 03
/teach day 03 --inline
/teach day 03 --both
```

End setup by showing `/teach`, `/quiz`, `/exercise`, `/hint`, `/assess`, `/learn`, `/progress`, and `/next` examples for the detected workspace. Explain that `/learn` reviews or corrects durable learning records and glossary terms, and that `/assess` can trigger native or inferred proof questions after implementation checks.

## Safety and boundaries

For Python cybersecurity, read and record the repository’s safety and lab rules before enabling command execution. Default to local, synthetic, bounded practice and ask before running checks.

For any repository, preserve existing files and learner records. Ask before installing dependencies, modifying source code, running commands with side effects, accessing services, or reading sensitive files. Never copy secrets, tokens, private keys, or sensitive personal data into generated lessons or glossary entries.
