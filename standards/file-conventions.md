# File Conventions

## Output Locations

| Agent | Output File | Location |
|-------|------------|----------|
| project-researcher | `initial-search.md` | Current directory |
| spec-architect | `spec.md` | Current directory |
| implementer | (code files) | As specified by user/spec |
| security-reviewer | `security-review.md` | Current directory |
| performance-reviewer | `performance-review.md` | Current directory |
| quality-reviewer | `quality-review.md` | Current directory |
| overall-reviewer | `overall-review.md` | Current directory |
| tech-documenter | `documentation.md` | `tech-docs/` directory |
| product-documenter | `documentation.md` | `docs/` directory |
| product-advisor | (inline response) | No file output |
| prompt-architect | Agent `.md` file | `.claude/agents/` or `agents/` |

## File Reference Format

When referencing code locations, use: `path/to/file.ext:lineNumber`

Examples:
- `src/controllers/UserController.ts:42`
- `lib/auth/jwt.py:15`
