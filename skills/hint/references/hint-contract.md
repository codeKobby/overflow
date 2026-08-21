# Hint Contract

## Resolve the active question

Read `.learning/exercises/*/manifest.json` and resolve an omitted question from `active_question`. If more than one exercise is active, show the exercise titles and ask. If a question ID is provided, use it only after confirming it exists in the manifest.

Inspect the answer region and recent attempt record before choosing a hint level. A learner who has not run the code should usually receive a prediction or observation prompt before a code hint.

## Escalate gradually

Start at the lowest useful level. `/hint` with no level should use the recorded `hint_level`, incrementing only after the learner asks again or confirms that the prior hint did not unblock them.

- Level 0: ask what was expected and what was observed.
- Level 1: cite the exact lesson, exercise, concept, or repository file.
- Level 2: identify the next decision or invariant.
- Level 3: give partial pseudocode or a meaningful blank.
- Level 4: provide a comparable example with changed names, data, and context.
- Level 5: review the complete solution only after an attempt or explicit request.

Record each hint in the attempt record, including the level, text, and whether the learner asked for a stronger hint. Do not paste a complete solution into the learner answer region.

## Put hints in comments when requested

A hint may be inserted immediately above the relevant answer region only after showing the proposed text and getting confirmation if writing into a learner-owned file. Use a language-appropriate comment syntax. Mark it so it cannot be mistaken for executable code:

```js
// CB-HINT-START CB-Q04 level=3
// pseudocode: normalize the input -> compare the normalized values -> return the boolean
// CB-HINT-END CB-Q04
```

For a Markdown answer file, use HTML comments. If the language’s comment form is unknown, keep the hint in `.learning/exercises/<exercise-id>/hints.md` instead.

## Do not spoil

Never quote or copy the canonical solution merely because the repository contains `solutions.md`. A full-solution review is a separate learner-requested action. For comparable examples, change identifiers, inputs, and surrounding context so the learner must transfer the idea.

## Preserve safety

Do not run code as part of a hint. Do not modify source files beyond the explicitly requested hint insertion. For cybersecurity exercises, hints must preserve authorization, local/synthetic scope, evidence, cleanup, privacy, and stop conditions.
