# Project Glossary

Maintain `.learning/PROJECT_GLOSSARY.md` as a small shared language for the repository and learner. Do not copy every identifier. Record only terms that are repeated, ambiguous, domain-specific, or important for understanding the selected learning path.

Use this shape:

```md
# Project Glossary

## Term: materialization cascade

- Plain meaning: turning a lesson definition into files that can run.
- Project meaning: the sequence that creates a section, lesson file, route, and index entry together.
- Aliases: materialize, publish lesson
- Source anchors: `src/materialize.ts:18-74`, `tests/materialize.test.ts:9-41`
- Learner note: first encountered on Day 03.
- Status: current
```

## Workflow

1. Extract candidate terms from README headings, domain nouns, repeated comments, public symbols, test names, configuration keys, and the learner’s own questions.
2. Show candidates as a selectable question: accept all, select terms, or skip glossary creation.
3. Draft definitions from the repository and cite source anchors.
4. Ask the learner to confirm the glossary draft before durable writing during setup.
5. Consult the glossary in `/teach`, `/quiz`, `/explain`, `/exercise`, and `/assess`.
6. When a conflict appears, show the current definition and proposed definition, then ask `keep`, `revise`, `add alias`, or `archive`.
7. Mark terms stale when the cited source changes; do not silently rewrite history.

Never include secrets, tokens, private keys, credentials, or sensitive personal data in the glossary.
