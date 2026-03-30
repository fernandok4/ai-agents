# Persistent Agent Memory — prompt-architect

## Review System Design (established 2026-02-20)

### Specialist reviewer pattern
- Specialist reviewers (quality, security, performance) send findings via team messages — they do NOT write files
- Tools for specialists: `Read, Grep, Glob, Bash` (no Write)
- Overall-reviewer is the only one that writes a file (`overall-review.md`)
- Tools for overall-reviewer: `Read, Write, Glob` (no Bash needed)

### Compact findings format (mandatory for all specialists)
Each finding has exactly 6 fields: Problem N, File:Line, Rating, Type, Problem, Fix.
No executive summaries, no tables, no deployment decisions in specialist output.

### Acknowledged non-problems pattern
All reviewers with `memory: project` must:
1. Read `.claude/agent-memory/{agent-name}/acknowledged.md` before reporting
2. Skip findings that match acknowledged patterns silently
3. Save dismissed findings to that file with Pattern, Reason, Date

### Cross-cutting elevation rule (overall-reviewer)
Same File:Line in 2+ specialist messages → elevate severity by one level.
Append `(Elevated: appears in Source1 + Source2)` to Type field.

### Deployment verdict rules (overall-reviewer)
- NO-GO: any CRITICAL finding
- CONDITIONAL GO: any HIGH, no CRITICAL
- GO: only MEDIUM/LOW or no findings

### Quality-reviewer: pattern discovery is mandatory
Before analyzing diff, quality-reviewer must:
1. Read config files (lint, format, architecture docs)
2. Identify what the diff introduces (cache, WebClient, repository, service, etc.)
3. Find the project's existing pattern for that construct
4. Only flag deviations if a prior pattern exists — never flag when no prior pattern is found

### Team-based command pattern
project-review command spawns 4 agents: 3 specialists in parallel + 1 overall-reviewer waiting for all 3.
Task 4 (overall-reviewer) is blocked by Tasks 1, 2, 3.
After overall-reviewer writes the file, shut down team and present findings inline.
