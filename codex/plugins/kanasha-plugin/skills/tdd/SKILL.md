---
name: tdd
description: TDD development workflow orchestrator. Takes an approved plan/spec → qa-engineer writes failing tests → backend-developer makes them pass → parallel code review → inline consolidation → fixes HIGH/CRITICAL. Use when starting a new feature with test-driven development (plan the architecture first using Plan mode).
---

Orchestrates a TDD development lifecycle from an approved plan/spec to reviewed, production-ready code.

## Prerequisites

Before invoking `/tdd`, the architecture and design decisions must already be settled. Use Plan mode (or write a `spec.md` manually) to produce the plan that this skill will execute. This skill does **not** generate the spec — it executes against one that already exists.

## Usage

```
/tdd <feature description or path to spec.md>
```

**Examples**:
```
/tdd Add a payment processing endpoint that charges a stored card and emits a payment.completed event
/tdd ./spec.md
```

## Workflow

Execute the phases in strict order. Do not skip phases. Do not proceed to the next phase if the current one fails.

---

### Phase 1 — Confirm the Plan

Establish the plan that will drive the TDD cycle.

- If the argument is a path to an existing spec file (e.g., `./spec.md`), read it and summarize it to the user.
- If the argument is a feature description and no `spec.md` exists in the current directory, ask the user to either (a) provide a `spec.md`, or (b) run Plan mode first and return, or (c) confirm that the description itself is detailed enough to drive tests.
- If a `spec.md` already exists in the current directory, confirm with the user whether to use it.

Do not proceed until the plan is confirmed.

---

### Phase 2 — TDD Red Phase: Write Failing Tests

Launch the `qa-engineer` agent to write failing test code based on the confirmed plan.

**Agent**: `qa-engineer`
**Input prompt**: "Read the confirmed plan (spec.md or the feature description provided) and write failing test code (red phase of TDD). Write actual executable test files — not just specifications or lists. Each test should fail because the production code doesn't exist yet. Create minimal stubs (throwing `NotImplementedError` or equivalent) for any production classes referenced in tests. Follow the project's existing test patterns and conventions. Organize tests by category: happy path, validation, business rules, edge cases, security, multi-tenancy."
**Output**: Test files in the project's test directory
**Run**: Foreground (wait for completion)

After the agent completes, verify the tests exist and report to the user:

```
Red phase complete. [N] test files created.
All tests should be failing (red). Proceeding to green phase.
```

---

### Phase 3 — TDD Green Phase: Make Tests Pass

Launch the `backend-developer` agent to implement production code that makes the failing tests pass.

**Agent**: `backend-developer`
**Input prompt**: "Failing TDD tests have been written. Read the confirmed plan for context. Implement the minimum production code needed to make ALL failing tests pass (green phase). Follow the red-green-refactor cycle: make each test pass, then refactor if needed. Do NOT modify the test files. Run tests after implementation to verify they pass."
**Output**: Production code files
**Run**: Foreground (wait for completion)

**Additional agents**: If the plan calls for database work, launch `database-specialist` before or alongside `backend-developer` for migrations/schema. If the plan calls for frontend work, launch `frontend-developer` (from the frontend plugin) instead of or alongside `backend-developer`.

After the agent completes:
- If all tests pass → proceed to Phase 4
- If some tests still fail → present the failures to the user and ask how to proceed (retry, adjust plan, or skip)

---

### Phase 4 — Code Review: Run Specialist Reviewers

Launch all 3 specialist reviewers in parallel:

- **quality-reviewer**: `Review the changes for code quality. Discover the project's existing patterns first. Write findings to quality-review.md.`
- **security-reviewer**: `Review the changes for security vulnerabilities following OWASP Top 10. Write findings to security-review.md.`
- **performance-reviewer**: `Review the changes for performance issues. Write findings to performance-review.md.`

**Run**: All 3 in parallel (background). Wait for all to complete.

---

### Phase 5 — Consolidation: Inline Review Verdict

After all 3 reviewers finish, read `quality-review.md`, `security-review.md`, and `performance-review.md`.

Consolidate the findings inline. Count findings by severity:

```
Review complete.

Verdict: [GO | CONDITIONAL GO | NO-GO]

| Severity | Count |
|----------|-------|
| CRITICAL | N     |
| HIGH     | N     |
| MEDIUM   | N     |
| LOW      | N     |

[If CRITICAL or HIGH findings exist:]
The following HIGH/CRITICAL issues must be fixed:

1. [Source] [Severity]: [Description] — File: [path:line]
2. ...

[If only MEDIUM/LOW or no findings:]
No blocking issues found. Feature is ready.
```

**Verdict rules:**
- **GO**: No CRITICAL or HIGH findings
- **CONDITIONAL GO**: No CRITICAL, but HIGH findings exist
- **NO-GO**: Any CRITICAL finding exists

---

### Phase 6 — Fix Phase (if HIGH/CRITICAL exist)

If the verdict is CONDITIONAL GO or NO-GO:

Launch the `backend-developer` agent to fix all HIGH and CRITICAL findings.

**Agent**: `backend-developer`
**Input prompt**: "Read quality-review.md, security-review.md, and performance-review.md. Fix every HIGH and CRITICAL finding. Do not fix MEDIUM or LOW findings. HIGH and CRITICAL fixes are mandatory — no exceptions."
**Run**: Foreground (wait for completion)

After fixes, re-run Phase 4 (all 3 reviewers in parallel) and Phase 5 (inline consolidation).

- If no HIGH/CRITICAL remain → proceed to Completion Summary
- If issues persist → run fix phase again (max 2 iterations total)
- After 2 iterations with remaining issues → present to user and ask how to proceed

---

### Completion Summary

When all phases are done, present:

```
Feature complete.

Verdict: [final verdict]

Files created:
[List all files created during this workflow]

Files modified:
[List all files modified during this workflow]

Review findings resolved:
[Number of HIGH/CRITICAL findings fixed, if any]

Remaining findings (MEDIUM/LOW):
[List any MEDIUM or LOW findings — these are optional improvements]

Next steps:
- Run /semantic-commit to create commits for these changes
- Run /project-review to re-review any time
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| No plan/spec available at Phase 1 | Ask the user to run Plan mode first or supply a `spec.md`. Do not proceed |
| `qa-engineer` fails to write test code | Report error. Green phase cannot start without failing tests |
| `backend-developer` reports still-failing tests | Present the specific failing tests to the user. Ask: retry, skip, or adjust plan |
| A reviewer fails to produce its output file | Note the missing review, consolidate with what's available, flag the gap |
| Phase 6 exceeds 2 iterations | Present remaining HIGH/CRITICAL issues to the user with options: fix manually, accept risk, update plan |

## Important Notes

- **Architecture and team composition are upstream of this skill.** Use Plan mode (or write a `spec.md` manually) before invoking `/tdd`. This skill does not design the system — it executes the TDD cycle against an existing plan
- **Default execution team**: `qa-engineer` → `backend-developer` → three reviewers in parallel. Add `database-specialist` or `frontend-developer` only when the plan explicitly requires them
- **Tests must be red before implementation starts** — if qa-engineer reports tests that already pass, flag this to the user
- **HIGH and CRITICAL are always fixed** — there are no exceptions in the fix phase
- **MEDIUM and LOW are never auto-fixed** — they are reported to the user as optional improvements
- **Review consolidation is inline** — no separate overall-reviewer agent. The skill reads the 3 review files and presents the verdict directly
