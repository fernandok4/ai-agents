# AI Agents Plugin

## Git Commits

Never add `Co-Authored-By` lines to commit messages. Do not include Claude as a co-author.

## Agent Orchestration

When orchestrating multiple agents, always prioritize using `TeamCreate` or `TeamAgent` over launching agents individually with the `Agent` tool. Teams provide better coordination, parallel execution, and structured communication between agents.

## Design Principles

### Agents Must Be Independent

Every agent must be self-contained and usable standalone — never tied to a specific workflow or skill. An agent must have a clear step-by-step of what it does, but it must work on its own without requiring a particular orchestration flow.

- Agents must NOT assume they are part of a pipeline (e.g., `/tdd`)
- Dependencies on other agents' outputs (`spec.md`, `test-plan.md`, `overall-review.md`) must be optional or clearly stated as prerequisites — not implicit workflow assumptions
- Communication with other agents (via `SendMessage`) must be conditional — if the other agent is not available, fall back to asking the user
- Descriptions and instructions must use "Use when..." language, not "Auto-delegates when the `/tdd` skill..."

### Skills and Agents Must Be Generic and Portable

When creating or editing skills and agents, never include references that are specific to a particular machine, user, or environment. They must work for any user without modification.

- Never hardcode absolute paths (e.g., `/Users/someone/...`)
- Never reference specific project names or local workspace structures
- Never mention specific database names, table names, or connection details
- Use relative paths, glob patterns, or environment-based discovery instead

### Always Pursue the Best Solution

Agents must always strive to find the best solution in terms of **performance** and **code quality**. Do not settle for the first approach that works — evaluate alternatives, consider trade-offs, and choose the option that is most efficient, maintainable, and robust.

- Prefer algorithms and data structures with optimal time/space complexity for the problem at hand
- Write clean, readable code that follows established patterns and best practices
- When multiple approaches exist, briefly reason about trade-offs before choosing
- Avoid unnecessary allocations, redundant operations, and inefficient patterns

### TDD Workflow Roles

In the TDD workflow (`/tdd` skill):
- **qa-engineer**: Writes the failing test code (red phase). Bridges specifications and executable tests.
- **backend-developer**: Makes the failing tests pass (green phase) and refactors. Also fixes HIGH/CRITICAL review findings.

The `backend-developer` is stack-agnostic — it reads CLAUDE.md and existing code to adapt to any tech stack automatically.

### Review Consolidation

There is no dedicated overall-reviewer agent. Review consolidation (reading the 3 specialist review files and determining a GO/CONDITIONAL GO/NO-GO verdict) is done **inline by the skill** that orchestrates the review (`/tdd`, `/project-review`, `/mr-code-review`).

## Project Structure

```
agents/          # Subagent configurations (.md files with frontmatter)
skills/          # Skills invoked via /skill-name (each has SKILL.md)
standards/       # Shared reference tables
helper/          # Internal reference material
```
