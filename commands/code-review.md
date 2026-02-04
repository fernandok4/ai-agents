# Code Review Command

Performs comprehensive production-ready code review following 2026 industry best practices for security, performance, quality, and production readiness. Understands natural language instructions for flexible, conversational code review.

## Objective

Conduct multi-layered code analysis that goes beyond syntax checking to evaluate code for production deployment, covering security vulnerabilities, performance issues, architectural concerns, and operational readiness. The command intelligently interprets natural language to understand what to review and what to focus on.

## Natural Language Understanding

This command interprets conversational requests. **No parameters or flags needed** - just describe what you want in plain language.

### How to Interact

Simply tell the command what you want to review and optionally what to focus on:

**Pattern**: `/code-review [what to review] [optional: focus area]`

**What to review**:
- "my changes" / "current changes" → uncommitted changes
- "my branch" / "this branch" → current branch vs main
- "feature/xyz branch" → specific branch
- "src/auth/login.ts" → specific file(s)
- "the login method" → specific method/function
- "UserService class" → specific class
- "authentication code" → search for auth-related code
- "payment processing" → search for payment-related code

**Focus areas** (optional):
- "for security" / "security issues" / "vulnerabilities"
- "for performance" / "optimization" / "bottlenecks"
- "production ready" / "ready to deploy" / "ready for release"
- "code quality" / "maintainability" / "clean code"
- "quick" / "brief" / "summary" → fast scan

### Conversational Examples

**Simple & Direct**:
- "review the login method"
- "check this file for security issues"
- "is my code production ready?"
- "review my current branch"

**Specific & Focused**:
- "is the UserService class production ready?"
- "check for performance issues in the API endpoints"
- "review the authentication code for security vulnerabilities"
- "are there any SQL injection risks in the data layer?"

**Questions & Natural Phrasing**:
- "can I deploy this to production?"
- "are there any blocking issues in my changes?"
- "what security problems exist in the payment code?"
- "is the database query optimized?"
- "should I refactor this method?"

**Contextual & Smart**:
- "review this" → (looks at code in conversation history)
- "check the class we just discussed"
- "review those changes" → (references previous context)
- "what about the performance?" → (continues previous review)

## Instructions

When the user invokes this command:

### 1. **Intelligent Target Identification & Context Gathering**

**Parse Natural Language Input**:

Analyze the user's request to identify:

**What to Review** (Target):
- **Keywords for current changes**: "current", "uncommitted", "my changes", "what I changed"
  → Review `git diff` (uncommitted changes)

- **Keywords for branches**: "branch", "feature", "my branch", "this branch", "compare"
  → Run `git branch --show-current` to get current branch, compare with main/master

- **File mentions**: Any path-like strings (e.g., "src/auth/login.ts", "UserService.java")
  → Review specified file(s)

- **Code element names**: Mentioned method/function/class names
  → Search codebase using Grep/Glob to locate and review

- **Keywords for commits**: "commits", "last commit", "recent changes", "commit range"
  → Use git log to identify relevant commits

- **Context clues**: "this", "that", "the code above"
  → Look at conversation history for referenced code

**Focus Area** (What to emphasize):
- **Security keywords**: "security", "vulnerabilities", "secure", "safe", "exploits", "OWASP", "injection", "XSS"
  → Prioritize security analysis, deep OWASP Top 10 scan

- **Performance keywords**: "performance", "slow", "optimize", "fast", "efficient", "scalability", "bottleneck"
  → Prioritize performance and complexity analysis

- **Production keywords**: "production ready", "deploy", "release", "production", "live", "prod"
  → Full production readiness assessment

- **Quality keywords**: "quality", "clean", "maintainable", "readable", "code smell"
  → Focus on code quality and maintainability

- **Testing keywords**: "tests", "coverage", "testing", "test cases"
  → Focus on testing adequacy and coverage

- **Quick keywords**: "quick", "fast", "brief", "summary", "critical only"
  → Quick scan for critical issues only

**Depth Level**:
- **Quick/Brief**: Critical security + blocking bugs only
- **Standard**: Comprehensive multi-layer analysis (default)
- **Deep/Thorough**: Extra scrutiny, include all recommendations

