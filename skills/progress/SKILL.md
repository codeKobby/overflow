---
name: progress
description: Recompute and explain code-buddy learning progress from .learning state, quiz sessions, attempts, assessments, misconceptions, and review dates. Use when the user asks how they are doing, what they have mastered, or what needs review.
license: MIT
metadata:
  package: code-buddy
  version: "0.2.0"
---

# Code Buddy Progress

Read `.learning/progress.json` and related records, then regenerate `.learning/PROGRESS.md` without overwriting learner-authored mission or evidence notes. Present filters such as topic, date range, evidence type, and output mode as selectable questions when supported; otherwise use numbered or lettered text.

Report the current repository or course and target, demonstrated topics, weak or overdue topics, recent assessments, quiz retrieval signals, implementation evidence, transfer evidence, and the smallest next action. Present possible next actions as a selectable question with one recommended option.

Keep these dimensions separate: exposure, retrieval, implementation, and transfer. Use qualitative states `new`, `exposed`, `emerging`, `retrieval-strong`, `reliable`, and `transferable`. Explain that confidence is a planning signal, not proof. A perfect multiple-choice quiz does not prove coding mastery.

If state is missing, recommend `/setup-learning`. If records conflict, show the conflict and ask before changing history. Use Markdown by default and provide a concise inline summary when possible.
