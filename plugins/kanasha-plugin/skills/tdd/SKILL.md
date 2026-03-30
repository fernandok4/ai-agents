---
name: tdd
description: TDD development workflow orchestrator. Runs software-architect → user approval → tech-team-architect plans TDD team → qa-engineer writes failing tests → backend-developer makes them pass → parallel code review → inline consolidation → fixes HIGH/CRITICAL. Use when starting a new feature with test-driven development.
user-invocable: true
argument-hint: "<feature description>"
---

Orchestrates a full TDD development lifecycle from feature description to reviewed, production-ready code.

## Usage

```
/tdd <feature description>
```

**Example**:
```
/tdd Add a payment processing endpoint that charges a stored card and emits a payment.completed event
```

## Workflow

Execute the phases in strict order. Do not skip phases. Do not proceed to the next phase if the current one fails.

---

### Phase 1 — Architecture: Generate Specification

Launch the `software-architect` agent to analyze the feature description and produce `spec.md`.

**Agent**: `software-architect`
**Input**: The user's feature description (the argument passed to `/tdd`)
**Output**: `spec.md` in the current directory
**Run**: Foreground (wait for completion)

After the agent completes, tell the user:

```
spec.md has been generated. Please review it carefully before the team is assembled.

Key questions to consider:
- Are all requirements captured correctly?
- Are the implementation phases in the right order?
- Are there any NEEDS CLARIFICATION items that need your input?

Reply with:
- "approved" to proceed
- Feedback to request changes (the software-architect will revise)
```

Wait for the user's response.

- If the user says **"approved"** (or equivalent) → proceed to Phase 2
- If the user provides **feedback** → re-launch `software-architect` with the feedback appended to the original request, then present the revised `spec.md` for approval again
- Repeat until explicit approval is received

---

### Phase 2 — Team Planning: Design the TDD Team

Launch the `tech-team-architect` agent to read `spec.md` and produce `team-plan.md`.

**Agent**: `tech-team-architect`
**Input prompt**: "Read `spec.md` and design a team to deliver this feature using TDD (Test-Driven Development). Define the team composition, execution order, responsibilities, and deliverables for each member. Write the result to `team-plan.md`."
**Output**: `team-plan.md`
**Run**: Foreground (wait for completion)

After the agent completes, read `team-plan.md` in full. This file is now the authoritative source for all remaining phases.

Present the team plan to the user:

```
Team assembled for TDD delivery. Here's the plan:

[Display the team members and execution order from team-plan.md]

Proceeding with the team plan.
```

No approval is needed for the team plan. Proceed immediately.

---

### Phase 3 — TDD Red Phase: Write Failing Tests

Launch the `qa-engineer` agent to write failing test code based on `spec.md`.

**Agent**: `qa-engineer`
**Input prompt**: "Read `spec.md` and write failing test code (red phase of TDD). Write actual executable test files — not just specifications or lists. Each test should fail because the production code doesn't exist yet. Create minimal stubs (throwing `NotImplementedError` or equivalent) for any production classes referenced in tests. Follow the project's existing test patterns and conventions. Organize tests by category: happy path, validation, business rules, edge cases, security, multi-tenancy."
**Output**: Test files in the project's test directory
**Run**: Foreground (wait for completion)

After the agent completes, verify the tests exist and report to the user:

```
Red phase complete. [N] test files created.
All tests should be failing (red). Proceeding to green phase.
```

---

### Phase 4 — TDD Green Phase: Make Tests Pass

Launch the `backend-developer` agent to implement production code that makes the failing tests pass.

**Agent**: `backend-developer`
**Input prompt**: "Failing TDD tests have been written. Read `spec.md` for context. Implement the minimum production code needed to make ALL failing tests pass (green phase). Follow the red-green-refactor cycle: make each test pass, then refactor if needed. Do NOT modify the test files. Run tests after implementation to verify they pass."
**Output**: Production code files
**Run**: Foreground (wait for completion)

**Additional agents**: If `team-plan.md` specifies extra agents for this phase (e.g., `database-specialist` for migrations), launch them before or alongside `backend-developer` as indicated by the team plan.

After the agent completes:
- If all tests pass → proceed to Phase 5
- If some tests still fail → present the failures to the user and ask how to proceed (retry, adjust spec, or skip)

---

### Phase 5 — Code Review: Run Specialist Reviewers

Launch all 3 specialist reviewers in parallel:

- **quality-reviewer**: `Review the changes for code quality. Discover the project's existing patterns first. Write findings to quality-review.md.`
- **security-reviewer**: `Review the changes for security vulnerabilities following OWASP Top 10. Write findings to security-review.md.`
- **performance-reviewer**: `Review the changes for performance issues. Write findings to performance-review.md.`

**Run**: All 3 in parallel (background). Wait for all to complete.

---

### Phase 6 — Consolidation: Inline Review Verdict

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

### Phase 7 — Fix Phase (if HIGH/CRITICAL exist)

If the verdict is CONDITIONAL GO or NO-GO:

Launch the `backend-developer` agent to fix all HIGH and CRITICAL findings.

**Agent**: `backend-developer`
**Input prompt**: "Read quality-review.md, security-review.md, and performance-review.md. Fix every HIGH and CRITICAL finding. Do not fix MEDIUM or LOW findings. HIGH and CRITICAL fixes are mandatory — no exceptions."
**Run**: Foreground (wait for completion)

After fixes, re-run Phase 5 (all 3 reviewers in parallel) and Phase 6 (inline consolidation).

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
| `software-architect` fails to produce `spec.md` | Report the error to the user. Do not proceed |
| User rejects spec more than 3 times | Ask the user if they want to provide a more detailed description or a manual spec |
| `tech-team-architect` fails to produce `team-plan.md` | Report the error. Ask the user: retry, or proceed with the default team (qa-engineer → backend-developer → 3 reviewers). Never silently fall back — the user decides |
| `qa-engineer` fails to write test code | Report error. Green phase cannot start without failing tests |
| `backend-developer` reports still-failing tests | Present the specific failing tests to the user. Ask: retry, skip, or adjust spec |
| A reviewer fails to produce its output file | Note the missing review, consolidate with what's available, flag the gap |
| Phase 7 exceeds 2 iterations | Present remaining HIGH/CRITICAL issues to the user with options: fix manually, accept risk, update spec |

## Important Notes

- **Spec approval is mandatory** — never skip it. The spec is the contract for the entire team
- **`team-plan.md` guides execution** — follow the team architect's recommended order and roles. If extra agents were added, launch them at the specified position
- **Tests must be red before implementation starts** — if qa-engineer reports tests that already pass, flag this to the user
- **HIGH and CRITICAL are always fixed** — there are no exceptions in the fix phase
- **MEDIUM and LOW are never auto-fixed** — they are reported to the user as optional improvements
- **Review consolidation is inline** — no separate overall-reviewer agent. The skill reads the 3 review files and presents the verdict directly
