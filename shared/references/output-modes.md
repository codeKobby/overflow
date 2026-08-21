# Output Modes

Support `--inline`, `--md`, and `--both` where useful.

| Mode | Default use | Behavior |
| --- | --- | --- |
| `inline` | Quiz turns, explanations, short feedback | Respond in chat and still update `.learning/` state. |
| `md` | Lesson notes, exercises, assessments, progress | Write a durable Markdown artifact and report its path. |
| `both` | Substantial assessment or learner request | Give a concise inline summary and write the full artifact. |

Default to inline for `/explain`, active `/quiz`, and short feedback. Default to Markdown for `/teach`, `/exercise`, `/progress`, and multi-criterion `/assess`. Respect the learner preference in `.learning/CONFIG.md` when present.

Never put the private answer key into a learner-visible active quiz transcript. Include the answer key only in the completed report or private session state.
