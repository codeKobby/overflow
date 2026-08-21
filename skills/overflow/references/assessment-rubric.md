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
| Proof response | Can the learner answer the repository’s native or inferred direct question in their own words and connect it to source evidence? |
| Completion gate | Has the learner demonstrated the native or inferred finish-line condition, including reproducibility, repair, limitation, or transfer where required? |

## Adaptive sequence

When an evidence plan exists, assess in this order unless the repository explicitly says otherwise:

1. implementation and acceptance criteria;
2. documented or approved verification;
3. one native `Prove it` question or clearly labelled inferred proof question at a time;
4. unresolved finish-line and self-assessment gates;
5. transfer or review recommendation.

Direct-answer questions are not graded by exact wording. Look for conceptual accuracy, source grounding, connection to the implementation or observed output, a meaningful boundary, and honest limitations. Record each response separately from code execution. A correct implementation with unanswered proof questions is verified for implementation but not yet transferable or mastered.

Every evidence item must include `source_kind: native` or `source_kind: inferred`, its source path and line range when available, the prompt, learner response or check output, verdict, and remaining gap.

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
