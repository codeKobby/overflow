---
name: quiz
description: Run continuous multiple-choice programming quizzes from the current repository’s lessons, documentation, files, symbols, tests, or existing codebase. Accept day 1, 01, 001, day one, lesson names, topics, resume, and progress targets; grade each A–D answer and immediately continue to the next question. Use when the user asks for a quiz or wants to test understanding.
license: MIT
metadata:
  package: overflow
  version: "0.2.0"
---

# Overflow Quiz

Run a normal continuous quiz session grounded in the current repository. Do not require a new command between questions. Present target, count, difficulty, output mode, and optional settings as selectable questions when supported; otherwise use numbered or lettered text with the same choices and accept text equivalents.

## Resolve the target

Accept `/quiz`, `/quiz 1`, `/quiz 01`, `/quiz 001`, `/quiz day 1`, `/quiz day one`, `/quiz day-001`, `/quiz lesson 1`, `/quiz variables`, `/quiz src/parser.py`, `/quiz "Lesson Title"`, `/quiz resume`, and `/quiz progress`.

Normalize leading zeroes, number words, punctuation, separators, case, `day`/`lesson` aliases, filenames, headings, symbols, functions, tests, keywords, and topics. Prefer an explicit path, course, day number, title/topic, symbol, then saved current lesson. If no formal lesson exists, quiz the selected codebase using its docs, tests, and implementation. Confirm the interpretation before question 1. If an explicit target is invalid or ambiguous, show candidates and ask instead of silently switching targets.

## Start and continue the session

Default to ten questions for a day and five for a topic. If count or difficulty is not already stored, ask with selectable options and mark the default. Support `--count N` and `--difficulty easy|medium|hard|adaptive`. Use single-answer questions with exactly four options labelled A–D.
 Mix concept retrieval, code tracing, output prediction, debugging diagnosis, transfer choices, edge cases, and cybersecurity scope judgment where appropriate.

Save the session before question 1 and after every answer under `.learning/quiz-sessions/`. Keep the answer key out of learner-visible active transcripts. Ask one question. When the learner answers with a letter, option number, or exact option text, normalize it, grade it, explain the result briefly, and immediately show the next question.

After each valid answer:

1. State `Correct` or `Not quite`.
2. Identify the selected option and correct option when different.
3. Explain the decision using the lesson source.
4. Record the topic, hint usage, and evidence strength.
5. Present the next question unless the session is complete.

An ambiguous answer is clarification, not a wrong answer. Present session controls such as hint level, pause, save, progress, finish, quit, and back as selectable options when the agent supports them, while accepting those words in text. Support `hint`, `explain`, `pause`, `save`, `progress`, `finish`, `quit`, and `back`.
 A hint must not reveal the answer. `/quiz resume` resumes the latest incomplete session.

## Completion

Write a Markdown report under `.learning/quiz-reports/` with target, score, question count, topic breakdown, missed questions, misconceptions, hints used, source anchors, and next action. Link it to the selected lesson or project-map target and later assessment or learning record by relative path. Correct answers without hints are retrieval evidence. Correct answers after hints are weaker evidence. A high quiz score alone must not mark implementation mastery; recommend an exercise, prediction, or assessment when appropriate.

Use `.learning/progress.json` if present. If it is absent, recommend `/setup-learning` and maintain only the current session until setup is complete.
