# Assessment Rubric

Assess evidence, not confidence alone. Use one of four verdicts: `not-demonstrated`, `emerging`, `reliable`, or `transferable`.

| Criterion | Questions |
| --- | --- |
| Concept | Can the learner explain the relevant behavior accurately? |
| Implementation | Does the artifact meet the acceptance condition on the taught input? |
| Reasoning | Can the learner explain why the code or answer works? |
| Verification | Which documented checks actually ran, and what do they prove? |
| Edge cases | Can the learner name and test a meaningful boundary or failure path? |
| Maintainability | Is the code readable, appropriately structured, and consistent with the course? |
| Transfer | Can the learner apply the idea to a changed input or novel task? |
| Safety | For security work, are authorization, scope, evidence, cleanup, and limits explicit? |

## Report format

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

Never fabricate test output. A green check proves only the condition it checks. A failing check is evidence of a mismatch, not a complete diagnosis. Separate observations from inferences.
