# State Schema

Store durable learner state in `.learning/` and do not modify course-owned curriculum files unless explicitly requested.

```text
.learning/
├── CONFIG.md
├── MISSION.md
├── PROGRESS.md
├── progress.json
├── quiz-sessions/
├── attempts/
├── assessments/
├── learning-records/
└── cache/
```

## `progress.json`

Use a small, inspectable JSON document:

```json
{
  "version": 1,
  "course": "course-slug",
  "current_lesson": "day-001",
  "topics": {
    "runtime": {
      "status": "emerging",
      "confidence": 0.55,
      "last_seen": "2026-08-21",
      "next_review": "2026-08-23",
      "evidence": [],
      "misconceptions": []
    }
  }
}
```

Keep `status` qualitative. A multiple-choice score can strengthen retrieval evidence but cannot alone promote a coding topic to `reliable`.

## Quiz session

Save a session before question 1 and after every valid answer. Keep the answer key out of learner-visible transcripts until completion.

```json
{
  "session_id": "timestamp-target-random",
  "status": "active",
  "target": {"course": "course-slug", "lesson_id": "day-001", "title": "Lesson"},
  "settings": {"count": 10, "difficulty": "adaptive", "mode": "inline"},
  "current_index": 1,
  "questions": [],
  "score": {"correct": 0, "answered": 0, "percentage": 0},
  "topics": {}
}
```

## Evidence records

Reference evidence by path rather than duplicating large code blocks. Record whether it is exposure, retrieval, implementation, or transfer evidence. Record hints used, checks actually run, and any uncertainty.

## Learning records

Create a numbered Markdown record only for non-obvious understanding, prior knowledge, corrected misconceptions, or a changed mission. Do not use learning records as a session diary.
