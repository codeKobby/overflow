# Overflow Command Reference

Use this reference when `/help` receives a command, topic, `examples`, `quickstart`, or `troubleshooting` target. Keep the response focused on the selected command and offer a link to the next useful command rather than dumping every section.

## Quick start

Start a new repository with:

```text
/setup-learning
```

Then choose a target with `/teach`, `/quiz`, or `/exercise`. A typical implementation loop is:

```text
/exercise day 1
/hint
/assess
/progress
/next
```

Use `/help <command>` for one command, `/help examples` for common workflows, and `/help state` for the `.learning/` files.

## Command map

| Command | What it does | Typical arguments |
| --- | --- | --- |
| `/help` | Explains commands, arguments, workflows, files, and troubleshooting. | `quiz`, `exercise`, `examples`, `state`, `troubleshooting` |
| `/setup-learning` | Classifies the current repository, interviews the learner, drafts the map/glossary/curriculum, asks about optional Git isolation, and asks before writing durable state. | none; answers to setup questions are stored |
| `/teach` | Produces one focused lesson from real repository sources, with citations, a mental model, example, prediction, and task. | day, lesson, topic, path, symbol, test, bug, feature, `--inline`, `--both` |
| `/quiz` | Runs a continuous single-answer A–D quiz, grading each response before showing the next question. | day, lesson, topic, `--count N`, `resume`, `progress` |
| `/exercise` | Creates or opens a learner-owned exercise with stable question markers, answer regions, an active question, and approved checks. | day, lesson, topic, path, question ID, issue, bug, feature |
| `/hint` | Gives progressive, non-spoiling help for the active exercise question. | question ID, `level N`, `comment`, `stronger` |
| `/assess` | Resolves the active question, asks before execution, runs approved checks, and reports correctness separately from quality. | file, diff, answer, question ID, `--inline`, `--both`, `static only` |
| `/explain` | Explains one concept, error, code block, output, or assessment comment in the repository’s context. | concept, error, code, path, symbol, test |
| `/review` | Runs retrieval practice on weak, overdue, or recently corrected topics. | topic, `due`, `weak`, `recent` |
| `/progress` | Recomputes evidence-based progress and shows exposure, retrieval, implementation, transfer, overdue review, and next gaps. | none; optionally a topic or path |
| `/next` | Recommends the smallest next learning action from current state and evidence gaps. | none; optionally `short`, `review`, or `implementation` |
| `/learn` | Reviews, searches, corrects, prunes, or exports durable learning memory. | `review`, `search`, `glossary`, `correct`, `prune`, `export` |

## `/setup-learning`

Use this first in a new repository. Overflow identifies the Git worktree, reads project documentation and standards, and classifies the workspace as `structured-course`, `source-project`, `hybrid`, or `sparse`. It then asks about the learner’s goal, experience, available time, preferred activity, output mode, optional Git isolation, and execution boundaries. Git choices are local branch, separate worktree, current branch, or decide later.

For a course, setup preserves the existing day or lesson order. For a source project, it creates a compact daily curriculum from technologies, dependencies, source structure, tests, and milestones without pre-generating every lesson. The learner confirms the draft before durable files are written. Before creating a branch or worktree, Overflow shows current status, dirty paths, base branch, base commit, target name, and exact command.

```text
/setup-learning
/setup-learning source project
/setup-learning I want to understand the authentication flow
```

## `/help git`

Use `/help git` for the optional Git exercise workflow. The recommended path is:

```text
/setup-learning
# choose local exercise branch or separate worktree
/exercise day 01
/assess
# optionally confirm stage, commit, push, or draft pull request separately
```

Overflow uses `overflow/exercise/<slug>` branch names by default, refuses to branch from a dirty or detached checkout, checks for branch/worktree collisions, and records `.learning/git-workflow.json` only after successful creation. It never silently stashes, resets, cleans, commits, pushes, opens a pull request, merges, deletes a branch, or removes a worktree.

The deterministic helper can inspect or plan without changing files:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . --mode inspect --output json
python3 <overflow-skill>/scripts/git_workflow.py . --mode plan --slug day-01-q03 --output json
```

Creation requires learner confirmation and an explicit apply step:

```bash
python3 <overflow-skill>/scripts/git_workflow.py . --mode branch --slug day-01-q03 --apply
python3 <overflow-skill>/scripts/git_workflow.py . --mode worktree --slug parser-basics --worktree ../project-overflow-parser-basics --apply
```

A commit, push, draft pull request, merge, branch deletion, and worktree cleanup are separate decisions. Git artifacts support review and assessment but do not prove learning mastery.

## `/teach`

Use `/teach` when the learner wants a lesson rather than a grade. The target may be a day, title, topic, file, symbol, test, bug, feature, or project milestone. Overflow reads only the relevant source slice and cites repository-relative paths, exact line ranges, symbols, headings, and nearby tests.

Markdown is the recommended output because it can be revisited and assessed later. Use `--inline` for chat-only teaching and `--both` for both a saved Markdown lesson and a concise chat explanation.

```text
/teach day 03
/teach day one
/teach src/parser.py
/teach parseRequest --both
/teach "How Programs Run" --inline
```

## `/quiz`

Use `/quiz` for continuous retrieval practice. Day quizzes default to ten questions and topic quizzes to five. Each question has four options labelled A–D, and the next question appears immediately after the learner answers. The learner may answer with a letter, option number, exact option text, or an interactive selection.

```text
/quiz
/quiz 1
/quiz 01
/quiz 001
/quiz day 1
/quiz day one
/quiz day-001
/quiz variables
/quiz day 1 --count 10
/quiz resume
/quiz progress
```

Inside a quiz, the learner may use `hint`, `explain`, `pause`, `save`, `progress`, `finish`, `quit`, or `back`. A quiz score is retrieval evidence; it does not by itself establish coding implementation mastery.

## `/exercise`

Use `/exercise` for hands-on implementation. Overflow prefers existing repository prompts, starter files, TODOs, failing tests, issue descriptions, and project milestones. It keeps course-owned lesson and solution files unchanged and creates learner-owned state under `.learning/exercises/<exercise-id>/`.

The generated manifest remembers the source prompt, source hash, stable IDs such as `CB-Q01`, answer-region delimiters, target files, acceptance criteria, checks, hint level, attempts, status, and `active_question`.

```text
/exercise day 1
/exercise "Functions and Parameters"
/exercise src/parser.py
/exercise fix the failing login test
/exercise CB-Q03
```

A typical answer region looks like:

```python
# CB-Q01: Return a safe greeting.
# CB-ANSWER-START CB-Q01
def safe_greeting(name: str) -> str:
    return ""  # replace this with your implementation
