# Curriculum Design

## Classify before planning

Classify the repository as `structured-course`, `source-project`, `hybrid`, or `sparse`. Show the evidence used and let the learner correct the classification.

| Type | Main evidence | Planning behavior |
| --- | --- | --- |
| `structured-course` | Day index, ordered lessons, exercises, hints, solutions, standards. | Preserve and map the existing sequence. |
| `source-project` | README/docs, source, tests, manifests, build scripts, issues, examples, no formal day index. | Build a project map and propose a daily curriculum. |
| `hybrid` | Course material plus a project or capstone. | Keep the course sequence and connect it to project milestones. |
| `sparse` | Unclear entry point or incomplete documentation. | Ask for a goal and starting path; mark assumptions and unknowns. |

## Interview the learner

Ask progressively, not as one overwhelming form:

- What should you be able to do with this repository?
- What is your experience with programming and the main technologies?
- Which concepts do you already know?
- How much time can you study per day?
- Do you prefer reading, building, debugging, or a mix?
- Should generated lessons be inline, Markdown, or both? Recommend Markdown by default.
- Which commands, files, services, or dependencies must not be touched?

Allow `unknown` and record assumptions in `.learning/CONFIG.md`.

## Create the plan, not every lesson

For a source project, draft `.learning/PROJECT_MAP.draft.md`, `.learning/PROJECT_GLOSSARY.draft.md`, and `.learning/CURRICULUM.draft.md`. Show concise summaries and ask for selectable confirmation before writing the durable files. Each roadmap day should contain an outcome, concepts, source anchors, prerequisites, an activity, evidence, verification, and a review target.
 Keep it compact and use 7-, 14-, 21-, or 30-day plans according to learner time and project size.

Do not generate full lessons, large code walkthroughs, complete solutions, or future quiz banks during setup. Lesson generation is on demand. Maintain a glossary of project terms and link lessons, attempts, assessments, quiz reports, and learning records by artifact path.

## Generate a lesson on demand

When the learner selects a day, topic, file, symbol, test, bug, feature, or milestone:

1. Load the selected roadmap entry or project target.
2. Read only relevant source, tests, and documentation.
3. State the outcome and source anchors.
4. Produce Markdown by default, or honor `--inline`/`--both`.
5. Include short, real source excerpts with repository-relative paths and line ranges.
6. Ask for prediction before explaining where useful.
7. Give an exercise, transfer task, and evidence requirement.
8. Save Markdown under `.learning/lessons/`.
9. Treat generation as exposure; update mastery only after learner evidence.

## Cite the real code

Use:

```md
### Source anchor

`src/parser.py:42-58` — `parse_config()`

```python
# short excerpt copied from the repository
```
```

Never guess line ranges. Cite tests separately when they prove behavior. If the file changes, mark the anchor stale. Redact secrets, tokens, keys, and sensitive personal data instead of copying them.
