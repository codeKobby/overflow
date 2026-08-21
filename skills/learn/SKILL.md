---
name: learn
description: Manage code-buddy’s durable learning memory across sessions by reviewing, searching, correcting, pruning, and exporting learning records, glossary terms, misconceptions, and learner preferences. Use when the learner asks what they have learned, wants to revisit past lessons, correct stale memory, or inspect progress evidence.
license: MIT
metadata:
  package: code-buddy
  version: "0.3.0"
---

# Code Buddy Learn

Manage learner-owned memory in the current repository. Do not turn every conversation into a permanent record. Record durable memory only after a lesson, attempt, assessment, correction, or explicit learner reflection.

## Resolve the request

Present the operation as a selectable question when supported; otherwise use numbered or lettered text:

1. Review recent learning records.
2. Search records by topic, symbol, file, misconception, or date.
3. Show the project glossary and suggest stale or conflicting terms.
4. Correct or append a learning record.
5. Prune or archive stale records.
6. Export a compact learning summary.

Accept `/learn`, `/learn review`, `/learn search parser`, `/learn glossary`, `/learn correct`, `/learn prune`, and `/learn export`.

## Read before writing

Inspect `.learning/CONFIG.md`, `.learning/MISSION.md`, `.learning/PROJECT_MAP.md`, `.learning/PROJECT_GLOSSARY.md`, `.learning/learning-records/`, recent lessons, attempts, assessments, quiz reports, and `progress.json`. Show what will change and ask for confirmation before editing or deleting durable memory. Use selectable confirmation when supported; require an explicit text confirmation for deletion or archival when interactive selection is unavailable.

## Learning record format

Write focused Markdown records under `.learning/learning-records/`:

```md
# LR-0001 — <concept or decision>

- Date: YYYY-MM-DD
- Source artifacts: `.learning/lessons/...`, `.learning/attempts/...`, `.learning/assessments/...`
- Target: `src/parser.py:42-58` or `day 03`
- Evidence type: exposure | retrieval | implementation | transfer
- What changed: <the learner’s durable understanding>
- Misconception corrected: <optional>
- Confidence: emerging | reliable | transferable
- Next review: YYYY-MM-DD
- Learner note: <optional learner-authored reflection>
```

Link records to the lesson, attempt, assessment, quiz session, and progress topic instead of copying large code blocks. If a source anchor is stale, mark it stale and locate a current anchor before teaching from it again.

## Glossary management

Maintain `.learning/PROJECT_GLOSSARY.md` with project terms, abbreviations, symbols, plain-language definitions, aliases, and source anchors. Show the existing term before changing it. Ask whether to `keep`, `revise`, `add alias`, or `archive` a conflicting definition.

## Prune and export

Pruning should archive rather than silently delete by default. Before pruning, show the candidate records and ask which ones to archive. Export should create `.learning/LEARNING_SUMMARY.md` containing the mission, durable concepts, corrected misconceptions, strongest evidence, open gaps, glossary highlights, and next review targets. Never include secrets or sensitive personal data.
