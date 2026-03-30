# Review Orchestration Steps

Shared instructions for running the frontend specialist reviewers and consolidating findings.

## Step 1: Run the 4 specialist reviewers in parallel

Spawn all 4 at the same time using the Agent tool:

- **frontend-quality-reviewer** (`subagent_type: frontend-plugin:frontend-quality-reviewer`)
  Prompt: `Review $TARGET for code quality. Discover the project's existing patterns first. Write findings to quality-review.md.`

- **frontend-security-reviewer** (`subagent_type: frontend-plugin:frontend-security-reviewer`)
  Prompt: `Review $TARGET for client-side security vulnerabilities. Write findings to security-review.md.`

- **frontend-performance-reviewer** (`subagent_type: frontend-plugin:frontend-performance-reviewer`)
  Prompt: `Review $TARGET for performance issues including rendering, bundle size, and Web Vitals impact. Write findings to performance-review.md.`

- **accessibility-reviewer** (`subagent_type: frontend-plugin:accessibility-reviewer`)
  Prompt: `Review $TARGET for accessibility against WCAG 2.2 Level AA. Write findings to accessibility-review.md.`

Replace `$TARGET` with the actual review target (diff output, file list, or branch reference).

## Step 2: Consolidate findings inline

After all 4 specialists finish, read `quality-review.md`, `security-review.md`, `performance-review.md`, and `accessibility-review.md`.

Count findings by severity and determine the verdict:

- **GO**: No CRITICAL or HIGH findings
- **CONDITIONAL GO**: No CRITICAL, but HIGH findings exist
- **NO-GO**: Any CRITICAL finding exists

Present the consolidated summary to the user:

```
Review complete.

Verdict: [GO | CONDITIONAL GO | NO-GO]

| Severity | Count |
|----------|-------|
| CRITICAL | N     |
| HIGH     | N     |
| MEDIUM   | N     |
| LOW      | N     |

[List all HIGH and CRITICAL findings with source, description, and file location]

[List MEDIUM and LOW findings as optional improvements]
```
