# code-buddy

`code-buddy` is an installable Agent Skills suite for learning from almost any local repository or existing codebase. It supports continuous multiple-choice quizzes, flexible day or topic or file targeting, repository-aware teaching, guided exercises, code examination, explanations, review, and Markdown progress tracking. The three zero-to-hero courses are supported examples, not a limitation.

## Install

Install the complete suite from its Git repository with the open skills installer:

```bash
npx skills add <owner>/code-buddy --all
```

Install only selected commands:

```bash
npx skills add <owner>/code-buddy --skill quiz --skill assess --skill progress
```

Target specific agents:

```bash
npx skills add <owner>/code-buddy --all \
  -a claude-code -a codex -a cline -a opencode
```

Install globally instead of only in the current project:

```bash
npx skills add <owner>/code-buddy --all --global
```

The installer can use symlinks for a shared source of truth or copies when symlinks are unavailable. Update later with `npx skills update`.

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

The skill stores learner-specific state in the current repository, not in the skill package:

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

## Local validation

From this distribution directory:

```bash
python3 shared/scripts/detect_course.py /path/to/course
python3 shared/scripts/normalize_target.py day one
python3 shared/scripts/validate_state.py /path/to/course
python3 shared/scripts/update_progress.py /path/to/course
```

The `skills/` directory contains the separately installable command skills. The `shared/` directory contains reference material and deterministic helpers used during development and validation.
