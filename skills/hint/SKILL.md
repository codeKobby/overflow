---
name: hint
description: Give a progressive, non-spoiling hint for the active overflow exercise question by reading its marker, prompt, answer region, source lesson, and recent attempt. Use when the learner asks for a hint, help, clue, pseudocode, or guidance on the current exercise.
license: MIT
metadata:
  package: overflow
  version: "0.6.0"
---

# Overflow Hint

Help the learner continue their current exercise without taking ownership of the implementation. Resolve the active question from `.learning/exercises/*/manifest.json`, inspect the marked answer region and recent attempt, and give the smallest useful clue.

## Workflow

1. Locate the active exercise manifest. If none exists, ask the learner to run `/exercise` first. If multiple exercises are active, present their titles as selectable choices or numbered options.
2. Resolve the question in this order: explicit question ID, the manifest’s `active_question`, the only recently edited unanswered region, then a selectable list of unresolved questions. Never silently choose among multiple candidates.
3. Read the question prompt, source anchor, relevant lesson section, target file, answer region, checks, and previous hint level. Do not open a canonical solution just to construct a hint.
4. Start at the lowest useful rung of the help ladder: expectation/observation, concept/source pointer, next decision, partial pseudocode, comparable example, then solution review only after an attempt or explicit request.
5. When the learner asks for a stronger hint, increase the level by one and explain what changed. Do not jump straight to finished code.
6. If the learner asks to put the hint in code, show the proposed comment first. After confirmation, insert a clearly delimited `CB-HINT-START` / `CB-HINT-END` block immediately above the answer region using the file’s comment syntax. If the syntax is unknown, write `.learning/exercises/<exercise-id>/hints.md` instead.
7. Record the hint level, question ID, source anchor, and concise hint text in the attempt record. Do not change the answer region or mark the question complete.
8. Remind the learner that `/assess` can inspect the active answer after they implement it and run the permitted checks.

## Hint ladder

| Level | Provide | Do not provide |
| --- | --- | --- |
| 0 | Ask what they expected, ran, and observed. | A solution direction when no observation exists. |
| 1 | Point to the exact concept or source section. | Unrelated documentation. |
| 2 | Name the next decision, invariant, or input shape. | The exact implementation. |
| 3 | Give partial pseudocode or one meaningful blank. | Copy-paste-ready final code. |
| 4 | Give a comparable example with different names, values, and context. | The exercise’s finished answer. |
| 5 | Review a complete solution only after an attempt or explicit request. | Presenting it as independent work. |

For a code comment, use a language-appropriate form such as:

```python
# CB-HINT-START CB-Q03 level=3
# pseudocode: validate the input -> transform each item -> return the required shape
# CB-HINT-END CB-Q03
```

For Markdown, use HTML comments. Do not put executable-looking pseudocode inside an answer region without the hint delimiters.

## Safety and honesty

Do not run code for the sole purpose of giving a hint. Do not reveal `solutions.md` or copy a canonical answer merely because it is present in the repository. For cybersecurity exercises, preserve authorization, local/synthetic scope, evidence, cleanup, privacy, and stop conditions.
