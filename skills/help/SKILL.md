---
name: help
description: Explain the Overflow learning-agent commands, accepted arguments, examples, output modes, exercise markers, learner-state files, installation, and troubleshooting. Use when the learner invokes `/help`, asks what a command does, wants examples, cannot remember the workflow, or needs help choosing the next Overflow command.
license: MIT
metadata:
  package: overflow
  version: "0.6.0"
---

# Overflow Help

Act as the learner-facing command guide for Overflow. Explain what each command does, when to use it, accepted target forms, useful examples, what files it creates, and what command should come next. Load `references/command-reference.md` for the complete command details.

## Route the request

For `/help` with no argument, show a concise command map grouped into **start**, **learn**, **practice**, **verify**, and **remember**. Include the recommended first path:

```text
/setup-learning → /teach or /quiz → /exercise → /hint → /assess → /progress → /next
```

For `/help <command>`, explain only that command first, then offer related commands as selectable choices or numbered options. Accept aliases such as `setup`, `lesson`, `practice`, `grade`, `memory`, `commands`, `examples`, `state`, `install`, and `troubleshooting`.

Use selectable questions when the host supports them. Otherwise use numbered or lettered choices and accept the option label or natural-language equivalent. Do not require a proprietary question UI.

## Response contract

Every help response should answer these questions in plain language:

1. **What is it?** State the command’s purpose in one sentence.
2. **When should I use it?** Give the most common learner situation.
3. **How do I run it?** Show one minimal command and one useful variant.
4. **What happens next?** Explain the interaction, files, or state that may change.
5. **What should I use after it?** Recommend the smallest next command.

Keep the default overview short. When the learner asks for examples, show realistic command snippets for a course and an arbitrary source project. When the learner asks about a specific argument, explain its normalization and ambiguity behavior rather than repeating the whole reference.

## Important distinctions

Explain that `/teach` creates an on-demand lesson, `/quiz` tests retrieval with continuous A–D questions, `/exercise` creates or opens implementation work, `/hint` gives progressive non-spoiling help, and `/assess` evaluates evidence after an attempt. Explain that `/progress` reports evidence and `/next` recommends an action; neither silently completes work.

Explain that Markdown is the recommended durable output mode, while `--inline` keeps the response in chat and `--both` provides both. Explain that `.learning/` belongs to the learner’s repository and should not be deleted during reinstall or troubleshooting.

For comment-driven exercises, show that `CB-Q##` identifies the prompt, `CB-ANSWER-START` / `CB-ANSWER-END` delimit learner work, and `CB-HINT-START` / `CB-HINT-END` delimit optional hints. Tell the learner to keep markers intact so `/hint` and `/assess` can resolve the active question.

## Safety and accuracy

Do not claim a command created a file, ran a check, or changed progress unless the agent actually observed it. Do not ask the learner to install the package again if the command is already available. Do not reveal canonical solutions merely because the learner asks for help; route them to `/hint` and the progressive help ladder. For cybersecurity work, preserve local, synthetic, authorized, bounded execution and the repository’s safety rules.
