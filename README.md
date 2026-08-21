# code-buddy

`code-buddy` is an installable Agent Skills suite for learning from almost any local repository or existing codebase. It supports continuous multiple-choice quizzes, flexible day or topic or file targeting, repository-aware teaching, guided exercises, code examination, explanations, review, and Markdown progress tracking. The three zero-to-hero courses are supported examples, not a limitation.

## Install

Install the complete suite from its Git repository with the open skills installer:

```bash
npx skills add codeKobby/code-buddy --all
```

Install only selected commands:

```bash
npx skills add codeKobby/code-buddy --skill quiz --skill assess --skill progress
```

Target specific agents:

```bash
npx skills add codeKobby/code-buddy --all \
  -a claude-code -a codex -a cline -a opencode
```

Install globally instead of only in the current project:

```bash
npx skills add codeKobby/code-buddy --all --global
```

The installer can use symlinks for a shared source of truth or copies when symlinks are unavailable. Update later with `npx skills update`.

## Interactive choices

Whenever code-buddy asks the learner to choose a goal, experience level, curriculum length, study schedule, lesson format, quiz count, difficulty, hint level, assessment mode, or next action, it should render the options as selectable questions when the current coding agent supports interactive choices. In text-only agents, it presents the same options as numbered or lettered choices and accepts the option label or a natural-language response. Stored answers are not asked again unless the learner wants to change them.

The continuous quiz itself uses the same interaction model: learners can click an A–D option where supported, or reply with a letter, number, or exact option text.

## Commands

| Command | Purpose |
| --- | --- |
| `/setup-learning` | Detect the repository course and initialize `.learning/`. |
| `/teach` | Teach one focused concept with an example, trace, and task. |
| `/quiz` | Run a continuous A–D quiz and continue after every answer. |
| `/exercise` | Select or create a concrete learner-owned exercise. |
| `/assess` | Review code, diffs, answers, output, or exercise artifacts. |
| `/explain` | Explain a concept, error, code block, or assessment comment. |
| `/review` | Practise weak, overdue, or recently corrected topics. |
| `/progress` | Regenerate the evidence-based progress dashboard. |
| `/next` | Recommend the smallest next learning action. |
| `/learn` | Review, search, correct, archive, or export durable learning records and project vocabulary. |

## Quiz examples

```text
/quiz
/quiz 1
/quiz 01
/quiz 001
/quiz day 1
/quiz day one
/quiz day-001
/quiz lesson 1
/quiz variables
/quiz "How Programs Run"
/quiz day 1 --count 10
/quiz resume
/quiz progress
```

A day quiz defaults to ten questions and a topic quiz to five. Each question has four options, A through D. After the learner answers, the skill explains the result and immediately presents the next question. Sessions are saved after every answer under `.learning/quiz-sessions/` and can be resumed.

## Learning state

The skill stores learner-specific state in the current repository, not in the skill package. Setup drafts `PROJECT_MAP.md`, `PROJECT_GLOSSARY.md`, and `CURRICULUM.md`, shows concise summaries, and asks the learner to confirm before writing durable files. Lessons, attempts, assessments, quiz reports, learning records, and progress topics link to one another by relative artifact paths. `/learn` lets the learner review, search, correct, archive, or export this memory; it never silently records every conversation.

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
└── lessons/
```

The skill distinguishes exposure, retrieval, implementation, and transfer. A high quiz score is useful retrieval evidence but does not by itself establish coding mastery.

## Compatibility with arbitrary codebases

The suite first reads the current repository’s own README files, documentation, source tree, tests, examples, issue descriptions, package configuration, and conventions. If it finds a day index or curriculum guide, it supports natural day and lesson commands. If it finds no formal curriculum, learners can target a file, symbol, function, test, feature, bug, pull request, or project milestone directly.

Examples include:

```text
/teach src/parser.py
/quiz tests/parser.test.ts
/exercise fix the failing login test
/assess src/components/Checkout.tsx
/explain this compiler error
```

The suite recognizes the user’s JavaScript/TypeScript, Python cybersecurity, and React/Next.js repositories from their own standards, but those are supported examples rather than a hard-coded boundary. For any other language or framework, the project’s own documentation, tests, conventions, and learner-stated goal become the source of truth. Cybersecurity tasks remain local, synthetic, authorized, bounded, and explicit about evidence and cleanup.

## Initialization and on-demand lessons

`/setup-learning` first classifies the workspace as a structured course, source project, hybrid, or sparse repository. It then asks the learner selectable questions about goals, experience, known concepts, available time, preferred activities, output mode, and execution boundaries. For a source project, it creates `.learning/PROJECT_MAP.md` and `.learning/CURRICULUM.md`: a compact daily roadmap derived from the project’s dependencies, technologies, source structure, tests, and milestones.

It does **not** generate every future lesson. When the learner selects a day, topic, file, function, component, test, bug, or feature, code-buddy produces the detailed lesson on demand. Markdown is recommended because the lesson can be revisited and assessed later:

```text
/teach day 03
/teach day 03 --inline
/teach src/parser.py --both
```

Generated Markdown lessons cite real repository-relative paths, symbols, tests, and exact line ranges with short source excerpts. The agent never guesses line numbers and redacts secrets or sensitive data.

## Local validation

From this distribution directory:

```bash
python3 shared/scripts/detect_course.py /path/to/course
python3 shared/scripts/normalize_target.py day one
python3 shared/scripts/validate_state.py /path/to/course
python3 shared/scripts/update_progress.py /path/to/course
```

The `skills/` directory contains the separately installable command skills. The `shared/` directory contains reference material and deterministic helpers used during development and validation.