**Decision Strategy**:
1. If user mentions specific files/methods/classes → Search and locate them
2. If user mentions "branch" or "changes" → Check git status and current branch
3. If request is vague → Default to uncommitted changes or ask for clarification
4. If multiple interpretations → Ask user to clarify (use conversational tone)
5. If target not found → Search broader, then report findings or ask
6. If scope too large → Suggest reviewing in parts or ask to narrow

### 2. **Conversational Response Patterns**

**When Target is Clear**:
Proceed directly with analysis and provide comprehensive report.

**When Target is Ambiguous**:
```
User: "review the authentication code"

Response: "I found authentication-related code in several places:
1. src/auth/login.ts (157 lines) - User login functionality
2. src/auth/session.ts (89 lines) - Session management
3. src/middleware/auth.ts (45 lines) - Auth middleware
4. tests/auth/*.test.ts - Auth tests

Would you like me to:
A) Review all authentication code (291 lines total)
B) Focus on a specific file
C) Review just the core logic (login + session, skip middleware)"
```

**When Focus is Unclear**:
Provide comprehensive review by default, but offer to dive deeper:
```
"I've completed a comprehensive review. The code is generally well-structured with
a few security concerns. Would you like me to:
- Dive deeper into the security findings
- Analyze performance implications
- Check production readiness
- Focus on any specific area?"
```

**When Answering Questions**:
Answer the question directly first, then provide supporting analysis:
```
User: "is this production ready?"

Response: "❌ Not yet - there are 2 blocking issues:

1. CRITICAL: Hardcoded API key in config.ts:23
2. CRITICAL: Missing error handling in payment processing

After fixing these, you'll also want to address:
- 3 performance optimizations recommended
- Test coverage at 65% (target: 80%)
- Missing health check endpoint

[Detailed analysis follows...]"
```

**Intelligent Context Gathering**:

Based on identified target, automatically:
- Read all changed/target files
- Identify programming language(s)
- Check for related test files
- Review recent commit messages for patterns
- Understand project structure and conventions
- Search for referenced methods/classes if mentioned by name
- Check git status if branch/changes mentioned
- Look at conversation history for previously discussed code

### 3. **Multi-Layered Analysis**

Perform comprehensive analysis across these dimensions:

#### Layer 1: Automated Static Analysis

**Linting & Syntax**:
- Check for syntax errors
- Verify code style consistency
- Identify unused imports/variables
- Check for proper formatting

**Complexity Metrics**:
- Calculate cyclomatic complexity (flag if > 15)
- Identify overly complex methods
- Check for excessive nesting
- Measure cognitive complexity

**Code Smells**:
- Detect duplicate code
- Identify magic numbers
- Find god classes/methods
- Spot spaghetti code patterns

#### Layer 2: Security Analysis (CRITICAL)

**OWASP Top 10 Coverage**:
- ✓ SQL Injection: Check for unsanitized database queries
- ✓ XSS: Look for unescaped user input in HTML/templates
- ✓ Broken Authentication: Review auth implementation, session management
- ✓ Sensitive Data Exposure: Find hardcoded secrets, API keys, passwords
- ✓ Security Misconfiguration: Check for insecure defaults
- ✓ Insecure Deserialization: Look for unsafe object deserialization
- ✓ Component Vulnerabilities: Note outdated dependencies
- ✓ Insufficient Logging: Verify error logging without exposing secrets

**Input Validation**:
- All user input properly validated?
- Type checking in place?
- Range/format validation?
- Command injection vulnerabilities?

**Authentication & Authorization**:
- No hardcoded credentials
- Proper password hashing (bcrypt, Argon2)
- Secure session management
- Access control properly implemented

**Cryptography**:
- No weak algorithms (MD5, SHA1 for security)
- Proper key management
- Secure random number generation
- HTTPS enforcement for sensitive data

**Secrets Management**:
- No secrets in code or comments
- Environment variables used correctly
- No API keys hardcoded
- No database credentials exposed

**Error Handling**:
- No sensitive info in error messages
- Proper exception handling
- No silent failures
- Logs don't expose sensitive data

**Special Scrutiny for**:
- Authentication/authorization code
- Payment processing
- Sensitive data handling
- External API calls with untrusted input

### 4. **Performance Analysis (Layer 3)**

**Algorithm Complexity**:
- Identify time complexity (O(1), O(n), O(n²), etc.)
- Flag O(n²) or worse in loops
- Check for unnecessary nested iterations
- Suggest optimization opportunities

