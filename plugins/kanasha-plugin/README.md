# AI Agents Plugin for Claude Code

A collection of specialized AI agents and skills designed to enhance your development workflow. This plugin provides powerful tools for architecture, TDD implementation, and code review—all integrated with Claude Code.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Skills](#skills)
  - [Development Workflow](#development-workflow)
  - [Background Skills](#background-skills)
- [Agents](#agents)
  - [Implementation](#implementation)
  - [Testing](#testing)
  - [Review Specialists](#review-specialists)
- [Typical Workflows](#typical-workflows)

---

## Installation

This plugin is available through the Claude Code plugin system. Add it to your Claude Code configuration to enable all agents and skills.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents)

---

## Quick Start

### Full TDD Workflow (recommended for new features)

```bash
# 1. Use Plan mode to design the feature and produce a plan/spec
# 2. Run TDD against the approved plan — red-green, review, and fixes
/tdd Add a payment processing endpoint that charges a stored card
```

### Manual Step-by-Step

```bash
# 1. Use Plan mode to design the implementation
# (Claude Code's built-in Plan mode replaces any architect agent)

# 2. Implement the plan
# (Claude delegates to the backend-developer agent)
Implement the plan

# 3. Review the code before committing
/project-review

# 4. Create semantic commits
/semantic-commit
```

---

## Skills

Skills are invoked manually with `/skill-name`. They provide structured workflows for specific tasks.

### Development Workflow

#### `/tdd <feature description or path to spec.md>`

**Purpose**: TDD development lifecycle from an approved plan to reviewed, production-ready code.

**Prerequisite**: Architecture and design decisions must already be settled — use Plan mode (or write a `spec.md` manually) before invoking this skill.

**What it does**:
1. Confirms the plan (from a `spec.md` or a detailed feature description)
2. Runs `qa-engineer` to write failing tests (red phase)
3. Runs `backend-developer` to make them pass (green phase) — adds `database-specialist` or `frontend-developer` when the plan requires it
4. Runs specialist reviewers in parallel
5. Consolidates review findings inline with a deployment verdict
6. Fixes all HIGH and CRITICAL findings, then re-reviews

**Key guarantees**:
- Architecture is decided upstream by you (Plan mode or manual spec) — this skill executes, it does not design
- Default team is `qa-engineer` → `backend-developer` → three reviewers; extra roles are added only when the plan calls for them
- HIGH and CRITICAL review issues are always fixed before the workflow ends
- Review consolidation is inline — no separate overall-reviewer agent

**Example**:
```bash
/tdd Add a payment processing endpoint that charges a stored card and emits a payment.completed event
/tdd Implement user MFA with TOTP and email fallback
```

---

#### `/project-review [target]`

**Purpose**: Run a comprehensive code review with multiple specialists.

**What it does**:
- Launches three specialist reviewers in parallel:
  - **Performance**: Algorithm complexity, resource usage, scalability
  - **Security**: OWASP Top 10, vulnerabilities, authentication
  - **Quality**: Code smells, architecture, testing
- Consolidates findings inline with a deployment verdict (GO / CONDITIONAL GO / NO-GO)

**Default target**: Uncommitted changes.

**Output files**:
- `performance-review.md`
- `security-review.md`
- `quality-review.md`

**Example**:
```bash
/project-review
/project-review src/services/
```

---

#### `/deep-web-search <topic>`

**Purpose**: Perform a thorough internet search on any topic.

**What it does**:
- Searches Stack Overflow, official docs, GitHub, and more
- Compiles findings into a single organized Markdown file
- Names the file `search_<topic>_YYYYMMDD.md`

**Example**:
```bash
/deep-web-search Claude API streaming
/deep-web-search PostgreSQL indexing strategies
```

---

#### `/semantic-commit`

**Purpose**: Create clean, semantic commits for your changes.

**What it does**:
- Creates **one commit per modified file**
- Uses semantic commit types (feat, fix, docs, refactor, etc.)
- Keeps messages concise and in English
- Never uses destructive git commands

**Example**:
```bash
/semantic-commit
```

---

#### `/db-query`

**Purpose**: Query databases in read-only mode.

**What it does**:
- Connects to databases and runs SELECT queries
- Validates data, checks records, investigates issues
- Read-only — never modifies data

**Example**:
```bash
/db-query Show me the last 10 users created
```

---

### Background Skills

Background skills (`user-invocable: false`) are not invoked directly. They are auto-injected into agents via the `skills:` frontmatter field, providing shared thresholds and criteria in a single place.

| Skill | Used By | Purpose |
|-------|---------|---------|
| `quality-standards` | quality-reviewer | Function size, complexity, duplication, test coverage, over-engineering thresholds |
| `performance-standards` | performance-reviewer | Scale assumptions, algorithm complexity, database, caching, resource usage, concurrency |
| `security-standards` | security-reviewer | OWASP Top 10 checklist, secrets detection patterns, security severity definitions |
| `severity-standards` | quality-reviewer, performance-reviewer, security-reviewer | Unified CRITICAL/HIGH/MEDIUM/LOW severity definitions |

---

## Agents

Agents are specialized, independent AI assistants. Each runs in its own context window with specific tool access. Every agent can be used standalone — they are not tied to any specific workflow or skill.

### Architecture & Planning

Architecture, design, and team composition are handled outside this plugin using Claude Code's built-in **Plan mode**. Produce a `spec.md` (or equivalent plan) first, then invoke `/tdd` or launch `backend-developer` directly against it.

---

### Implementation

#### Backend Developer

**Use when**: You want to implement a feature from instructions or an architect's plan. Also makes failing TDD tests pass (green phase).

**Stack-agnostic**: Reads CLAUDE.md and existing code to adapt to any tech stack automatically.

**Capabilities**:
- Implements features following architectural plans
- Makes failing TDD tests pass (red → green → refactor)
- Fixes HIGH and CRITICAL review findings
- Discovers and follows project conventions automatically

---

#### Database Specialist

**Use when**: You need database schema design, migration creation, query optimization, or repository layer implementation.

**Focus areas**: PostgreSQL, JPA/Hibernate, Flyway migrations, index optimization, query performance analysis.

---

### Testing

#### QA Engineer

**Use when**: You need test specifications, TDD test code, frontend flow mapping, or system-level testing.

**Four modes**:
1. **TDD Test Specification** — generates numbered test case lists before implementation
2. **Test List from Specification** — creates comprehensive test matrices from feature specs
3. **Frontend Flow Mapping** — documents user journeys with API calls and edge cases
4. **System Testing via curl** — tests running endpoints with systematic curl commands

In the `/tdd` workflow, the QA Engineer writes the actual failing test code (red phase).

---

#### E2E Test Runner

**Use when**: You need to test a running microservice application end-to-end via API calls.

**What it does**: Executes systematic API tests, validates responses, and produces comprehensive test reports.

---

### Review Specialists

#### Performance Reviewer

**Use when**: You need a performance review of code changes.

**Focus areas**: Algorithm complexity, database query optimization, caching opportunities, resource usage, concurrency and scalability.

**Output**: `performance-review.md`

---

#### Security Reviewer

**Use when**: You need a security review of code changes.

**Focus areas**: OWASP Top 10 vulnerabilities, injection attacks, authentication flaws, secrets management, cryptographic practices.

**Output**: `security-review.md`

---

#### Quality Reviewer

**Use when**: You need a code quality review of changes.

**Focus areas**: Code smells, pattern violations, test coverage, architecture, production readiness.

**Output**: `quality-review.md`

---

## Typical Workflows

### New Feature — Full TDD Workflow

```bash
# 1. Use Plan mode to design the feature
# 2. Run /tdd against the approved plan:
#    plan confirmation → qa-engineer (red) → backend-developer (green) → review → fix
/tdd Add a product catalogue endpoint with price variants and entitlement checks
```

### New Feature — Manual Step-by-Step

```bash
# 1. Use Plan mode to design the implementation
# (Claude Code's built-in Plan mode — no dedicated agent)

# 2. Implement the plan
# (Claude delegates to backend-developer)
Implement the plan

# 3. Run comprehensive review
/project-review

# 4. Create semantic commits
/semantic-commit
```

### Before a Pull Request

```bash
# Comprehensive review (orchestrates all 3 specialists)
/project-review
```

---

## Project Structure

```
ai-agents/
├── agents/              # Subagent configurations (isolated context, heavy workflows)
│   ├── backend-developer.md     # Stack-agnostic backend implementer + TDD green phase
│   ├── qa-engineer.md           # TDD test writer + test planning + system testing
│   ├── e2e-test-runner.md       # End-to-end API test runner
│   ├── database-specialist.md   # Schema, migrations, query optimization
│   ├── quality-reviewer.md      # → quality-review.md
│   ├── security-reviewer.md     # → security-review.md
│   └── performance-reviewer.md  # → performance-review.md
├── skills/              # Skills (manual-trigger workflows with SKILL.md)
│   ├── tdd/                     # /tdd — full TDD workflow orchestrator
│   ├── project-review/
│   ├── deep-web-search/
│   ├── semantic-commit/
│   ├── db-query/
│   ├── quality-standards/       # Background: code quality thresholds
│   ├── performance-standards/   # Background: performance & scalability criteria
│   ├── security-standards/      # Background: OWASP Top 10 & secrets detection
│   └── severity-standards/      # Background: unified severity levels
├── standards/           # Reference tables
│   ├── file-conventions.md
│   └── review-orchestration.md
└── README.md
```

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.

---

## License

This project is open source. See the repository for license details.
