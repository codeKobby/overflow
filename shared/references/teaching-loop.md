# Teaching Loop

Use a short learning episode rather than a large lecture.

## Default sequence

1. State the learner’s target and why it matters.
2. Ask one retrieval or prediction question before explaining.
3. Teach the smallest mental model needed for the task.
4. Show one runnable worked example.
5. Ask the learner to trace output, state, control flow, or data shape.
6. Give a meaningful incomplete example with a concept-level blank.
7. Ask the learner to implement independently.
8. Run documented checks only when allowed and report actual evidence.
9. Ask for one edge case, limitation, or trade-off.
10. Record evidence and schedule later retrieval.

## Help ladder

Use the lowest level that unblocks progress:

| Level | Response |
| --- | --- |
| 0 | Ask what the learner expected and observed. |
| 1 | Point to a relevant concept or lesson section. |
| 2 | Give a targeted hint about the next decision. |
| 3 | Show partial pseudocode or a meaningful blank. |
| 4 | Explain a comparable worked example. |
| 5 | Review a complete solution only after an attempt or explicit request. |

Do not make the learner copy finished code when the goal is independent practice. If a solution is requested, label it as a solution review and ask the learner to explain the important decisions afterward.

## Course-specific teaching

For JavaScript/TypeScript, show the same runtime idea in both languages and distinguish compiler feedback from runtime behavior. For React/Next.js, identify state ownership and server/client boundaries. For cybersecurity, establish authorization, target, scope, evidence, cleanup, and stop conditions before technical steps.
