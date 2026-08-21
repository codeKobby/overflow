# code-buddy

`code-buddy` is an installable Agent Skills suite for learning from almost any local repository or existing codebase. It supports continuous multiple-choice quizzes, flexible day or topic or file targeting, repository-aware teaching, guided exercises, code examination, explanations, review, and Markdown progress tracking. The three zero-to-hero courses are supported examples, not a limitation.

## Install

Install the complete suite from its Git repository with the open skills installer:

```bash
npx skills add codeKobby/code-buddy --all
```

Install only selected commands:

```bash
npx skills add codeKobby/code-buddy --skill quiz --skill exercise --skill hint --skill assess --skill progress
```

Target specific agents:

```bash
npx skills add codeKobby/code-buddy --all \
  -a claude-code -a codex -a cline -a opencode -a antigravity
```

Install globally instead of only in the current project:

```bash
npx skills add codeKobby/code-buddy --all --global
```

The installer can use symlinks for a shared source of truth or copies when symlinks are unavailable. Update later with `npx skills update`.

## skills.sh directory

The package is listed in the [`skills.sh` directory](https://skills.sh/codekobby/code-buddy). There is no separate publishing command: the current skills ecosystem indexes public Git repositories through the normal `npx skills add` installation flow and its anonymous discovery telemetry. Users can also search for it with:

```bash
npx skills find code-buddy
```

For the official publishing and package-format guidance, see the [Vercel Agent Skills guide](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context). Review the repository and scripts before installation, as recommended for all agent skills.

## Agent compatibility

Compatibility is a first-class part of the package, not just a list of names. The complete matrix is maintained in [`compatibility/hosts.json`](compatibility/hosts.json), with user-facing guidance in [`compatibility/README.md`](compatibility/README.md). Tier A hosts have verified standard discovery contracts; Tier B hosts are installer-routed and require host-specific placement; Tier C hosts are bridge integrations. The repository also includes an optional Claude Code plugin manifest at [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and Codex picker metadata beside every skill.

| Tier | Hosts |
| --- | --- |
| A — native portable | Claude Code, Codex CLI, Cline, OpenCode, Google Antigravity, GitHub Copilot / VS Code |
| B — installer-routed | Cursor, Factory Droid, Kiro, Slate, Hermes |
| C — bridge | OpenClaw, GBrain |

Every host must preserve explicit invocation, progressive loading, relative references, selectable-question fallbacks, learner confirmation, source citations, and repository-local `.learning/` state. A host adapter must not silently add telemetry, external network calls, or destructive operations.

## Interactive choices

Whenever code-buddy asks the learner to choose a goal, experience level, curriculum length, study schedule, lesson format, quiz count, difficulty, hint level, assessment mode, or next action, it should render the options as selectable questions when the current coding agent supports interactive choices. In text-only agents, it presents the same options as numbered or lettered choices and accepts the option label or a natural-language response. Stored answers are not asked again unless the learner wants to change them.

The continuous quiz itself uses the same interaction model: learners can click an A–D option where supported, or reply with a letter, number, or exact option text.

## Commands

| Command | Purpose |
| --- | --- |
| `/setup-learning` | Detect the repository course and initialize `.learning/`. |
| `/teach` | Teach one focused concept with an example, trace, and task. |
| `/quiz` | Run a continuous A–D quiz and continue after every answer. |
| `/exercise` | Create or open a learner-owned, comment-marked exercise and set the active question. |
| `/hint` | Give progressive, non-spoiling help for the active exercise question. |
| `/assess` | Resolve the active question, optionally run approved checks, and assess the implementation. |
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
├── exercises/
├── attempts/
├── assessments/
├── learning-records/
└── lessons/
```

The skill distinguishes exposure, retrieval, implementation, and transfer. A high quiz score is useful retrieval evidence but does not by itself establish coding mastery.

## Comment-driven exercises

When `/exercise` opens a course question, it creates a learner-owned manifest under `.learning/exercises/<exercise-id>/` and gives each prompt a stable marker such as `CB-Q01`. The answer file keeps the question visible and places the learner’s code between `CB-ANSWER-START CB-Q01` and `CB-ANSWER-END CB-Q01`. The original lesson, hints, and solutions remain unchanged.

```python
# CB-Q01: Write a function that returns a safe greeting.
# CB-ANSWER-START CB-Q01
def safe_greeting(name: str) -> str:
    return ""  # replace this with your implementation
# CB-ANSWER-END CB-Q01
```

The manifest remembers the active question, so the learner can simply ask `/hint` or `/assess` without repeating the prompt. `/hint` escalates from an observation question to a concept pointer, targeted clue, partial pseudocode, comparable example, and—only after an attempt or explicit request—a solution review. Hints can be inserted into comments after confirmation.

`/assess` can inspect the changed region, ask permission to activate a commented draft or use a temporary copy, run documented checks, and record the real evidence. It reports correctness separately from reasoning, verification, edge cases, maintainability, complexity, and modernity. A solution that is correct but longer than necessary is not failed; it receives an explanation of a clearer or more idiomatic alternative and the trade-offs involved.

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
python3 shared/scripts/detect_hosts.py /path/to/course
python3 shared/scripts/normalize_target.py day one
python3 skills/exercise/scripts/parse_exercise_markers.py /path/to/course
python3 shared/scripts/validate_state.py /path/to/course
python3 shared/scripts/update_progress.py /path/to/course
python3 shared/scripts/validate_compatibility.py .
```

The `skills/` directory contains the separately installable command skills. The `shared/` directory contains reference material and deterministic helpers used during development and validation.
