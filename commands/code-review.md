# Code Review Command

Performs comprehensive code review for quality, architecture, testing, and production readiness. For focused analysis, use `/security-review` or `/performance-review`.

## Objective

Conduct practical code analysis covering code quality, maintainability, architecture, testing, and production readiness through natural language interaction.

## Usage

**Pattern**: `/code-review [what to review]`

**Examples**:
- `/code-review` → reviews uncommitted changes
- `/code-review my branch` → current branch vs main
- `/code-review src/api/users.ts` → specific file
- `/code-review is this production ready?` → readiness assessment
- `/code-review the UserService class` → specific class

## Instructions

### 1. Target Identification

**Parse the request to identify what to review**:

- **"my changes"/"current changes"** → `git diff` (uncommitted)
- **"my branch"/"this branch"** → current branch vs main/master
- **File paths** (e.g., "src/auth/login.ts") → specific files
- **Method/class names** → use Grep/Glob to locate
- **"this"/"that"** → check conversation history
- **Nothing specified** → default to uncommitted changes

**If ambiguous**: Ask for clarification with specific options.

### 2. Context Gathering

Automatically gather context:
- Read target files
- Check related test files
- Review recent commits if relevant
- Identify programming language
- Understand project structure

### 3. Analysis Layers

#### Code Quality & Maintainability

