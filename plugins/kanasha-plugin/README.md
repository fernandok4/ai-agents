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
  - [Architecture & Planning](#architecture--planning)
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
# One command — spec, team assembly, TDD red-green-refactor, review, and fixes
/tdd Add a payment processing endpoint that charges a stored card
```

### Manual Step-by-Step

```bash
# 1. Create a detailed implementation spec
# (Claude delegates to the software-architect agent)
Create an implementation spec for user authentication with JWT

# 2. Implement the specification
# (Claude delegates to the backend-developer agent)
Implement the spec

# 3. Review the code before committing
/project-review

# 4. Create semantic commits
/semantic-commit
```

---

## Skills

Skills are invoked manually with `/skill-name`. They provide structured workflows for specific tasks.

### Development Workflow

#### `/tdd <feature description>`

**Purpose**: Full TDD development lifecycle from feature description to reviewed, production-ready code.

**What it does**:
1. Runs `software-architect` to generate `spec.md` — **waits for your approval**
2. Runs `tech-team-architect` to design the TDD team → `team-plan.md`
3. Executes the team plan (typically: `qa-engineer` writes failing tests, `backend-developer` makes them pass)
4. Runs specialist reviewers in parallel
5. Consolidates review findings inline with a deployment verdict
6. Fixes all HIGH and CRITICAL findings, then re-reviews

**Key guarantees**:
- Spec is always approved by you before any code is written
- Team composition is decided by `tech-team-architect`, not hardcoded
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
| `quality-standards` | software-architect, quality-reviewer | Function size, complexity, duplication, test coverage, over-engineering thresholds |
| `performance-standards` | software-architect, performance-reviewer | Scale assumptions, algorithm complexity, database, caching, resource usage, concurrency |
| `security-standards` | security-reviewer | OWASP Top 10 checklist, secrets detection patterns, security severity definitions |
| `severity-standards` | quality-reviewer, performance-reviewer, security-reviewer | Unified CRITICAL/HIGH/MEDIUM/LOW severity definitions |

---

## Agents

Agents are specialized, independent AI assistants. Each runs in its own context window with specific tool access. Every agent can be used standalone — they are not tied to any specific workflow or skill.

### Architecture & Planning

#### Software Architect

**Use when**: You need a detailed implementation specification or design.

**What it produces**: `spec.md` containing:
- Executive summary
- Files to create/modify with exact paths
- Classes and methods with signatures
- Performance and scalability considerations
- Implementation order and phases
- Testing strategy

---

#### Tech Team Architect

**Use when**: You have a task or spec and need to plan team composition, roles, and execution order.

**What it produces**: `team-plan.md` containing:
- Team member roles with responsibilities and deliverables
- Execution order with dependency graph
- Risk register and production readiness checklist

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
# One command does everything:
# software-architect → approval → tech-team-architect → team execution → review → fix
/tdd Add a product catalogue endpoint with price variants and entitlement checks
```

### New Feature — Manual Step-by-Step

```bash
# 1. Create detailed specification
# (Claude delegates to software-architect)
Create a spec for rate limiting on API endpoints

# 2. Implement the feature
# (Claude delegates to backend-developer)
Implement the spec

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
│   ├── software-architect.md    # Produces spec.md
│   ├── tech-team-architect.md   # Team composition strategist → team-plan.md
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
