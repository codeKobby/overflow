# Repository Detection

Use this procedure before teaching, quizzing, assessing, or reporting progress.

## Locate the course

1. Identify the Git worktree root.
2. Search for `DAY_INDEX.md`, `CURRICULUM_GUIDE.md`, `COURSE_QUALITY_STANDARD.md`, `LESSON_STANDARD.md`, `BEGINNER_TUTORIAL_STANDARD.md`, `EXERCISE_STANDARD.md`, `README.md`, `package.json`, `pyproject.toml`, and lesson directories.
3. Prefer an authoritative day index or curriculum guide over filename sorting.
4. Build a compact map of lessons, titles, headings, outcomes, exercises, hints, solutions, references, checks, and safety documents.
5. Cache the map under `.learning/cache/course-map.json` when scripts are available.

## Recognize known repositories

### JavaScript/TypeScript

Look for `COURSE_QUALITY_STANDARD.md`, `LESSON_TEMPLATE.md`, `package.json`, day folders, matched JavaScript and TypeScript examples, and separate practice files. Preserve runtime parity and use the documented project check.

### Python cybersecurity

Look for `EXERCISE_STANDARD.md`, `SAFETY_AND_LAB_RULES.md`, `SECURITY.md`, `pyproject.toml`, day folders, and local fixtures. Before any security exercise, read the safety and scope documents.

### React/Next.js

Look for `LESSON_STANDARD.md`, `MODERN_TOOLCHAIN.md`, `PROJECT_STRUCTURE_GUIDE.md`, `package.json`, day folders, and separate practice files. Distinguish JavaScript, React, and Next.js behavior.

## Resolve a target

Normalize explicit input in this order:

1. Direct path.
2. Course selector.
3. Integer day/lesson number.
4. Number words such as `one`, `two`, or `twenty-one`.
5. Title, heading, keyword, topic, or directory slug.
6. Saved current lesson.

Accept `day`, `lesson`, `d`, and common separators. Normalize leading zeroes, case, punctuation, and whitespace. For an invalid explicit number, show the nearest valid lessons and ask. For multiple title/topic matches, show the candidates and ask. Never silently select a different lesson.
