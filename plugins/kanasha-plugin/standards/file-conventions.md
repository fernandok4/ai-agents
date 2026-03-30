# File Conventions

## Output Locations

| Agent | Output | Location |
|-------|--------|----------|
| software-architect | `spec.md` | Current directory |
| tech-team-architect | `team-plan.md` | Current directory |
| backend-developer | (code files) | As specified by user/spec |
| qa-engineer | (test files) | Project test directory |
| database-specialist | (migrations, schema) | As specified by project |
| e2e-test-runner | (test report) | Inline or current directory |
| quality-reviewer | `quality-review.md` | Current directory |
| security-reviewer | `security-review.md` | Current directory |
| performance-reviewer | `performance-review.md` | Current directory |

## File Reference Format

When referencing code locations, use: `path/to/file.ext:lineNumber`

Examples:
- `src/controllers/UserController.ts:42`
- `lib/auth/jwt.py:15`