**Readability**:
- Clear, descriptive naming
- Appropriate comments (where logic isn't self-evident)
- Consistent formatting
- Logical organization

**Structure**:
- Proper modularization
- Single Responsibility Principle
- Appropriate abstraction levels
- No over-engineering

**Code Smells**:
- Duplicate code
- Magic numbers
- God classes (> 500 lines or > 20 methods)
- Excessive complexity

**Complexity**:
- Calculate cyclomatic complexity (flag if > 15)
- Check for excessive nesting
- Identify overly complex methods

#### Architecture & Design

**Pattern Adherence**:
- Follows project conventions
- Consistent with existing architecture
- SOLID principles respected
- Appropriate design patterns

**Technical Debt**:
- New debt introduced?
- Existing debt addressed?
- Workarounds or hacks?
- Code duplication?

**API Design** (if applicable):
- RESTful principles
- Proper HTTP methods/status codes
- Versioning strategy
- Backward compatibility

#### Testing & Coverage

**Test Presence**:
- Unit tests present?
- Edge cases covered?
- Error conditions tested?
- Integration tests for APIs?

**Coverage Goals**:
- Minimum 80% for new code
- Critical paths at 100%
- Tests are meaningful, not just coverage padding

#### Production Readiness

**Error Handling**:
- Proper exception handling
- No silent failures
- User-friendly error messages
- Errors logged appropriately

**Observability**:
- Structured logging at appropriate levels
- Key metrics instrumented (latency, errors, throughput)
- Request correlation IDs
- Health check endpoints

**Reliability**:
- Fault tolerance mechanisms
- Circuit breakers for external services
- Retry logic with exponential backoff
- Graceful degradation

**Deployment Considerations**:
- Breaking changes identified
- Database migrations needed?
- Feature flags for risky changes?
- Rollback capability
- Environment variables documented

**Scalability**:
- Handles expected load
- Resource usage efficient
- No single point of failure
- Horizontal scaling possible

### 4. Quality Gates

**BLOCKING (Must Fix)**:
- Critical bugs
- Syntax errors
- All tests must pass
- Code coverage ≥ 80% on new code

**WARNINGS (Should Fix)**:
- Cyclomatic complexity ≥ 15
- Code smells introduced
- Missing error handling
- Inadequate logging

### 5. Report Generation

Generate structured report:

```markdown
# Code Review Report

**Target**: [what was reviewed]
**Status**: 🟢 READY | 🟡 REVIEW NEEDED | 🔴 NOT READY

## Executive Summary

[2-3 sentence overview of code quality and readiness]

**Production Ready**: [Yes/No with reasoning]

---

## Analysis Results

### ✅ Passed (X)
- [Checks that passed]

### ⚠️ Warnings (X)
- [Non-blocking issues with file:line references]

### ❌ Critical Issues (X)
- [Blocking issues with file:line and severity]

---

## Code Quality

**Readability**: [Assessment]
**Structure**: [Assessment]
**Complexity**: [Metrics and concerns]

**Score**: X/10

---

## Architecture & Design

**Pattern Adherence**: [How well it follows project patterns]
**Technical Debt**: [New debt introduced or addressed]

**Score**: X/10

---

## Testing & Coverage

- Lines covered: X%
- New code coverage: X%
- Edge cases: [Assessment]

**Score**: X/10

---

## Production Readiness

**Error Handling**: [Assessment]
**Observability**: [Logging, metrics, tracing]
**Reliability**: [Fault tolerance, graceful degradation]
**Scalability**: [Load handling capability]
**Deployment Risk**: [Breaking changes, migrations]

**Score**: X/10

---

## Metrics Summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Lines Changed | X | < 400 | ✅/⚠️/❌ |
| Cyclomatic Complexity | X | < 15 | ✅/⚠️/❌ |
| Code Coverage | X% | ≥ 80% | ✅/⚠️/❌ |
| Code Smells | X | 0 new | ✅/⚠️/❌ |

---

## Prioritized Recommendations

### Must Fix (Blocking)
1. [Critical fixes with file:line references]

### Should Fix (High Priority)
2. [Important improvements]

### Consider (Enhancement)
3. [Optional optimizations]

---

## Detailed Findings

### File: [filename]

**[CRITICAL/WARNING/INFO]** Line X: [Issue]
- **Problem**: [What's wrong]
- **Impact**: [Why it matters]
- **Fix**: [How to resolve]

---

## Deployment Decision

**Recommendation**: [APPROVE | APPROVE WITH CONDITIONS | REJECT]

**Reasoning**: [Clear explanation]

**Required Actions**:
1. [Must-do items if conditional]
```

### 6. Conversational Delivery

**Answer questions directly first**:
```
User: "is this production ready?"
Response: "❌ Not yet - 2 blocking issues:
1. CRITICAL: Missing error handling in payment.ts:45
2. CRITICAL: No tests for new UserService methods

[Then provide full analysis...]"
```

**Offer follow-up**:
- "Would you like me to dive deeper into any area?"
- "Should I focus on the error handling issues?"
- "Need help with test implementation?"

## Anti-Patterns to Flag

**Process**:
- Oversized changes (> 400 lines, suggest splitting)
- Missing tests for new functionality
- No documentation for public APIs

**Code**:
- God classes (> 500 lines or > 20 methods)
- Magic numbers without constants
- Dead/commented code (lava flow)
- High cyclomatic complexity (> 15)

## Principles

1. **Natural Language**: Understand plain language, no rigid syntax
2. **Context-Aware**: Infer intent from conversation
3. **Actionable**: Every issue needs clear fix suggestion
4. **Prioritized**: Critical before nice-to-haves
5. **Objective**: Measurable criteria, not subjective
6. **Educational**: Explain WHY, not just WHAT
7. **Clarify When Needed**: Ask instead of assuming

## Special Considerations

**AI-Generated Code**:
- Extra scrutiny for edge cases
- Verify it solves the actual problem
- Check for over-engineering

**Legacy Code**:
- Don't require refactoring entire system
- Focus on new changes and immediate impact
- Suggest improvements but don't block on legacy debt

**Critical Paths** (always recommend manual review):
- Authentication/authorization
- Payment processing
- Cryptographic operations
- Database migrations

## Notes

- This is AI-assisted review, not replacement for human review
- Some "issues" may be intentional design decisions
- For critical code paths, always require manual security review
- Tool helps catch issues but cannot guarantee bug-free code
