# AI Agents Frontend Plugin

## Git Commits

Never add `Co-Authored-By` lines to commit messages. Do not include Claude as a co-author.

## Agent Orchestration

When orchestrating multiple agents, always prioritize using `TeamCreate` or `TeamAgent` over launching agents individually with the `Agent` tool. Teams provide better coordination, parallel execution, and structured communication between agents.

## Design Principles

### Agents Must Be Independent

Every agent must be self-contained and usable standalone — never tied to a specific workflow or skill. An agent must have a clear step-by-step of what it does, but it must work on its own without requiring a particular orchestration flow.

- Agents must NOT assume they are part of a pipeline
- Dependencies on other agents' outputs (`spec.md`, `test-plan.md`, `overall-review.md`) must be optional or clearly stated as prerequisites — not implicit workflow assumptions
- Communication with other agents (via `SendMessage`) must be conditional — if the other agent is not available, fall back to asking the user
- Descriptions and instructions must use "Use when..." language, not "Auto-delegates when..."

### Skills and Agents Must Be Generic and Portable

When creating or editing skills and agents, never include references that are specific to a particular machine, user, or environment. They must work for any user without modification.

- Never hardcode absolute paths (e.g., `/Users/someone/...`)
- Never reference specific project names or local workspace structures
- Never mention specific framework versions, component library versions, or design system specifics
- Use relative paths, glob patterns, or environment-based discovery instead
- Design system knowledge comes from CLAUDE.md or project memory — never baked into agents

### Always Pursue the Best Solution

Agents must always strive to find the best solution in terms of **performance**, **accessibility**, and **code quality**. Do not settle for the first approach that works — evaluate alternatives, consider trade-offs, and choose the option that is most efficient, maintainable, and robust.

- Prefer semantic HTML over div soup with ARIA overrides
- Write clean, readable code that follows established patterns and best practices
- When multiple approaches exist, briefly reason about trade-offs before choosing
- Avoid unnecessary re-renders, oversized bundles, and inaccessible patterns

### Design System Awareness

Agents learn the project's design system from CLAUDE.md and existing code. They store design patterns, tokens, and conventions in project memory for reuse across conversations. No agent should assume a specific UI library or design system — they adapt to what the project uses.

## Project Structure

```
agents/          # Subagent configurations (.md files with frontmatter)
skills/          # Skills invoked via /skill-name (each has SKILL.md)
standards/       # Shared reference tables
helper/          # Internal reference material
```
