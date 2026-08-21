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
├── exercises/
├── attempts/
├── assessments/
├── learning-records/
├── lessons/
└── cache/
    └── evidence-map.json

Optional Git metadata:

```text
.learning/git-workflow.json
```

During setup, write `PROJECT_MAP.draft.md`, `PROJECT_GLOSSARY.draft.md`, and `CURRICULUM.draft.md` first. Show concise summaries, ask for learner confirmation, and only then write the durable versions. If existing files differ, show a proposed diff and ask before reconciling.

## Planning files

`CONFIG.md` stores repository classification, learner experience, goals, time budget, activity preference, output mode, execution permissions, and safety boundaries. `MISSION.md` stores the learner’s current outcome and assumptions. `PROJECT_MAP.md` records entry points, technologies, directories, important symbols, tests, commands, milestones, risks, unknowns, and source anchors. `PROJECT_GLOSSARY.md` records project terms, aliases, symbols, plain-language definitions, and source anchors. `CURRICULUM.md` stores daily roadmap metadata, not full lessons.

Each roadmap day should record an observable outcome, concepts, prerequisites, source anchors, activity, a native-or-inferred evidence plan, verification, Git isolation preference when selected, and later review target. Setup must not pre-generate every lesson or quiz bank.

## Evidence map

After learner confirmation, cache `.learning/cache/evidence-map.json`. Native records point to headings or linked artifacts found in the repository; inferred records explain which source files, tests, or milestones motivated the proposed evidence step.

```json
{
  "version": 1,
  "repository_type": "structured-course",
  "source_hashes": {"day_01/lesson.md": "sha256:..."},
  "native_sections": [
    {"role": ["proof", "verification"], "title": "Prove it", "path": "day_01/lesson.md", "start_line": 100, "end_line": 110, "confidence": {"proof": 1.0}}
  ],
  "inferred_evidence": [],
  "evidence_order": ["implementation", "verification", "reasoning", "edge-case", "completion", "transfer", "safety"]
}
```

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

## Exercise manifests

Store learner-owned exercise state under `.learning/exercises/<exercise-id>/`. Keep the source prompt path and a source hash so regeneration can detect changed course material. A manifest contains stable `CB-Q##` IDs, source anchors, target files, answer regions, acceptance criteria, approved checks, `active_question`, hint level, status, attempts, an optional native-or-inferred `evidence_plan`, optional Git branch/worktree metadata, and last evidence. Per-question status may be `not-started`, `scaffolded`, `in-progress`, `hinted`, `submitted`, `verified`, `needs-revision`, or `mastered`.

```json
{
  "version": 1,
  "exercise_id": "day-01-setup",
  "source": {
    "prompt_path": "day_1/practice/exercises.md",
    "source_hash": "sha256:..."
  },
  "active_question": "CB-Q02",
  "questions": [
    {
      "id": "CB-Q02",
      "status": "in-progress",
      "answer_regions": [
        {"path": "answers.py", "start_marker": "CB-ANSWER-START CB-Q02", "end_marker": "CB-ANSWER-END CB-Q02"}
      ],
      "hint_level": 2,
      "hints_used": [2],
      "checks": ["python answers.py"],
      "last_evidence": null
    }
  ]
}
```

Keep the answer region executable whenever possible. If a learner submits a commented draft, record `evidence_mode: draft-answer` until a reversible activation or separate executable answer has run successfully. Record quality dimensions separately from correctness; a passing implementation can still have `quality: improvable` or `modernity: opportunity`. If a native or inferred proof plan exists, store direct-answer responses separately from code evidence and keep unresolved finish-line gates visible. Git commits, branch diffs, pushes, and pull requests are evidence artifacts, not proof of mastery.

## Git workflow state

When the learner selects branch isolation, store `.learning/git-workflow.json` only after the requested branch or worktree is successfully created. Record `mode`, `base_branch`, `base_commit`, `exercise_branch`, `worktree_path`, `created_at`, `commit_status`, `push_status`, and `pull_request_status`. Keep commit, push, pull-request, merge, deletion, and branch-switch actions independently confirmed.

## Lesson artifacts

When a learner selects a target and requests Markdown, save `.learning/lessons/day-03-topic.md` or `.learning/lessons/source-parser.md`. Include generation date, target, outcome, source anchors, short real excerpts, explanations, exercise, concise native-or-inferred evidence plan, proof questions or finish-line gates when due, evidence requirement, and stale-anchor notes when applicable. Link the lesson to later attempts, assessments, quiz reports, and learning records by relative path.

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

Reference artifacts by path instead of duplicating large code blocks. Record whether evidence is exposure, retrieval, implementation, or transfer; record hints used, checks actually run, source-anchor freshness, uncertainty, and links to the preceding and following artifacts. Do not treat a green check as proof of mastery without explanation and transfer evidence.
