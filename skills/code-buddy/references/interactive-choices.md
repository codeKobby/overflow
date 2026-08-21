# Interactive Choice Contract

Present every meaningful learner choice as a question. When the current coding agent supports selectable options, render the choices as interactive buttons or a structured question. When it does not, render the same choices as numbered or lettered text and accept the number, letter, exact label, or a natural-language equivalent.

## Choice rules

1. Ask one decision at a time unless the options are independent and a compact multi-select is clearly easier.
2. Give each option a short, distinct label and a plain-language description.
3. Mark the recommended default, but never select it silently when the choice changes the learner’s plan or output.
4. Offer `Other`, `Not sure`, and `Skip for now` when appropriate.
5. Explain what the answer changes before asking, especially for study duration, command execution, output format, or safety boundaries.
6. Preserve the learner’s answer in `.learning/CONFIG.md` or the relevant session state.
7. If the learner replies with prose instead of selecting an option, interpret it and confirm only when ambiguous.
8. Do not repeat a question whose answer is already stored unless the learner asks to change it.

## Portable rendering

Use a semantic question shape internally:

```yaml
id: output_mode
question: How should generated lessons be delivered?
options:
  - id: markdown
    label: Markdown file (recommended)
    description: Save a durable lesson under .learning/lessons/.
  - id: inline
    label: In chat
    description: Keep the lesson in the current conversation.
  - id: both
    label: Both
    description: Show a short summary in chat and save the full Markdown lesson.
  - id: other
    label: Other
    description: Tell me your preferred format.
default: markdown
allow_multiple: false
```

Interactive-capable agents may render the `options` as buttons. Text-only agents should render:

```text
How should generated lessons be delivered?
1. Markdown file (recommended) — save a durable lesson.
2. In chat — keep the lesson inline.
3. Both — summarize in chat and save the full lesson.
4. Other — tell me your preferred format.
Reply with 1–4 or the option name.
```

## Where to use selectable questions

Use this contract for repository classification, learner experience, goal, study schedule, activity preference, output mode, command permissions, curriculum length, first target, quiz count, difficulty, quiz controls, hint level, assessment mode, review scope, and next action. Multiple-choice quiz questions are also selectable questions, but their answer key remains hidden until grading.
