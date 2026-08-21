# State Schema

Store durable learner state in `.learning/` and do not modify course-owned curriculum files.

```text
.learning/
├── CONFIG.md
├── MISSION.md
├── PROJECT_MAP.md
├── PROJECT_GLOSSARY.md
├── CURRICULUM.md
├── PROGRESS.md
├── progress.json
├── quiz-sessions/
├── attempts/
├── assessments/
├── learning-records/
├── lessons/
└── cache/
```

During setup, write `PROJECT_MAP.draft.md`, `PROJECT_GLOSSARY.draft.md`, and `CURRICULUM.draft.md` first. Show concise summaries, ask for learner confirmation, and only then write the durable versions. If existing files differ, show a proposed diff and ask before reconciling.

## Planning files

`CONFIG.md` stores repository classification, learner experience, goals, time budget, activity preference, output mode, execution permissions, and safety boundaries. `MISSION.md` stores the learner’s current outcome and assumptions. `PROJECT_MAP.md` records entry points, technologies, directories, important symbols, tests, commands, milestones, risks, unknowns, and source anchors. `PROJECT_GLOSSARY.md` records project terms, aliases, symbols, plain-language definitions, and source anchors. `CURRICULUM.md` stores daily roadmap metadata, not full lessons.

Each roadmap day should record an observable outcome, concepts, prerequisites, source anchors, activity, evidence, verification, and later review target. Setup must not pre-generate every lesson or quiz bank.

## `progress.json`

Use a small, inspectable JSON document:

```json
{
  "version": 3,
  "repository_type": "source-project",
  "course": "project-slug",
  "current_target": "src/parser.py",
  "topics": {
    "parsing": {
      "status": "emerging",
      "confidence": 0.55,
      "last_seen": "2026-08-21",
      "next_review": "2026-08-23",
      "evidence": [
        ".learning/lessons/source-parser.md",
        ".learning/attempts/parser-001.md",
        ".learning/assessments/parser-001.md"
      ],
      "misconceptions": []
    }
  }
}
```

Keep `status` qualitative. A multiple-choice score can strengthen retrieval evidence but cannot alone promote a coding topic to `reliable`.

## Lesson artifacts

When a learner selects a target and requests Markdown, save `.learning/lessons/day-03-topic.md` or `.learning/lessons/source-parser.md`. Include generation date, target, outcome, source anchors, short real excerpts, explanations, exercise, evidence requirement, and stale-anchor notes when applicable. Link the lesson to later attempts, assessments, quiz reports, and learning records by relative path.

Cite repository-relative paths and exact line ranges. Never guess line numbers. Redact secrets, tokens, private keys, and sensitive personal data.

## Learning records

Store focused records under `.learning/learning-records/`. Each record should identify the concept, date, target, evidence type, source artifacts, durable understanding, misconception corrected, confidence, next review, and optional learner note. Do not create a record from ordinary conversation unless the learner explicitly reflects or confirms it.

## Quiz session

Save a session before question 1 and after every valid answer. Keep the answer key out of learner-visible transcripts until completion.

```json
{
  "session_id": "timestamp-target-random",
  "status": "active",
  "target": {"repository_type": "source-project", "target": "src/parser.py", "title": "Parser"},
  "settings": {"count": 10, "difficulty": "adaptive", "mode": "md"},
  "current_index": 1,
  "questions": [],
  "score": {"correct": 0, "answered": 0, "percentage": 0},
  "topics": {},
  "artifacts": []
}
```

## Artifact links

Reference artifacts by path instead of duplicating large code blocks. Record whether evidence is exposure, retrieval, implementation, or transfer; record hints used, checks actually run, source-anchor freshness, uncertainty, and links to the preceding and following artifacts.
