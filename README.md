# Kanasha Marketplace for Claude Code and Codex

A marketplace of specialized AI agent plugins and skills for Claude Code and Codex, providing tools for TDD, code review, accessibility auditing, wiki workflows, and more.

---

## Plugins

### kanasha-plugin

Backend-focused agents and skills for architecture, TDD implementation, code review, and database operations.

**Agents**: backend-developer, database-specialist, qa-engineer, e2e-test-runner, quality-reviewer, security-reviewer, performance-reviewer

Architecture and team composition are handled via Claude Code's built-in Plan mode — no dedicated architect agent.

**Skills**: `/tdd`, `/project-review`, `/deep-web-search`, `/semantic-commit`, `/db-query`

[Full documentation](plugins/kanasha-plugin/README.md)

---

### kanasha-frontend-plugin

Frontend-focused agents and skills for UI architecture, component implementation, testing, accessibility auditing, and code review. Stack-agnostic — works with React, Vue, Angular, Svelte, or any frontend framework.

**Agents**: frontend-developer, frontend-qa-engineer, frontend-quality-reviewer, frontend-security-reviewer, frontend-performance-reviewer, accessibility-reviewer

Architecture and design decisions are handled via Claude Code's built-in Plan mode — no dedicated architect agent.

[Full documentation](plugins/kanasha-frontend-plugin/README.md)

---

## Installation

These plugins are available through the Claude Code plugin system and through Codex local marketplace metadata.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents)

### Claude Code

Claude Code reads the existing `.claude-plugin/marketplace.json` file.

### Codex

Codex reads the repo marketplace at `.agents/plugins/marketplace.json`. The marketplace points to Codex-specific plugin folders under `codex/plugins/`, and each plugin includes a required `.codex-plugin/plugin.json` manifest that points to its bundled `skills/` directory.

Open Codex in this repository and use `/plugins` to inspect and install the local entries:

```bash
codex
/plugins
```

After installing a plugin, start a new Codex thread and invoke a bundled skill explicitly with `$skill-name`, or describe the task and let Codex choose a matching skill from its description.

### Codex compatibility notes

- Codex `skills/*/SKILL.md` files are copied into `codex/plugins/*` with Codex-compatible frontmatter.
- Claude Code keeps using the original `plugins/*` tree, including Claude-specific frontmatter such as `user-invocable` and `argument-hint`.
- Existing Claude `agents/*.md` files are not automatically Codex custom agents. Codex custom agents use standalone TOML files under `.codex/agents/` or `~/.codex/agents/`, so converting the Claude agents is a separate follow-up.
- The Codex tree avoids globally duplicated skill names where practical, for example by using separate backend and frontend severity standards.

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.

---

## License

This project is open source. See the repository for license details.
