# Routing, Readiness, and Skill Handoffs

Use this contract when Overflow is invoked as `/overflow`, receives a natural-language request, or needs to choose a learning sub-skill.

## Router responsibility

Overflow is a route-first orchestrator. Its first job is to recognize the user’s request, announce the selected route, and continue the task. It is not a generic prompt that exposes internal instructions or stops at the first missing state file.

Run `scripts/route_request.py <repository> --request "<original request>" --json` before acting. The helper is read-only and returns the primary intent, selected route, readiness state, whether initialization is required, an announcement, and a continuation payload. Use the helper as a deterministic guardrail, not as a replacement for judgment.

A good route announcement has three parts:

> **Route:** what Overflow will run.
>
> **Reason:** why that route fits the request and current repository state.
>
> **Continuation:** what Overflow will do after setup or a specialist handoff.

For example:

> I’m going to run `/setup-learning` first because this repository has no Overflow learning state. I’ll inspect the repository, ask the setup questions, and wait for confirmation before writing `.learning/`. After setup, I’ll continue with `/teach` for your original request.

Do not say that the skill instructions require a question. Do not expose the readiness detector, routing table, or internal decision process unless the learner asks for diagnostics.

## First-run and `/overflow` behavior

When `/overflow` is invoked without a specific request, route to `/next` after checking readiness. If the repository is uninitialized, announce that Overflow will run `/setup-learning` first and then recommend the smallest next action. If `/overflow` includes a request, preserve that exact request as the continuation target.

When a stateful request arrives and `.learning/` is missing, draft, or partial, automatically start `/setup-learning` after announcing it. The initializer must still inspect, interview, draft, and ask before durable writes. Once setup is confirmed and succeeds, continue the original route in the same conversation whenever possible. Do not ask the learner to retype the original request.

Use the following continuation contract:

```text
original_request: the user’s exact request
initializer: setup-learning
resume_route: the selected Overflow route
resume_after_setup: true only after setup completes successfully
```

If the learner explicitly requests a one-off stateless explanation, skip initialization and say that no durable learning state will be written. If the request needs progress, review history, active exercise state, durable memory, or a learning record, it cannot be meaningfully completed statelessly. Explain that and route to setup.

## Readiness states

Run `scripts/detect_readiness.py <repository> --json` as part of route planning. The detector never creates, deletes, or changes files.

| State | Meaning | Route behavior |
| --- | --- | --- |
| `uninitialized` | `.learning/` does not exist. | Announce `/setup-learning`, preserve the original request, and continue after confirmed setup. |
| `draft` | Setup drafts exist but durable state has not been accepted. | Announce that setup will resume; preserve drafts and continue after confirmation. |
| `partial` | Some durable files or directories exist, but state is incomplete. | Announce setup resumption, show missing items when relevant, and never recreate or reset silently. |
| `initialized` | Required planning files and learning directories exist. | Continue to the selected Overflow route. |
| `invalid` | `.learning` is a file or otherwise unusable. | Stop before writes and ask whether to repair or choose another repository. |

For `/help`, `/setup-learning`, `/explain`, and explicit diagnostic requests, do not block on durable learning readiness. `/explain` should run inline by default and only write an artifact when requested. `/help` and `/setup-learning` should proceed directly.

## Intent routing

Prefer explicit slash commands. Otherwise classify one primary intent and, when useful, one secondary intent. Route by workflow, not just by keyword.

| Intent | Primary route | Preconditions | Typical continuation |
| --- | --- | --- | --- |
| Orient or invoke `/overflow` without a task | `/next` | Durable state, so initialize first when missing | `/teach`, `/quiz`, or `/exercise` selected by `/next` |
| Learn from this repository or study a topic | `/teach` or `/next` | Durable state for saved lessons and curriculum | `/quiz`, `/exercise`, or `/assess` |
| Retrieve knowledge | `/quiz` | Durable state for sessions and reports | `/exercise` or `/review` |
| Practise implementation | `/exercise` | Durable state for active markers and attempts | `/hint`, `/assess`, then `/review` |
| Explain code or an error | `/explain` | No durable state required by default | Optional `/teach` or `/exercise` |
| Review or assess evidence | `/review` or `/assess` | Durable state unless a clearly bounded inline review is requested | `/teach`, `/hint`, or `/next` |
| Manage learning memory or progress | `/learn`, `/progress`, or `/next` | Durable state | Continue with the recommended evidence gap |
| Implement, debug, test, review, document, design, deploy, or modify an artifact | Specialist candidate | Inspect installed skill metadata first | Return to the original learning route and offer `/assess` |
| No clear Overflow or specialist match | Direct answer | No durable state unless requested | Offer `/help` or a next action only when useful |

## Specialist discovery and invocation policy

Run `scripts/discover_skills.py <repository> --include-global --json` before proposing a specialist. Match the skill’s frontmatter `name` and `description`, not the directory name alone. Filter out deprecated, experimental, malformed, and duplicate entries when the host exposes that metadata.

Use Matt Pocock’s invocation distinction:

| Skill type | Router behavior |
| --- | --- |
| User-invoked | Announce and offer the exact command. Do not invoke it silently from another skill. |
| Model-invoked | The host may invoke it when the match is clear and proactive routing is enabled. Announce the route first. |
| Unknown invocation policy | Treat it as user-invoked and ask for confirmation. |

Overflow itself owns learning state, source citations, project glossary, curriculum, evidence plans, exercise markers, assessment records, progress, and durable learning memory. A specialist may work on the requested artifact, but it must not delete `.learning/`, rewrite learner records, commit, push, open a pull request, merge, switch branches, or run risky commands without separate confirmation.

## Handoff and phase boundaries

Use a handoff for a real boundary: a new harness, a new directory, a colleague, or a side task. A specialist handoff is not the same as a portable conversation handoff.

Before a specialist invocation, announce the skill, why it matches, expected files or commands, whether Overflow state remains untouched, and the next return point. Ask confirmation before file-changing or external actions. If the host cannot invoke a skill programmatically, render its exact command or name as text.

After a specialist returns, verify what actually happened, summarize observed changes and checks, re-run readiness if `.learning/` may have changed, and continue the original request when safe. Do not claim that a handoff occurred, a command ran, or a file changed without host evidence.

At a phase boundary, prefer continuing in the same conversation when the next phase needs the current reasoning as a primary source. Use a portable handoff only when work moves to another harness, directory, colleague, or side task. Use a fresh compacted session when the context is relevant but too large. Preserve the original request and the next route in any continuation artifact.

## Examples

```text
User: /overflow teach me how this parser works
Overflow: I’m going to run `/setup-learning` first because this repository has no Overflow learning state. I’ll inspect the repository, ask the setup questions, and wait for confirmation before writing `.learning/`. After setup, I’ll continue with `/teach` for your original request.
```

```text
User: /overflow explain this error in src/parser.py
Overflow: I’ll route this to `/explain` and answer inline without creating learning state. If you want the explanation saved or turned into a lesson, I’ll offer that next.
```

```text
User: /overflow build a React dashboard for this lesson
Overflow: This is implementation work rather than a core learning command. I’ll inspect installed skill metadata and propose the closest web-development specialist. After it returns, I’ll bring the result back to Overflow for `/assess` and progress tracking.
```

```text
User: /overflow review my answer
Overflow: I found an active Overflow exercise, so I’ll route this to `/assess`. I’ll inspect the `CB-Q##` marker, use the approved checks only after confirmation, and keep correctness separate from quality and proof evidence.
```
