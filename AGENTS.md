# Overflow Agent Guidance

`overflow` is a portable Agent Skills suite. Do not assume it is Claude-only or tied to the three example courses.

## Compatibility rule

Use the standard `SKILL.md` folders from this repository. Before claiming host support, consult [`compatibility/README.md`](compatibility/README.md) and [`compatibility/hosts.json`](compatibility/hosts.json). Host-specific metadata may improve a picker or installation route, but it must not replace the portable skill body.

## Learning workflow

When `/overflow` receives a request, run `shared/scripts/route_request.py` or the equivalent packaged helper, announce the selected route, and continue the task. If a stateful request arrives before setup, announce that `/setup-learning` will run first, preserve the original request, and resume the selected route after setup succeeds. `/setup-learning` must classify the workspace, interview the learner, draft the project map, glossary, and curriculum, and ask for confirmation before writing durable learner state. Do not generate every future lesson during setup. Stateless `/explain` requests may continue without initialization when no artifact is requested.

For a selected target, use `/help`, `/teach`, `/quiz`, `/exercise`, `/hint`, `/assess`, `/review`, `/progress`, `/next`, or `/learn`. Prefer Markdown artifacts for lessons and assessments. Link artifacts to one another and preserve `.learning/` as repository-local learner state. `/exercise` may create `.learning/exercises/<exercise-id>/manifest.json` with stable `CB-Q##` markers and an `active_question`; `/hint` and `/assess` should resolve that state rather than asking the learner to repeat the prompt. Setup may offer a local exercise branch, linked worktree, current branch, or decide-later choice; preserve `.learning/git-workflow.json` when isolation is selected.

## Host behavior

Use selectable questions when the host supports them; otherwise present numbered or lettered options. Never make correctness depend on a proprietary question UI. Keep question markers and `CB-ANSWER-START` / `CB-ANSWER-END` delimiters intact. `/hint` must escalate without spoiling the solution, and `/assess` must ask before activating a commented draft or running checks. For natural-language requests outside Overflow’s core learning loop, announce that installed skill metadata will be inspected and offer a confirmation-based `/handoff`. Only model-invoked specialists may be automatically invoked when the host supports it; user-invoked skills must be offered as explicit commands. Never silently invoke a specialist. Keep references relative, avoid absolute host paths in portable instructions, and do not leak Claude-only tool names into skills intended for Codex, Cline, OpenCode, Antigravity, Copilot, or other compatible agents.

## Safety and validation

Review skill code and scripts before installation. Ask before writing host configuration, installing dependencies, accessing external systems, or running commands with side effects. Run `detect_readiness.py` before claiming progress or creating state. Git status must be inspected before branch setup; show dirty paths and obtain confirmation before `git_workflow.py --apply`, staging, committing, pushing, opening a pull request, merging, deleting, cleaning, or switching. Run the compatibility validator and the skill validator before publishing a release.
