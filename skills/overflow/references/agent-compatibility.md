# Agent Compatibility

## Support model

`overflow` is a portable Agent Skills package. Keep the canonical skill behavior host-neutral, then use the host matrix for discovery paths, invocation details, installation, and validation.

| Tier | Meaning |
| --- | --- |
| A — Native portable | The host discovers standard `SKILL.md`, progressively loads it, and supports explicit invocation or an equivalent skill command. |
| B — Installer-routed | The host can consume the standard package through the open skills installer or a documented copy/link route, with host-specific placement guidance. |
| C — Bridge | Support depends on a community or host bridge and must be documented as experimental. |

## Host matrix

| Host | Tier | Project path | Global path | Invocation |
| --- | --- | --- | --- | --- |
| Claude Code | A | `.claude/skills/<skill>/SKILL.md` | `~/.claude/skills/<skill>/SKILL.md` | `/<skill>` or automatic |
| OpenAI Codex CLI | A | `.agents/skills/<skill>/SKILL.md` | `~/.agents/skills/<skill>/SKILL.md` | Skill picker or explicit skill use |
| Cline | A | `.cline/skills/<skill>/SKILL.md` | `~/.cline/skills/<skill>/SKILL.md` | Slash command or automatic `use_skill` |
| OpenCode | A | `.opencode/skills/<skill>/SKILL.md` or `.agents/skills/<skill>/SKILL.md` | `~/.config/opencode/skills/<skill>/SKILL.md` or `~/.agents/skills/<skill>/SKILL.md` | Native `skill` tool or slash UI |
| Google Antigravity | A | `.agents/skills/<skill>/SKILL.md` | `~/.gemini/config/skills/<skill>/SKILL.md` | Automatic or explicit mention |
| GitHub Copilot / VS Code | A | `.github/skills/<skill>/SKILL.md` | User skill location or configured `chat.agentSkillsLocations` | `/` skill menu or automatic |
| Cursor | B | Host-specific or `.agents/skills` when recognized | Host-specific | Slash command or skill UI |
| Factory Droid | B | Host-specific | Host-specific | Host skill UI |
| Kiro | B | Host-specific | Host-specific | Host skill UI |
| Slate | B | Host-specific | Host-specific | Host skill UI |
| Hermes | B | Host-specific | Host-specific | Host skill UI |
| OpenClaw | C | Bridge-specific | Bridge-specific | Conversational or spawned-agent bridge |
| GBrain | C | Provider-specific | Provider-specific | Provider-specific |

## Portable rules

Use only standard frontmatter in the canonical skill body: `name`, `description`, `license`, `compatibility` when truly required, and string-valued `metadata`. Keep references relative to the skill root. Do not put Claude-only tool names, absolute paths, host-specific shell assumptions, telemetry, or browser machinery in portable instructions.

Every command must work when explicitly invoked and must degrade selectable questions to numbered or lettered text. Orchestration commands such as `/setup-learning`, `/quiz`, `/teach`, `/learn`, and `/handoff` are user-invoked by default. Before stateful learning commands, Overflow may detect whether `.learning/` is missing, draft, partial, initialized, or invalid and must ask before initializing or repairing it. A natural-language request may produce a proposed handoff to another installed skill, but the handoff must be confirmed and must have an explicit-command or text fallback when the host cannot invoke it programmatically. Do not depend on a host-specific question tool for correctness.

## Install

Universal install:

```bash
npx skills add codeKobby/overflow --all
```

Targeted install where the CLI supports host selection:

```bash
npx skills add codeKobby/overflow --all -a claude-code -a codex -a cline -a opencode
```

Manual installation means placing the selected skill directory under the project or global path shown in the matrix. Prefer project-local installation when sharing a team workflow; prefer global installation for personal learning across repositories.

## Validation

A host is supported only after checking discovery, metadata, explicit invocation, relative references, text fallback, and isolation of `.learning/` from host configuration. Review all bundled instructions and scripts before installing because skills can influence tool use and file operations.
