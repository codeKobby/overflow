---
name: review
description: Run spaced retrieval practice over weak, overdue, or recently corrected programming topics from overflow progress state. Mix related concepts and recommend the next review without overwhelming the learner. Use when the user asks to review, revise, practise older material, or study due topics.
license: MIT
metadata:
  package: overflow
  version: "0.2.0"
---

# Overflow Review

Read `.learning/progress.json`, recent quiz sessions, assessments, misconceptions, and review dates. Select a manageable set of due or weak topics. Present review scope, daily load, interleaving, and output choices as selectable questions when supported; otherwise use numbered or lettered text.
 Prefer effortful retrieval and changed examples over rereading.

Use a mixture of concept recall, output prediction, code tracing, debugging diagnosis, edge cases, and transfer. Interleave related topics only after the learner has basic fluency. Ask one item at a time, give concise feedback, and record evidence.

Use transparent states such as `new`, `exposed`, `emerging`, `retrieval-strong`, `reliable`, and `transferable`. Correct answers after hints are weaker evidence. Present the recommended review set as a selectable question before starting unless the learner already specified it.
 Do not promote implementation mastery from recall alone. Keep daily review volume reasonable and recommend `/teach`, `/exercise`, or `/assess` when retrieval reveals a gap.

Write a review session under `.learning/review-sessions/` when Markdown or durable history is requested. Finish with topics reviewed, misconceptions found, evidence strength, and the next review date.
