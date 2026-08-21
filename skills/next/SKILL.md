---
name: next
description: Recommend the next learning action in a repository-based programming course by inspecting code-buddy mission, progress, quizzes, exercises, assessments, misconceptions, and review dates. Use when the user asks what to do next or wants a personalized learning path.
license: MIT
metadata:
  package: code-buddy
  version: "0.1.0"
---

# Code Buddy Next

Inspect `.learning/` and the course index before recommending an action. Choose one concrete next step, not a long list.

Use this priority:

1. Safety, setup, or environment blocker.
2. Overdue review of a high-value misconception.
3. Incomplete core exercise.
4. Submitted artifact awaiting assessment.
5. Transfer task for a recently learned topic.
6. Next lesson or project milestone.

Explain why the action is next, which evidence supports it, what the learner should produce, and which command to run. Prefer `/review`, `/teach`, `/exercise`, `/assess`, or `/quiz` with a precise target. Do not automatically advance to a new day when required evidence is missing.

If `.learning/` is missing, recommend `/setup-learning`. If the learner has conflicting state, show it and ask before changing history.