# CB-ANSWER-END CB-Q01
```

Keep the question marker intact. The active question allows `/hint` and `/assess` to work without repeating the full prompt.

## `/hint`

Use `/hint` when the learner is stuck or wants a clue without a full solution. With no argument, it resolves the manifest’s `active_question`. The hint ladder begins with expected-versus-observed behavior, then points to a concept or source section, identifies the next decision, gives partial pseudocode, gives a comparable example, and only performs a complete solution review after an attempt or explicit request.

```text
/hint
/hint CB-Q03
/hint stronger
/hint level 3
/hint comment
```

`/hint comment` shows the proposed comment before inserting a marked `CB-HINT-START` / `CB-HINT-END` block. Hints never replace the learner’s answer and do not run code.

## `/assess`

Use `/assess` after an attempt. Overflow resolves the active question, reads the linked prompt and answer region, inspects the diff, and asks before activating a commented draft or running checks. It runs only documented or explicitly approved commands and records real evidence.

```text
/assess
/assess CB-Q03
/assess src/parser.py
/assess --static-only
/assess --both
```

The assessment separates correctness, verification, reasoning, edge cases, maintainability, complexity, modernity, transfer, and safety. A correct but long approach remains correct; overflow explains a clearer or more modern alternative with trade-offs instead of treating it as a failed answer.

If the repository has a native `Prove it`, `Finish line`, self-assessment, or reflection section, `/assess` uses it after implementation checks: it asks one direct-answer question at a time in chat, then asks only unresolved completion gates. If the repository has no equivalent, Overflow labels the source-grounded questions as **inferred** and cites the files, tests, or milestone used to create them. A passing test does not silently close unanswered proof questions.

## `/explain`

Use `/explain` for a focused explanation of a concept, error, code block, output, or assessment note. It should cite the relevant repository source and distinguish observed behavior from inference.

```text
/explain closures
/explain this TypeScript error
/explain src/auth/session.ts
/explain why this test fails
/explain the complexity feedback
```

## `/review`

Use `/review` when a topic is weak, overdue, or recently corrected. It should use retrieval questions, code tracing, small predictions, and transfer prompts rather than repeating a long lesson.

```text
/review
/review due
/review promises
/review weak parser
/review recent
```

## `/progress`

Use `/progress` to regenerate or inspect `PROGRESS.md` and `progress.json`. It reports evidence separately for exposure, retrieval, implementation, reasoning, verification, transfer, and safety, and links to lessons, quiz reports, attempts, assessments, and learning records. When available, it also shows native versus inferred section counts, proof questions due, and open Finish line gates.

```text
/progress
/progress parser
/progress day 3
```

## `/next`

Use `/next` when the learner does not know what to do next. Overflow chooses the smallest action that closes the largest evidence gap: setup blocker, overdue misconception, incomplete exercise, submitted answer awaiting assessment, or next curriculum target.

```text
/next
/next review
/next implementation
/next short
```

## `/learn`

Use `/learn` to manage durable memory deliberately. It can review records, search by topic/file/symbol/misconception, inspect or revise the project glossary, append a correction, prune stale records, or export a summary.

```text
/learn review
/learn search parser
/learn glossary
/learn correct
/learn prune
/learn export
```

Overflow should show proposed changes and ask before editing or archiving durable records.

## Output modes

Markdown is the default for lessons and substantial assessments. Use `--inline` when the learner wants only chat output and `--both` when they want both a durable file and a concise inline summary. The output mode is remembered in `.learning/CONFIG.md` and should not be asked again unless the learner wants to change it.

## Learning state

Overflow keeps learner-specific state in the current repository:

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
├── lessons/
└── cache/
    └── evidence-map.json

Optional Git state:

```text
.learning/git-workflow.json
```

Existing `.learning/` state is reused when the package is renamed or reinstalled. Do not delete it during troubleshooting.

## Troubleshooting

If a command is not available, verify the package was installed with `npx skills add codeKobby/overflow --all` and that the current host’s skill directory is configured. If the repository has not been initialized, run `/setup-learning`. If `/hint` or `/assess` cannot resolve a question, run `/exercise` or provide an explicit `CB-Q##` ID. If several exercises are active, choose the exercise and question shown by the agent instead of allowing a silent guess. For Git issues, use `/help git` and inspect with `git_workflow.py --mode inspect`; do not delete or reset a branch to troubleshoot.

If citations are stale, regenerate the lesson or assessment from the current source file. If checks fail, preserve the output, inspect the first relevant error, and ask `/explain` about it. If the native/inferred section map looks wrong, rerun `python3 <overflow-skill>/scripts/discover_evidence.py <path> --repository-type <type>` and ask setup to revise the evidence plan. Do not run undocumented destructive commands, expose secrets, or open canonical solutions merely to construct a hint.
