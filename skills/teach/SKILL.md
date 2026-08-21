---
name: teach
description: Teach one focused programming concept from the current repository’s lessons, documentation, source files, tests, symbols, or bugs, using a plain-language mental model, runnable example, prediction, code trace, limitation, and learner-owned practice. Use when the user asks to learn from a codebase, understand a lesson, or be taught step by step.
license: MIT
metadata:
  package: code-buddy
  version: "0.1.0"
---

# Code Buddy Teach

Teach one small concept tied to the repository’s curriculum and the learner’s mission. Prefer a short episode over a long lecture.

## Sequence

1. Resolve the requested day, lesson, topic, file, symbol, test, bug, or current target.
2. Read prerequisites, outcomes, runnable examples, traces, common mistakes, practice, references, nearby code, tests, and project conventions.
3. Ask one retrieval or prediction question before explaining when appropriate.
4. Explain the problem first, then give a plain-language mental model.
5. Show a small runnable worked example and expected behavior.
6. Ask the learner to trace output, state changes, control flow, or data shape.
7. Give a meaningful faded example with a concept-level blank.
8. Assign a small independent task with an acceptance condition.
9. Ask for an edge case or limitation and record evidence after the learner responds.

## Help ladder

Use the lowest level that unblocks learning: question, reminder, targeted hint, partial scaffold, comparable worked example, then solution review. Do not silently write the learner’s exercise solution. If a complete solution is requested, label it as a solution review and ask the learner to explain the key decisions.

For JavaScript/TypeScript, preserve the same runtime idea across both languages and distinguish compiler feedback from runtime behavior. For React/Next.js, distinguish JavaScript, React, and Next.js behavior. For cybersecurity, establish authorization, scope, evidence, cleanup, and stop conditions before technical steps. For any other codebase, use its own documentation, tests, conventions, and learner-stated goal as the teaching source.

Write a Markdown lesson note under `.learning/lessons/` when the user requests `--md`; otherwise keep the lesson inline.
