# Project Command

Performs comprehensive code review by orchestrating parallel specialist reviewers.

## Usage

```
/review [target]
```

Default: uncommitted changes.

## Instructions

1. **Launch in parallel** using the Task tool:
   - **performance-reviewer**: `Review [target]. Write findings to performance-review.md`
   - **security-reviewer**: `Review [target]. Write findings to security-review.md`
   - **quality-reviewer**: `Review [target]. Write findings to quality-review.md`

2. **After all complete**, launch **overall-reviewer**:
   - `Read performance-review.md, security-review.md, quality-review.md. Synthesize into overall-review.md with deployment decision.`

3. **Present summary** from overall-review.md to user.
