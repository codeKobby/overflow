# Routing, Readiness, and Skill Handoffs

Use this contract when Overflow receives a natural-language request instead of an explicit slash command, or when a command depends on durable learning state.

## Readiness states

Run `scripts/detect_readiness.py <repository> --json` before claiming progress, resolving an omitted learning target, or writing a lesson, quiz session, exercise, hint, assessment, review, or learning record.

| State | Meaning | Router action |
| --- | --- | --- |
| `uninitialized` | `.learning/` does not exist. | Ask whether to initialize Overflow now, run `/setup-learning` only after confirmation, or continue with a one-off explanation without durable state. |
| `draft` | Setup drafts exist but durable state has not been accepted. | Offer to resume setup, revise drafts, or discard drafts only after an explicit confirmation. Do not overwrite them. |
| `partial` | Some durable files or directories exist, but the state is incomplete. | Show the missing items and offer to resume or repair setup. Do not silently recreate or reset state. |
| `initialized` | Required planning files and learning directories exist. | Continue to the requested learning command. |
| `invalid` | `.learning` is a file or otherwise unusable. | Explain the problem and ask whether to repair or choose another repository. Never delete it automatically. |

When state is missing and the learner asks for an explicit Overflow command, pause at the readiness gate. Ask one selectable question:

```text
Overflow is not initialized in this repository. What would you like to do?
A. Initialize Overflow here (recommended; I will inspect the repo and ask before writing .learning/)
B. Run this one-off without saving learning state
C. Show me what initialization would inspect
D. Cancel
```

For `/help`, `/setup-learning`, and a request explicitly asking to initialize, do not block on the gate. For `/progress`, `/next`, `/review`, `/learn`, `/hint`, and `/assess`, initialization is required unless the learner selects the one-off alternative and the command has a meaningful stateless fallback. Never fabricate progress or durable memory.

## Intent triage

Prefer an explicit slash command over inference. Otherwise classify the request into one primary intent and, when useful, one secondary intent:

| Intent | Overflow action | Typical handoff candidates |
| --- | --- | --- |
| learn from this repository, understand a concept, study a day | Use `/setup-learning`, `/teach`, `/quiz`, or `/next`. | A repository-specific teaching or documentation skill, if installed. |
| implement or practise a change | Use `/exercise`, then `/hint` and `/assess`. | A coding, refactoring, or test-writing skill for implementation assistance. |
| inspect or explain existing code | Use `/explain` or `/teach` with a source anchor. | A code-review, debugging, architecture, or language skill. |
| run checks, review a diff, or assess quality | Use `/assess` or `/review`. | A testing, code-review, security, or performance skill. |
| create or modify files, documentation, UI, media, or infrastructure | Preserve the learning context, then offer a specialist skill. | The installed skill whose description most directly matches the artifact or operation. |
| manage Overflow memory or state | Use `/learn`, `/progress`, `/next`, or `/help`. | Do not hand off state mutations unless the learner explicitly asks. |

Use `scripts/discover_skills.py <repository> --include-global --json` to inventory installed skill metadata. Match by the skill’s `name` and `description`, not by directory name alone. If no direct match exists, keep the work inside Overflow and explain the nearest supported command.

## Handoff protocol

A handoff is an offer, not a silent invocation. Before triggering another skill, show the learner the proposed skill, the reason it matches, the files or operation it may affect, whether Overflow state will remain untouched, and the exact next action. Ask for confirmation as a selectable question. If the host cannot invoke another skill programmatically, render the equivalent explicit command or skill name as text.

Use the smallest useful handoff. Do not invoke multiple specialists for one request unless the learner approves a sequence. Keep Overflow responsible for learning state, citations, exercise markers, evidence plans, and assessment records. The specialist may help perform the requested code or artifact work, but it must not delete `.learning/`, rewrite learner records, commit, push, open a pull request, merge, switch branches, or run risky commands without separate confirmation.

After a handoff returns, summarize what was actually observed, re-run readiness detection if state may have changed, and ask whether to continue with `/assess`, `/teach`, `/review`, or another explicit command. Never claim that a handoff occurred, a test ran, or a file changed unless the host or tool reported it.

## Examples

```text
User: teach me this repository
Overflow: .learning is missing. Initialize here, run a one-off explanation, inspect initialization, or cancel?
User: Initialize here
Overflow: I found a source project with Python and pytest. I will draft the map, glossary, and curriculum, then ask before writing state.
```

```text
User: review this pull request
Overflow: I can assess it as learning evidence. I also found an installed code-review skill whose description matches review work. Should I use it for review feedback and keep Overflow for citations and progress?
```

```text
User: build a React dashboard for this lesson
Overflow: This is an implementation request. I found an installed web-development skill. Should I hand off the dashboard implementation, then return here for `/assess` and progress tracking?
```
