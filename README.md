# Kanasha Marketplace for Claude Code

A marketplace of specialized AI agent plugins for Claude Code, providing powerful tools for architecture, TDD, code review, accessibility auditing, and more.

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

These plugins are available through the Claude Code plugin system. Add the marketplace and enable the plugins you need.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents)

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.

---

## License

This project is open source. See the repository for license details.