**Resource Usage**:
- CPU: Unnecessary computations, tight loops
- Memory: Inefficient data structures, memory leaks
- I/O: Excessive disk/network operations
- Database: N+1 queries, missing indexes, inefficient joins

**Caching**:
- Identify cacheable operations
- Check cache invalidation logic
- Verify TTL appropriateness
- Ensure caching at right layer

**Database Queries**:
- Check for N+1 query problems
- Verify indexes on queried columns
- Look for SELECT * anti-pattern
- Check for proper pagination

#### Layer 4: Code Quality & Maintainability

**Readability**:
- Clear, descriptive naming
- Appropriate comments (where logic isn't self-evident)
- Consistent formatting
- Logical code organization

**Structure**:
- Proper modularization
- Single Responsibility Principle
- Appropriate abstraction levels
- No over-engineering

**Testing**:
- Unit tests present?
- Test coverage adequate (80%+ for new code)?
- Edge cases covered?
- Error conditions tested?
- Integration tests for APIs?

**Dependencies**:
- Up-to-date libraries
- No deprecated APIs
- License compliance
- Minimal dependency footprint

#### Layer 5: Architecture & Design

**Pattern Adherence**:
- Follows project conventions?
- Consistent with existing architecture?
- SOLID principles respected?
- Appropriate design patterns used?

**Technical Debt**:
- New debt introduced?
- Existing debt addressed?
- Workarounds or hacks present?
- Code duplication?

**API Design** (if applicable):
- RESTful principles followed?
- Proper HTTP methods/status codes?
- Versioning strategy?
- Backward compatibility?

#### Layer 6: Production Readiness

**Scalability**:
- Handles expected load?
- Horizontal scaling possible?
- No single point of failure?
- Resource usage efficient?

**Reliability**:
- Proper error handling?
- Fault tolerance mechanisms?
- Circuit breakers for external services?
- Retry logic with exponential backoff?
- Graceful degradation?

**Observability**:
- **Logging**: Structured logs at appropriate levels?
- **Metrics**: Key metrics instrumented (latency, errors, throughput)?
- **Tracing**: Request correlation IDs?
- **Health Checks**: Endpoints implemented?
- **Alerting**: Critical conditions covered?

**Deployment**:
- Breaking changes identified?
- Database migrations needed?
- Feature flags for risky changes?
- Rollback plan possible?
- Environment variables documented?

**Documentation**:
- API endpoints documented?
- Complex logic explained?
- Configuration parameters listed?
- Dependencies documented?

### 4. **Quality Gates Validation**

Check against production readiness thresholds:

**Required (BLOCKING)**:
- [ ] Zero high/critical security vulnerabilities
- [ ] Zero hardcoded secrets
- [ ] All tests passing
- [ ] No syntax errors
- [ ] Code coverage ≥ 80% on new code

**Recommended (WARNINGS)**:
- [ ] Cyclomatic complexity < 15 per method
- [ ] No code smells introduced
- [ ] No deprecated dependencies
- [ ] Proper error handling in place
- [ ] Observability implemented (logging/metrics)

### 5. **Generate Review Report**

Create structured output:

```markdown
# Code Review Report

**Date**: [timestamp]
**Target**: [branch/files/method reviewed]
**Reviewer**: Claude Code (Automated Review)
**Status**: 🟢 READY | 🟡 NEEDS REVIEW | 🔴 NOT READY

---

## Executive Summary

**Overall Score**: [X/10]

[2-3 sentence summary of code quality and production readiness]

**Production Readiness**: [Assessment of whether code is ready for deployment]

---

## 📊 Analysis Results

### ✅ Passed Checks (X)
- [List all checks that passed]

### ⚠️  Warnings (X)
- [List issues that should be addressed but don't block deployment]
- Include file:line references

### ❌ Critical Issues (X)
- [List blocking issues that MUST be fixed before deployment]
- Include file:line references and severity

---

## 🔒 Security Analysis

### Vulnerabilities Found
[List any security issues organized by OWASP category]

### Security Best Practices
[Note any security concerns or recommendations]

**Security Score**: [X/10]

---

## ⚡ Performance Analysis

### Algorithm Complexity
[Time/space complexity analysis of key functions]

### Resource Optimization
[Database queries, caching, memory usage]

### Performance Recommendations
[Specific optimization suggestions]

**Performance Score**: [X/10]

---

## 🏗️ Architecture & Design

### Pattern Adherence
[How well code follows project patterns]

### Design Quality
[SOLID principles, modularity, abstraction]

### Technical Debt
[New debt introduced or addressed]

**Architecture Score**: [X/10]

---

## 🧪 Testing & Coverage

### Test Coverage
- Lines covered: X%
- Branches covered: X%
- New code coverage: X%

### Test Quality
[Assessment of test completeness and edge case coverage]

**Testing Score**: [X/10]

---

## 🚀 Production Readiness

### Scalability
[Assessment of scaling capability]

### Reliability
[Error handling, fault tolerance]

### Observability
[Logging, metrics, tracing, alerting]

### Deployment Risk
[Breaking changes, migration needs, rollback capability]

**Production Readiness Score**: [X/10]

---

## 📈 Metrics Summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Lines Changed | X | < 400 | ✅/⚠️/❌ |
| Cyclomatic Complexity | X | < 15 | ✅/⚠️/❌ |
| Code Coverage | X% | ≥ 80% | ✅/⚠️/❌ |
| Security Vulnerabilities | X | 0 | ✅/⚠️/❌ |
| Code Smells | X | 0 new | ✅/⚠️/❌ |

---

## 💡 Prioritized Recommendations

### Must Fix (Blocking)
1. [Highest priority fixes with file:line references]

### Should Fix (High Priority)
1. [Important improvements]

### Consider (Enhancement)
1. [Optional optimizations]

---

## 📝 Detailed Findings

### File: [filename]

#### Issues
- **[CRITICAL/WARNING/INFO]** Line X: [Issue description]
  - **Problem**: [What's wrong]
  - **Impact**: [Why it matters]
  - **Fix**: [How to resolve]

[Repeat for each file]

---

## 🎯 Production Deployment Decision

**Recommendation**: [APPROVE | APPROVE WITH CONDITIONS | REJECT]

**Reasoning**: [Clear explanation of decision]

**Required Actions Before Deployment**:
1. [List of must-do items if conditional approval]

---

## 📚 References

- [Link to specific coding standards]
- [Link to security guidelines]
- [Link to architecture documentation]
```

### 6. **Conversational Clarification**

When request is ambiguous:
- Ask clarifying questions in natural language
- Offer suggestions: "Did you mean X or Y?"
- Request context on design decisions if needed
- Verify assumptions about requirements
- Discuss trade-offs when multiple approaches exist

**Example**:
User: "review the auth code"
Response: "I found authentication code in 3 places:
1. `src/auth/login.ts` - Login handler
2. `src/auth/session.ts` - Session management
3. `src/middleware/auth.ts` - Auth middleware

Which would you like me to review, or should I review all authentication-related code?"

### 7. **Intelligent Focus Detection**

Automatically adjust analysis depth based on request:

**Security-Focused** (keywords: security, vulnerabilities, safe, secure):
- Deep OWASP Top 10 analysis
- Secrets scanning
- Authentication/authorization scrutiny
- Input validation review

**Performance-Focused** (keywords: performance, slow, optimize, fast):
- Algorithm complexity analysis
- Database query optimization
- Caching strategy review
- Resource usage patterns

**Production Readiness** (keywords: production, deploy, release, ready):
- Full scalability assessment
- Reliability checks
- Observability requirements
- Deployment risk analysis

**Quick Scan** (keywords: quick, brief, summary, critical):
- Critical security issues only
- Blocking bugs
- Must-fix items before deploy

**Comprehensive** (default or keywords: thorough, deep, complete, full):
- All layers of analysis
- All recommendations
- Detailed findings

### 8. **Adaptive Output Format**

Automatically choose appropriate format based on request:

**Brief/Summary**: When user asks for "quick", "summary", "brief"
- Executive summary only
- Top 3-5 critical issues
- Production ready yes/no

**Detailed**: Default for thorough reviews
- Full multi-section report
- All findings with context
- Prioritized recommendations

**Checklist**: When user asks "is this ready?", "can I deploy?"
- Production readiness checklist
- Pass/fail for each criterion
- Action items for failures

**Conversational**: When user asks questions
- Direct answers to specific questions
- Focused on requested aspect
- Interactive discussion format

## Anti-Patterns to Detect

Flag these common issues:

**Process Anti-Patterns**:
- Oversized changes (> 400 lines should suggest splitting)
- Missing tests for new functionality
- No documentation for public APIs

**Code Anti-Patterns**:
- God classes (> 500 lines or > 20 methods)
- Magic numbers without constants
- Lava flow (dead/commented code)
- Cargo cult programming (patterns without understanding)
- Spaghetti code (high cyclomatic complexity)

## Principles

1. **Natural & Conversational**: Understand plain language, no rigid syntax required
2. **Context-Aware Intelligence**: Infer intent from conversation and codebase context
3. **Security First**: Security issues are always critical and blocking
4. **Production Readiness**: Code must be operationally sound, not just functionally correct
5. **Adaptive Analysis**: Adjust depth and focus based on user needs
6. **Actionable Feedback**: Every issue must have clear fix suggestion with examples
7. **Prioritized**: Critical issues before nice-to-haves, ranked by impact
8. **Objective**: Use measurable criteria, not subjective preferences
9. **Respectful**: Assume positive intent, focus on code not coder
10. **Educational**: Explain WHY something is an issue, not just WHAT
11. **Clarify When Needed**: Ask questions instead of making wrong assumptions
12. **Continuous Dialogue**: Support follow-up questions and iterative refinement

## Special Considerations

**AI-Generated Code**:
- Extra scrutiny for security and edge cases
- Verify the code actually solves the problem
- Check for over-engineering or unnecessary complexity

**Legacy Code Modifications**:
- Don't require refactoring entire legacy system
- Focus on new changes and their immediate impact
- Suggest improvements but don't block on legacy debt

**Critical Code Paths**:
- Authentication/authorization: ALWAYS require manual review
- Payment processing: ALWAYS require manual review
- Cryptographic operations: ALWAYS require security expert review
- Database migrations: ALWAYS verify rollback capability

## Usage Examples

All examples use natural language - just describe what you want to review:

### General Reviews

```
/code-review
→ Reviews uncommitted changes (git diff)

/code-review check my current changes
→ Reviews uncommitted changes

/code-review review my branch
→ Compares current branch with main/master

/code-review review the changes in feature/new-auth branch
→ Reviews specific branch vs main
```

### File-Specific Reviews

```
/code-review check src/auth/login.ts
→ Reviews specific file

/code-review review the authentication files
→ Searches for and reviews auth-related files

/code-review look at UserService.java and OrderService.java
→ Reviews multiple files
```

### Code Element Reviews

```
/code-review review the authenticateUser method
→ Finds and reviews specific method

/code-review check the UserAuthenticationService class
→ Finds and reviews specific class

/code-review review the login function for security issues
→ Reviews method with security focus
```

### Security-Focused Reviews

```
/code-review check for security vulnerabilities
→ Deep security scan of current changes

/code-review is the payment processing code secure?
→ Security review of payment-related code

/code-review scan for SQL injection vulnerabilities
→ Focused security scan

/code-review check if there are any hardcoded secrets
→ Secrets detection scan

/code-review review authentication code for OWASP issues
→ OWASP-focused security review
```

### Performance-Focused Reviews

```
/code-review check for performance issues
→ Performance analysis of current changes

/code-review is the getUserData method optimized?
→ Performance review of specific method

/code-review review database queries for performance
→ Database optimization review

/code-review check if there are any N+1 query problems
→ Focused performance scan
```

### Production Readiness

```
/code-review is this production ready?
→ Full production readiness assessment

/code-review can I deploy this to production?
→ Production readiness checklist

/code-review check if my branch is ready for release
→ Release readiness review

/code-review review for deployment risks
→ Deployment risk assessment
```

### Quick Scans

```
/code-review quick check
→ Critical issues only (fast scan)

/code-review any blocking issues?
→ Critical bugs and security issues

/code-review brief summary of code quality
→ Executive summary only
```

### Combined Requests

```
/code-review check the API endpoints for security and performance issues
→ Multi-focus review

/code-review review UserController.java for production readiness
→ Specific file, production focus

/code-review is the authentication service secure and performant?
→ Multi-aspect analysis

/code-review quick security scan of payment processing
→ Fast security-focused review
```

### Conversational Follow-ups

```
User: /code-review check my changes
Claude: [provides review]
User: what about security specifically?
→ Provides detailed security analysis

User: /code-review review the login code
Claude: "I found 3 login-related files. Which should I review?"
User: all of them
→ Reviews all authentication files
```

## Natural Language Processing Strategy

When parsing user requests:

1. **Extract Keywords**: Identify key terms (security, performance, method names, file paths)
2. **Determine Intent**: What does the user want? (review, check, scan, assess)
3. **Identify Target**: What to review? (files, methods, branches, changes)
4. **Detect Focus**: What to emphasize? (security, performance, production, quality)
5. **Assess Urgency**: How thorough? (quick, standard, deep)

**Execution Flow**:
```
User Request
    ↓
Parse Natural Language
    ↓
Identify: Target + Focus + Depth
    ↓
Gather Context (read files, git status, search code)
    ↓
Perform Analysis (adapt to focus area)
    ↓
Generate Report (adapt format to request type)
    ↓
Present Results (conversational or structured)
```

**Handling Ambiguity**:
- If target unclear → Check git status for changes, or ask user
- If multiple matches → Present options and ask which to review
- If focus unclear → Default to comprehensive review
- If request too broad → Suggest narrowing scope or offer to review in parts

## Integration with CI/CD

For automated environments, the command can still accept structured input:
- Environment variables: `CODE_REVIEW_TARGET`, `CODE_REVIEW_FOCUS`
- Config files: `.code-review.json` with review preferences
- Git hooks: Automatically review on pre-push

Exit codes:
- Exit code 0: All checks passed
- Exit code 1: Warnings present (non-blocking)
- Exit code 2: Critical issues found (blocking)

Output formats:
- Structured JSON for machine parsing
- Markdown for human-readable reports
- Checklist for quick pass/fail assessment

## Quality Thresholds

Based on 2026 industry standards:

- **Code Coverage**: ≥ 80% for new code
- **Cyclomatic Complexity**: < 15 per method
- **PR Size**: Warn if > 400 lines, suggest splitting
- **Security**: Zero tolerance for high/critical vulnerabilities
- **Performance**: Flag O(n²) or worse in production paths
- **Code Smells**: Zero new smells introduced

## Execution Flow

1. **Parse Natural Language Request**
   - Extract keywords and intent
   - Identify what to review (target)
   - Determine focus areas (security, performance, etc.)
   - Assess desired depth (quick, standard, comprehensive)

2. **Intelligent Target Resolution**
   - If file paths mentioned → Read those files
   - If method/class name → Use Grep to find it
   - If "branch" or "changes" → Check git status
   - If ambiguous → Check conversation history or ask for clarification
   - If nothing specified → Default to uncommitted changes

3. **Context Gathering**
   - Read all target files
   - Check related test files
   - Review git history if relevant
   - Understand project structure
   - Identify programming language(s)

4. **Adaptive Analysis** (adapt layers based on focus)
   - If security-focused → Deep OWASP scan, prioritize security layer
   - If performance-focused → Complex algorithms, database queries
   - If production-ready → Full scalability, reliability, observability
   - If quick scan → Critical issues only
   - Default → All layers comprehensively

5. **Aggregate Findings**
   - Calculate scores per dimension
   - Prioritize by severity (critical → warning → info)
   - Organize by file/component

6. **Generate Contextual Report**
   - Adapt format to request type
   - If question asked → Answer directly first
   - If quick scan → Brief summary only
   - If thorough → Full detailed report
   - Always include actionable recommendations

7. **Conversational Delivery**
   - Provide deployment recommendation
   - Offer to dive deeper into specific areas
   - Suggest next steps
   - Answer follow-up questions

## Notes

- **Human Review Required**: This is AI-assisted review, not replacement for human review
- **Context Matters**: Some "issues" may be intentional design decisions
- **Trust but Verify**: For critical code paths, always require manual security review
- **Continuous Improvement**: Learn from production incidents to improve review criteria
- **No False Security**: Tool helps catch issues but cannot guarantee bug-free code

## Success Metrics

Track effectiveness:
- Issue catch rate (bugs found in review vs production)
- False positive rate (issues flagged that aren't actually problems)
- Review time savings
- Production incident reduction
- Code quality trends over time
