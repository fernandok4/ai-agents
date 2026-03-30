# Review Orchestration Steps

Shared instructions for running the specialist reviewers and consolidating findings.

## Step 1: Run the 3 specialist reviewers in parallel

Spawn all 3 at the same time using the Agent tool:

- **quality-reviewer** (`subagent_type: kanasha-plugin:quality-reviewer`)
  Prompt: `Review $TARGET for code quality. Discover the project's existing patterns first. Write findings to quality-review.md.`

- **security-reviewer** (`subagent_type: kanasha-plugin:security-reviewer`)
  Prompt: `Review $TARGET for security vulnerabilities following OWASP Top 10. Write findings to security-review.md.`

- **performance-reviewer** (`subagent_type: kanasha-plugin:performance-reviewer`)
  Prompt: `Review $TARGET for performance issues. Write findings to performance-review.md.`

Replace `$TARGET` with the actual review target (diff output, file list, or branch reference).

## Step 2: Consolidate findings inline

After all 3 specialists finish, read `quality-review.md`, `security-review.md`, and `performance-review.md`.

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
