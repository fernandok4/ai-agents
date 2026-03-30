# AI Agents Frontend Plugin for Claude Code

A collection of specialized AI agents designed to enhance frontend development workflows. This plugin provides tools for UI architecture, component implementation, testing, accessibility auditing, and comprehensive code review — all integrated with Claude Code.

**Stack-agnostic**: All agents adapt to your project's tech stack by reading CLAUDE.md and exploring existing code. Works with React, Vue, Angular, Svelte, Solid, or any other frontend framework.

---

## Table of Contents

- [Installation](#installation)
- [Agents](#agents)
  - [Architecture & Planning](#architecture--planning)
  - [Implementation](#implementation)
  - [Testing](#testing)
  - [Review Specialists](#review-specialists)
- [Background Skills](#background-skills)
- [Typical Workflows](#typical-workflows)

---

## Installation

This plugin is available through the Claude Code plugin system. Add it to your Claude Code configuration to enable all agents and skills.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents) (frontend directory)

---

## Agents

Agents are specialized, independent AI assistants. Each runs in its own context window with specific tool access. Every agent can be used standalone — they are not tied to any specific workflow.

### Architecture & Planning

#### Frontend Architect

**Use when**: You need a detailed implementation specification for a UI feature, page, or component system.

**What it produces**: `spec.md` containing:
- Executive summary and user interactions
- Component architecture with props interfaces and hierarchy
- State management strategy
- API integration and data flow
- Routing and navigation
- Styling and responsive design
- Accessibility specification
- Performance considerations
- Implementation phases and testing strategy

---

### Implementation

#### Frontend Developer

**Use when**: You want to implement a UI feature from instructions or an architect's plan. Also makes failing TDD tests pass (green phase).

**Stack-agnostic**: Reads CLAUDE.md and existing code to adapt to any frontend stack automatically. Learns and remembers the project's design system.

**Capabilities**:
- Implements components, pages, hooks, and state management
- Follows the project's design system and conventions
- Makes failing TDD tests pass (red → green → refactor)
- Fixes HIGH and CRITICAL review findings
- Prioritizes accessibility and semantic HTML

---

### Testing

#### Frontend QA Engineer

**Use when**: You need test specifications, TDD test code, or e2e test scenarios for frontend features.

**Four modes**:
1. **TDD Test Specification** — generates numbered test case lists before implementation
2. **TDD Test Code (Red Phase)** — writes actual failing test files
3. **E2E Test Planning** — maps complete user journeys with keyboard/screen reader paths
4. **Test Review** — identifies coverage gaps and test quality issues

---

### Review Specialists

#### Frontend Quality Reviewer

**Use when**: You need a code quality review of frontend changes.

**Focus areas**: Component architecture, props design, state management, styling consistency, code duplication, naming conventions, test coverage.

**Output**: `quality-review.md`

---

#### Frontend Security Reviewer

**Use when**: You need a security review of frontend changes.

**Focus areas**: XSS prevention, token storage, sensitive data exposure, third-party script risks, open redirects, PostMessage security.

**Output**: `security-review.md`

---

#### Frontend Performance Reviewer

**Use when**: You need a performance review of frontend changes.

**Focus areas**: Re-render optimization, bundle size, code splitting, Web Vitals (LCP, INP, CLS), data fetching patterns, memory leaks, image optimization.

**Output**: `performance-review.md`

---

#### Accessibility Reviewer

**Use when**: You need an accessibility audit of frontend changes.

**Focus areas**: WCAG 2.2 Level AA compliance, semantic HTML, ARIA patterns, keyboard navigation, screen reader compatibility, color contrast, focus management.

**Output**: `accessibility-review.md`

---

## Background Skills

Background skills (`user-invocable: false`) are auto-injected into agents via the `skills:` frontmatter field, providing shared thresholds and criteria.

| Skill | Used By | Purpose |
|-------|---------|---------|
| `severity-standards` | All reviewers | Unified CRITICAL/HIGH/MEDIUM/LOW severity definitions |
| `frontend-quality-standards` | frontend-architect, frontend-quality-reviewer | Component size, complexity, duplication, test coverage, over-engineering thresholds |
| `frontend-performance-standards` | frontend-architect, frontend-performance-reviewer | Web Vitals targets, bundle budgets, rendering, data fetching, memory |
| `frontend-security-standards` | frontend-security-reviewer | Client-side OWASP checklist, XSS patterns, secrets detection |

---

## Typical Workflows

### New Feature — Manual Step-by-Step

```bash
# 1. Create detailed specification
# (Claude delegates to frontend-architect)
Create a spec for a dashboard with real-time charts and filters

# 2. Implement the feature
# (Claude delegates to frontend-developer)
Implement the spec

# 3. Run comprehensive review (all 4 specialists)
# (manually launch the 4 reviewers in parallel)
Review the changes for quality, security, performance, and accessibility

# 4. Create semantic commits
/semantic-commit
```

### Before a Pull Request

```bash
# Launch all 4 reviewers for a comprehensive check
Review the frontend changes for quality, security, performance, and accessibility
```

### Accessibility Audit

```bash
# Focused accessibility review
Review the checkout page components for accessibility
```

---

## Project Structure

```
frontend/
├── agents/
│   ├── frontend-developer.md       # Stack-agnostic UI implementer + TDD green phase
│   ├── frontend-architect.md       # Produces spec.md for UI features
│   ├── frontend-qa-engineer.md     # Test writer + test planning
│   ├── frontend-quality-reviewer.md    # → quality-review.md
│   ├── frontend-security-reviewer.md   # → security-review.md
│   ├── frontend-performance-reviewer.md # → performance-review.md
│   └── accessibility-reviewer.md       # → accessibility-review.md
├── skills/
│   ├── severity-standards/             # Background: unified severity levels
│   ├── frontend-quality-standards/     # Background: component quality thresholds
│   ├── frontend-performance-standards/ # Background: Web Vitals & bundle budgets
│   └── frontend-security-standards/    # Background: client-side security patterns
├── standards/
│   ├── file-conventions.md
│   └── review-orchestration.md
├── CLAUDE.md
└── README.md
```

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.

---

## License

This project is open source. See the repository for license details.
