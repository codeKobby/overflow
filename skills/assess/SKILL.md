---
name: assess
description: Assess a learner’s code, diff, answer, test output, pull request, bug fix, or exercise artifact against the current repository’s standards and stated goal. Provide a qualitative verdict, evidence, gaps, explanation, edge cases, and next action; write a Markdown report when useful. Use when the user asks to grade, review, examine, assess, or check learning work in any codebase.
license: MIT
metadata:
  package: code-buddy
  version: "0.2.0"
---

# Code Buddy Assessment

Assess evidence, not confidence alone. Accept a file path, diff, pasted code, written answer, test output, or the most recent attempt. Present assessment target, output mode, and optional rubric emphasis as selectable questions when supported; otherwise use numbered or lettered text.

## Workflow

1. Identify the lesson, exercise, topic, file, symbol, bug, project goal, and acceptance condition.
2. Read the repository’s quality standard, README, tests, documentation, conventions, and relevant exercise/rubric files when present.
3. Inspect only the submitted artifact and necessary supporting files.
4. Run documented local checks only when allowed and report exactly what ran.
5. Separate observations from inferences.
6. Use the verdict `not-demonstrated`, `emerging`, `reliable`, or `transferable`; when the learner wants to discuss the result, present these interpretations as selectable options before asking for the next decision.
7. Write `.learning/assessments/YYYY-MM-DD-topic.md` for substantial assessments, linking the source lesson, attempt, quiz report, project-map target, files inspected, and checks actually run; otherwise respond inline for brief feedback.
8. Update progress evidence, link the assessment path into the affected topic, and present the recommended next action as a selectable question with `Other` when possible.

## Rubric

Assess concept accuracy, implementation acceptance, reasoning, verification, edge cases, maintainability, integration impact, transfer, and limitations. For Python cybersecurity also assess authorization, target, scope, evidence, cleanup, privacy, and stop conditions. For any other repository, derive criteria from the learner’s stated goal and the project’s own tests and conventions rather than inventing a course-specific rubric.

Use this report shape:

```md
# Assessment: <topic>

- Verdict: <level>
- Evidence inspected: <paths, diff, answer, output>

## What is demonstrated
<specific observations>

## Gaps and risks
<smallest useful corrections>

## Explanation
<focused trace or decision walkthrough>

## Verification
<checks run and what they prove; checks not run are stated>

## Edge case or limitation
<one boundary to test or explain>

## Next action
<one exercise, review, or transfer task>
```

Never fabricate test output. A green check proves only its tested condition. Do not mark implementation mastery from a multiple-choice score alone. If the learner has not attempted the work, give a task or hint instead of pretending to grade it.
