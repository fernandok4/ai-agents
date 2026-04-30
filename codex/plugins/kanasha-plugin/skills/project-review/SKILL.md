---
name: project-review
description: Performs a comprehensive code review by orchestrating specialist reviewers (quality, security, performance) in parallel, then consolidating their findings inline with a deployment verdict. Use when the user wants to review code, check changes before merging, run a pre-merge review, or validate code quality of a diff or branch.
---

Performs a comprehensive code review by orchestrating specialist reviewers in parallel, then consolidating their findings inline.

## Usage

```
/project-review [target]
```

Default target: uncommitted changes (`git diff HEAD`).

## Instructions

Follow the orchestration steps in `references/review-orchestration.md`.

When passing the target to specialist reviewers, replace `$TARGET` with the user's argument (or `git diff HEAD` if no argument was provided).

After all reviewers finish, consolidate the findings inline as described in Step 2 of `references/review-orchestration.md`. Read all 3 review files, count findings by severity, determine the verdict (GO / CONDITIONAL GO / NO-GO), and present everything to the user.
