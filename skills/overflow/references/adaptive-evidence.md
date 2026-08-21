# Adaptive Evidence Contract

Use this contract before generating a lesson, exercise, assessment, progress update, or next-action recommendation. Overflow must adapt to the repository’s own teaching structure instead of assuming every project has the same files or section names.

## Discover before deciding

Inspect the selected lesson or source-project slice, its headings, nearby paragraphs, Markdown links, starter files, tests, package commands, standards, and safety documents. Use `scripts/discover_evidence.py` to create a compact inventory. Preserve each section’s relative path, heading, line range, source hash, links, role, and confidence.

A native section is one actually found in the repository. An inferred section is a proposed evidence step created because a source project lacks an equivalent. Label inferred plans as `inferred`; never claim the repository itself contains a `Prove it` or `Finish line` section when it does not.

## Normalized section roles

| Role | Common native signals | Evidence it supplies | Default handling |
| --- | --- | --- | --- |
| `practice` | Practice, Independent exercises, Workshop, Try it, Tasks | Implementation or experiment | Create or link a learner-owned exercise. |
| `proof` | Prove it, Prove, Check your understanding, Answer these, Questions | Direct-answer reasoning | Ask one question at a time in chat after implementation evidence. |
| `finish` | Finish line, Completion, Done when, Ready when, Exit criteria | Completion and mastery gate | Convert statements into a checklist and ask only unresolved items. |
| `reflection` | Self-assessment, Reflection, Review note, What you learned, Limitation | Transfer, limitation, next-step reasoning | Ask for a short explanation and one limitation. |
| `verification` | Verify, Expected output, Run it, Check, Test, Assertion | Actual output, test result, prediction comparison | Offer documented checks and record actual output. |
| `hints` | Hint, Help, Clue, linked `hints.md` | Progressive support | Use only after an attempt or explicit request. |
| `solutions` | Solution, Solutions, Finished, Answer key, linked `solutions.md` | Protected reference | Do not reveal by default; use only for explicit solution review. |
| `safety` | Safety, Scope, Authorization, Lab rules, Out of scope, Boundaries | Safety and authorization evidence | Read before action; require bounded, authorized, local/synthetic work. |

A heading may have more than one role. For example, `Prove it` is both `proof` and `verification`, while a self-assessment section may provide `reflection` and `finish` evidence.

## Course episode sequence

When a native course structure exists, preserve its order:

1. Read the relevant explanation and source anchors.
2. Run or inspect the smallest worked example.
3. Create or open the `practice` exercise.
4. Offer `hints` only after the learner attempts or asks.
5. Assess implementation and run approved `verification` checks.
6. Ask native `proof` questions in chat, one at a time, after the implementation assessment.
7. Ask unresolved `finish` and `reflection` questions.
8. Record evidence by type and recommend review, transfer, or the next lesson.

Do not force every section into every episode. Use the learner’s current evidence gaps. A small mechanical exercise may need only implementation and one proof question; a capstone may need all roles.

## Direct-answer proof questions

Treat questions under a native `proof` section as retrieval and reasoning prompts, not as code tasks. Preserve the original wording and source anchor. Ask one at a time and accept a natural-language answer, not exact string matching. Evaluate:

- conceptual accuracy;
- connection to the learner’s implementation and observed output;
- use of repository vocabulary and source anchors;
- ability to explain a normal case and a meaningful boundary;
- uncertainty or limitation stated honestly.

After each answer, explain briefly what was demonstrated and what remains unclear. Store the prompt, answer, verdict, evidence links, and misconception if any in the assessment or attempt record.

## Finish-line gates

Convert a native finish-line paragraph into explicit checklist items. For example, a statement that the learner can run a starter, explain the runtime, repair a failure, and teach the idea becomes four separate gates. Do not mark the topic `mastered` because code compiles once. Require the evidence the repository itself names: reproducibility, explanation, repair, boundary awareness, limitation, safety, or transfer.

## Source-project adaptation

When no native `practice`, `proof`, `verification`, or `finish` section exists, infer the smallest useful plan from source code, tests, documentation, and the learner’s goal:

| Inferred role | Prompt seed |
| --- | --- |
| Practice | Change one small behavior in the selected source slice and show the diff. |
| Proof | Explain what the selected symbol or flow does and cite the lines that prove it. |
| Verification | Run the documented test/check and state exactly what it proves. |
| Finish | Explain the normal case, one boundary or failure case, one limitation, and the next evidence needed. |

Mark these prompts as `source_kind: inferred`, cite the files and tests that motivated them, and ask the learner to confirm or correct the plan before durable curriculum writing. Generate detailed lessons only after the learner selects the target.

## Dynamic lesson format

A Markdown lesson or inline episode should include a compact `Evidence plan` section:

```md
## Evidence plan

- Practice: `.learning/exercises/day-01/manifest.json` — implementation attempt.
- Proof: `lesson.md:665-674` — direct-answer questions, asked after assessment.
- Verification: `package.json` command `npm run check` — actual output recorded.
- Finish line: `lesson.md:653-663` — unresolved completion gates.
- Reflection: inferred or native source anchor — limitation and transfer response.
```

For a source project, label inferred rows and explain which source files, tests, or milestones motivated them. Never invent exact line ranges; mark an anchor stale when the source changes.

## State and progress

Store a section inventory in `.learning/cache/evidence-map.json` or link it from the course map. Add an optional `evidence_plan` to lesson and exercise manifests. Record `native` versus `inferred`, source hash, prompt IDs, answers, checks, verdicts, and unresolved gates. Keep implementation, retrieval, reasoning, verification, transfer, and safety evidence separate in `progress.json` and `PROGRESS.md`.

A green test proves only the condition it checks. A correct implementation plus unanswered proof questions is `verified` for implementation but not `mastered` overall. A learner may be strong in retrieval but still need implementation practice, or pass implementation while needing explanation and transfer review.

## Safety

Read native safety and scope sections before generating or running security exercises. Preserve authorization, local/synthetic targets, bounded scope, evidence, cleanup, privacy, and stop conditions. Never use a solution section as a default source of hints or execute commands merely because they appear in a lesson.
