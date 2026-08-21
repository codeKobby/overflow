---
name: next
description: Recommend the next learning action in a repository-based programming course by inspecting overflow mission, progress, quizzes, exercises, assessments, misconceptions, and review dates. Use when the user asks what to do next or wants a personalized learning path.
license: MIT
metadata:
  package: overflow
  version: "0.2.0"
---

# Overflow Next

Inspect `.learning/` and the course index before recommending an action. Choose one concrete next step, not a long list. Present the candidate actions as a selectable question when supported; otherwise use numbered or lettered text and accept a natural-language answer.

Use this priority:

1. Safety, setup, or environment blocker.
2. Overdue review of a high-value misconception.
3. Incomplete core exercise.
4. Submitted artifact awaiting assessment.
5. Transfer task for a recently learned topic.
6. Next lesson or project milestone.

Explain why the action is next, which evidence supports it, what the learner should produce, and which command to run. Mark one recommended option and include `Other` or `Not sure`. Prefer `/review`, `/teach`, `/exercise`, `/assess`, or `/quiz` with a precise target.
 Do not automatically advance to a new day when required evidence is missing.

If `.learning/` is missing, recommend `/setup-learning`. If the learner has conflicting state, show it and ask before changing history.
