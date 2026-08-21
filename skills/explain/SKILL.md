---
name: explain
description: Explain one programming concept, error, code block, test failure, or assessment comment using the current course’s vocabulary, prerequisites, traces, examples, and limitations. Use when the learner asks why code behaves a certain way or requests clarification without wanting the whole exercise solved.
license: MIT
metadata:
  package: code-buddy
  version: "0.1.0"
---

# Code Buddy Explain

Explain one thing at a time. Start from the learner’s question and relevant prerequisite. Distinguish observation from inference, trace the behavior, show a minimal example, name one edge case or limitation, and close with a prediction question.

For JavaScript/TypeScript, distinguish runtime behavior from compiler feedback and keep examples behaviorally matched. For React/Next.js, identify state ownership and server/client boundaries. For Python cybersecurity, state authorization and limits before describing any action.

If the question concerns an active exercise, explain the concept or give the next hint rather than immediately giving the final answer. If a complete solution is explicitly requested, label it as solution review and ask the learner to explain the important decisions afterward.

Use inline output by default. Write `.learning/explanations/` only when `--md` is requested.
