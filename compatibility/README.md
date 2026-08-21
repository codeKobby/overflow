# Code Buddy Agent Compatibility

`code-buddy` uses the open Agent Skills format: each command is a folder containing a `SKILL.md`. The package is designed to work across multiple coding agents, but support has levels. A name in the manifest is not, by itself, proof that a host has been tested.

## Install the complete suite

```bash
npx skills add codeKobby/code-buddy --all
```

Install for selected hosts when the installer exposes them:

```bash
npx skills add codeKobby/code-buddy --all \
  -a claude-code \
  -a codex \
  -a cline \
  -a opencode \
  -a antigravity
```

The package is also listed at [`skills.sh/codekobby/code-buddy`](https://skills.sh/codekobby/code-buddy). Search for it with `npx skills find code-buddy`; there is no separate registry-upload command. Use one distribution route per host where possible; do not install both a plugin copy and a skills-CLI copy of the same command because duplicate skill names can be confusing. The package also includes an optional Claude Code plugin manifest at `.claude-plugin/plugin.json`.

## Tier A: native portable support

| Host | Project installation | Global installation | How to invoke |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/<skill>/SKILL.md` | `~/.claude/skills/<skill>/SKILL.md` | `/<skill>` or automatic loading |
| Codex CLI | `.agents/skills/<skill>/SKILL.md` | `~/.agents/skills/<skill>/SKILL.md` | Skill picker or explicit skill use |
| Cline | `.cline/skills/<skill>/SKILL.md` | `~/.cline/skills/<skill>/SKILL.md` | Slash command or automatic `use_skill` |
| OpenCode | `.opencode/skills/<skill>/SKILL.md` or `.agents/skills/<skill>/SKILL.md` | `~/.config/opencode/skills/<skill>/SKILL.md` | Native skill tool or slash UI |
| Antigravity | `.agents/skills/<skill>/SKILL.md` | `~/.gemini/config/skills/<skill>/SKILL.md` | Automatic loading or explicit mention |
| GitHub Copilot / VS Code | `.github/skills/<skill>/SKILL.md` | Configured user skill location | `/` skill menu or automatic loading |

All Tier A hosts consume the same portable `SKILL.md` body. The `agents/openai.yaml` files only provide Codex picker metadata and do not change the portable instructions.

## Tier B: installer-routed support

The package can be selected for Cursor, Factory Droid, Kiro, Slate, and Hermes through the open installer or a host-specific copy route. Their exact current project and global paths can change independently of code-buddy, so the package records these as adapter targets rather than pretending that one path is universal. Confirm the current host documentation before committing a project-local adapter.

## Tier C: bridge support

OpenClaw and GBrain are treated as bridge/provider integrations. OpenClaw can launch or coordinate a supported coding-agent session, while GBrain is optional code intelligence. Neither is required for the core learning workflow, and neither should be described as native portable support until a current host path and smoke test exist.

## What every host must preserve

The learner must be able to run `/setup-learning`, `/teach`, `/quiz`, `/exercise`, `/hint`, `/assess`, and `/learn`, or the host’s equivalent explicit skill command. Selectable questions must degrade to numbered or lettered text. Relative references must resolve. `.learning/` must remain repository-local and separate from host configuration. The host adapter must not weaken learner confirmation, source-citation, privacy, or Python cybersecurity boundaries.

For troubleshooting, compare the host’s skill path with `compatibility/hosts.json`, check that `SKILL.md` is uppercase, verify that `name` matches the directory, and inspect host permissions. OpenCode can hide skills through `opencode.json` permissions; Cline can toggle skills off; Claude Code can have name conflicts across project, personal, plugin, and synced levels.

## Security

Review the contents of any skill before installing it. Skills can influence tool use and file operations. Do not add scripts that silently send repository content to network services. Keep installation and update actions explicit, and ask before writing project configuration or running commands with side effects.
