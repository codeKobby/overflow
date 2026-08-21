# Overflow Agent Guidance

`overflow` is a portable Agent Skills suite. Do not assume it is Claude-only or tied to the three example courses.

## Compatibility rule

Use the standard `SKILL.md` folders from this repository. Before claiming host support, consult [`compatibility/README.md`](compatibility/README.md) and [`compatibility/hosts.json`](compatibility/hosts.json). Host-specific metadata may improve a picker or installation route, but it must not replace the portable skill body.

## Learning workflow

For a new repository, start with `/setup-learning`. It must classify the workspace, interview the learner, draft the project map, glossary, and curriculum, and ask for confirmation before writing durable learner state. Do not generate every future lesson during setup.

For a selected target, use `/help`, `/teach`, `/quiz`, `/exercise`, `/hint`, `/assess`, `/review`, `/progress`, `/next`, or `/learn`. Prefer Markdown artifacts for lessons and assessments. Link artifacts to one another and preserve `.learning/` as repository-local learner state. `/exercise` may create `.learning/exercises/<exercise-id>/manifest.json` with stable `CB-Q##` markers and an `active_question`; `/hint` and `/assess` should resolve that state rather than asking the learner to repeat the prompt.

## Host behavior

Use selectable questions when the host supports them; otherwise present numbered or lettered options. Never make correctness depend on a proprietary question UI. Keep question markers and `CB-ANSWER-START` / `CB-ANSWER-END` delimiters intact. `/hint` must escalate without spoiling the solution, and `/assess` must ask before activating a commented draft or running checks. Keep references relative, avoid absolute host paths in portable instructions, and do not leak Claude-only tool names into skills intended for Codex, Cline, OpenCode, Antigravity, Copilot, or other compatible agents.

## Safety and validation

Review skill code and scripts before installation. Ask before writing host configuration, installing dependencies, accessing external systems, or running commands with side effects. Run the compatibility validator and the skill validator before publishing a release.
