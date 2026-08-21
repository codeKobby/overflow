# Quiz Design

## Continuous interaction

Treat `/quiz` as a session command. Resolve the target, confirm it, save the session, ask question 1, grade the answer, explain it, and immediately ask the next question. Do not require a new slash command between questions.

Default to ten questions for a day and five for a topic. Support `--count N`, `--difficulty easy|medium|hard|adaptive`, `resume`, and `progress`.

## Target examples

All of these should be accepted when they resolve uniquely:

```text
/quiz 1
/quiz 01
/quiz 001
/quiz day 1
/quiz day one
/quiz day-001
/quiz lesson 1
/quiz variables
/quiz "How Programs Run"
/quiz day 1 --count 10
/quiz resume
```

## Question contract

Use single-answer multiple choice with four options labelled A–D. Each question must have one best answer, plausible distractors based on real misconceptions, a concise explanation, a source path, a topic tag, and a difficulty label. Mix concept recall, output prediction, state/data shape, debugging diagnosis, transfer, edge cases, and course-specific safety judgment.

Do not make the correct option conspicuously longer or differently formatted. Avoid trick questions, untaught trivia, and answer choices that reveal the lesson wording.

## Answer handling

Accept a letter, option number, or exact option text. Normalize case and whitespace. If ambiguous, ask for A, B, C, or D without scoring the response. After a valid response:

1. State `Correct` or `Not quite`.
2. Identify the selected option and correct option when different.
3. Explain the decision briefly using the lesson source.
4. Record the topic signal and hint usage.
5. Show the next question immediately unless the session is complete.

Support `hint`, `explain`, `pause`, `save`, `progress`, `finish`, `quit`, and `back`. A hint should reduce evidence strength and never reveal the answer outright.

## Progress interpretation

Correct without a hint is positive retrieval evidence. Correct after a hint is partial retrieval evidence. Repeated errors lower confidence and create a misconception record. A high quiz score without an exercise does not establish implementation mastery.
