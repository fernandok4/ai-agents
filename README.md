# AI Agents Plugin for Claude Code

A collection of specialized AI agents and commands designed to enhance your development workflow. This plugin provides powerful tools for research, implementation, code review, and product management—all integrated with Claude Code.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
  - [Development Workflow](#development-workflow)
  - [Code Review](#code-review)
  - [Utilities](#utilities)
- [Agents](#agents)
  - [Research & Planning](#research--planning)
  - [Implementation](#implementation)
  - [Review Specialists](#review-specialists)
  - [Product Management](#product-management)
- [Typical Workflows](#typical-workflows)

---

## Installation

This plugin is available through the Claude Code plugin system. Add it to your Claude Code configuration to enable all agents and commands.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents)

---

## Quick Start

Here's a typical workflow from idea to implementation:

```bash
# 1. Research how to implement a feature
/project-search Add user authentication with JWT

# 2. Create a detailed implementation spec
/spec

# 3. Implement the specification
/implement

# 4. Review the code before committing
/review

# 5. Create semantic commits
/semantic-commit
```

---

## Commands

### Development Workflow

#### `/project-search <description>`

**Purpose**: Research project patterns and technical solutions before implementing a feature.

**What it does**:
- Analyzes your codebase to find existing patterns
- Searches the internet for best practices
- Creates an `initial-search.md` file with all findings

**Example**:
```bash
/project-search Add JWT authentication to API routes
/project-search Refactor form validation to use Zod
/project-search Implement Redis cache for frequent queries
```

---

#### `/spec`

**Purpose**: Transform research into a detailed implementation specification.

**What it does**:
- Reads `initial-search.md` (created by `/project-search`)
- Creates `spec.md` with concrete file paths, method signatures, and implementation steps
- Focuses on performance, scalability, and maintainability

**Prerequisites**: Run `/project-search` first.

**Example**:
```bash
/spec
```

---

#### `/implement [spec-file]`

**Purpose**: Execute an implementation specification.

**What it does**:
- Reads the spec file (defaults to `spec.md`)
- Implements exactly what's specified—no more, no less
- Creates `questions.md` if clarification is needed before proceeding

**Example**:
```bash
/implement
/implement custom-spec.md
```

---

### Code Review

#### `/review [target]`

**Purpose**: Run a comprehensive code review with multiple specialists.

**What it does**:
- Launches three specialist reviewers in parallel:
  - **Performance**: Algorithm complexity, resource usage, scalability
  - **Security**: OWASP Top 10, vulnerabilities, authentication
  - **Quality**: Code smells, architecture, testing
- Synthesizes findings into `overall-review.md` with a deployment decision

**Default target**: Uncommitted changes.

**Output files**:
- `performance-review.md`
- `security-review.md`
- `quality-review.md`
- `overall-review.md`

**Example**:
```bash
/review
/review src/services/
```

---

#### `/performance-review [target]`

**Purpose**: Deep performance analysis.

**What it does**:
- Analyzes algorithm complexity (Big-O notation)
- Identifies N+1 queries and database bottlenecks
- Finds caching opportunities
- Evaluates resource usage (CPU, memory, I/O)
- Creates `performance-review.md`

**Example**:
```bash
/performance-review
/performance-review src/controllers/
```

---

#### `/security-review [target]`

**Purpose**: Security analysis following OWASP Top 10.

**What it does**:
- Checks for injection vulnerabilities (SQL, XSS, command)
- Identifies authentication and authorization issues
- Scans for hardcoded secrets
- Evaluates cryptographic practices
- Creates `security-review.md`

**Example**:
```bash
/security-review
/security-review src/auth/
```

---

#### `/quality-review [target]`

**Purpose**: Code quality and maintainability review.

**What it does**:
- Detects code smells and complexity issues
- Evaluates architecture and design patterns
- Checks test coverage and quality
- Assesses production readiness
- Creates `quality-review.md`

**Example**:
```bash
/quality-review
```

---

### Utilities

#### `/deep-search <topic>`

**Purpose**: Perform a thorough internet search on any topic.

**What it does**:
- Searches Stack Overflow, official docs, GitHub, and more
- Compiles findings into a single organized Markdown file
- Names the file `search_<topic>_YYYYMMDD.md`

**Example**:
```bash
/deep-search Claude API streaming
/deep-search PostgreSQL indexing strategies
/deep-search React Server Components
```

---

#### `/semantic-commit`

**Purpose**: Create clean, semantic commits for your changes.

**What it does**:
- Creates **one commit per modified file**
- Uses semantic commit types (feat, fix, docs, refactor, etc.)
- Keeps messages concise and in English
- Never uses destructive git commands

**Commit types**:
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `refactor` | Code refactoring |
| `test` | Test additions/modifications |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |
| `style` | Code style/formatting |

**Example**:
```bash
/semantic-commit
```

---

#### `/think-on-tests <class-path>`

**Purpose**: Generate a comprehensive test plan without writing code.

**What it does**:
- Analyzes the target class and its dependencies
- Documents every test case using the AAA pattern (Arrange, Act, Assert)
- Covers success paths, edge cases, and failure scenarios
- Creates `testsScenarios/<path/to/class>.md`

**Example**:
```bash
/think-on-tests src/controllers/UserController.ts
/think-on-tests src/services/PaymentService.ts
```

---

### Product Management

#### `/product-advisor <question>`

**Purpose**: Get product insights, brainstorm features, or analyze requirements.

**What it does**:
- Answers questions about how the product works
- Helps brainstorm new feature ideas
- Creates user stories and acceptance criteria
- Applies prioritization frameworks (RICE, MoSCoW)

**Example**:
```bash
/product-advisor How does the payment flow work?
/product-advisor Brainstorm ideas for improving onboarding
/product-advisor Define requirements for a notification system
```

---

#### `/product-document <topic>`

**Purpose**: Create business-focused documentation for non-technical audiences.

**What it does**:
- Writes documentation for **product people, not developers**
- Explains what the product does and why it matters (no code or technical jargon)
- Maintains `docs/documentation.md` as the single source of truth
- Translates technical features into business value and user benefits

**Audience**: Product managers, stakeholders, executives, business analysts.

**Example**:
```bash
/product-document the entire project
/product-document the login experience
/product-document the payment system
```

---

## Agents

Agents are specialized AI assistants that can be invoked automatically or manually. Each has a specific focus and set of tools.

### Research & Planning

#### Project Researcher

**Purpose**: Analyze codebase patterns and research solutions before implementation.

**When used**: Automatically by `/project-search`.

**What it produces**: `initial-search.md` containing:
- Project patterns found in the codebase
- Relevant files and their purposes
- Internet research findings
- Recommended approach with justification

---

#### Spec Architect

**Purpose**: Transform research into actionable implementation specifications.

**When used**: Automatically by `/spec`.

**What it produces**: `spec.md` containing:
- Executive summary
- Files to create/modify with exact paths
- Classes and methods with signatures
- Performance and scalability considerations
- Implementation order and phases
- Testing strategy

---

### Implementation

#### Implementer

**Purpose**: Execute implementation specifications with precision.

**When used**: Automatically by `/implement`.

**Behavior**:
- Follows specs exactly—no extra features or "improvements"
- Creates `questions.md` if anything is unclear
- Only proceeds when specs are unambiguous

---

### Review Specialists

#### Performance Reviewer

**Purpose**: Deep performance analysis.

**Focus areas**:
- Algorithm complexity (time and space)
- Database query optimization
- Caching opportunities
- Resource usage (CPU, memory, I/O)
- Concurrency and scalability

**Output**: `performance-review.md`

---

#### Security Reviewer

**Purpose**: Security vulnerability detection.

**Focus areas**:
- OWASP Top 10 vulnerabilities
- Injection attacks (SQL, XSS, command)
- Authentication and authorization flaws
- Secrets management
- Cryptographic practices

**Output**: `security-review.md`

---

#### Quality Reviewer

**Purpose**: Code quality and maintainability analysis.

**Focus areas**:
- Code smells and complexity
- SOLID principles adherence
- Test coverage and quality
- Architecture patterns
- Production readiness

**Output**: `quality-review.md`

---

#### Overall Reviewer

**Purpose**: Synthesize all specialist reviews into a deployment decision.

**When used**: After performance, security, and quality reviews complete.

**What it produces**: `overall-review.md` containing:
- Executive summary with deployment decision
- Prioritized findings from all reviews
- Action items by timeframe
- Risk assessment

---

### Product Management

#### Product Advisor

**Purpose**: Product strategy and feature guidance.

**Capabilities**:
- Answer product questions based on codebase analysis
- Brainstorm features with pros/cons evaluation
- Create user stories and acceptance criteria
- Apply prioritization frameworks

---

#### Product Documenter

**Purpose**: Create business-focused documentation for non-technical audiences.

**Audience**: Product managers, stakeholders, executives—anyone who thinks about the product, not the code.

**Capabilities**:
- Translate technical features into plain language
- Explain what the product does and why it matters
- Focus on user value and business outcomes
- Maintain `docs/documentation.md` as the single source of truth

---

## Typical Workflows

### New Feature Development

```bash
# 1. Research patterns and best practices
/project-search Implement rate limiting for API endpoints

# 2. Create detailed specification
/spec

# 3. Implement the feature
/implement

# 4. Run comprehensive review
/review

# 5. Create semantic commits
/semantic-commit
```

### Before a Pull Request

```bash
# Quick comprehensive review
/review

# Or individual reviews
/security-review
/performance-review
/quality-review
```

### Planning Test Coverage

```bash
/think-on-tests src/services/PaymentService.ts
```

### Understanding the Codebase

```bash
/product-advisor How does the authentication flow work?
/deep-search Best practices for JWT refresh tokens
```

### Creating Documentation

```bash
/product-document the entire project
/product-document authentication module
```

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.

---

## License

This project is open source. See the repository for license details.
