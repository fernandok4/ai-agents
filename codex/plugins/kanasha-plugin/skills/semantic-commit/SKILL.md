---
name: semantic-commit
description: Create semantic commits following strict standards, with one commit per modified file, using English for commit messages. Use when the user wants to commit changes following semantic versioning conventions, save their work with proper commit messages, or do a git commit.
allowed-tools: Bash, Read
---

## First Mandatory Action

**ALWAYS** ask which directory to use if not specified:
"In which directory should I execute the commits?"

## Core Rules

1. **Strictly follow** `knowledge/commit-standards.md` if it exists
2. **One commit per modified file** - never batch multiple files
3. **Format**: `type: objective description` (max 150 characters)
4. **English exclusively** for all commit messages
5. **NEVER** mention AI, Claude, or include `Co-Authored-By` tags
6. **Only `git add`** files that are ready; abort if conflicts exist
7. **Never use**: `git reset`, `git stash`, `git checkout`, or any destructive commands

## Commit Types

Use these standard types (consult `knowledge/commit-standards.md` for full list):

- **feat**: new feature
- **fix**: bug fix
- **docs**: documentation changes
- **refactor**: code refactoring
- **test**: test additions/modifications
- **chore**: maintenance tasks
- **perf**: performance improvements
- **style**: code style/formatting
- **ci**: CI/CD changes
- **build**: build system changes
- **revert**: revert previous commit

## Workflow

1. Ask for target directory if not specified
2. Run `git status` to identify modified files
3. For each modified file:
   - Analyze the changes using `git diff`
   - Determine appropriate commit type
   - Create concise, objective description in English
   - Execute: `git add <file> && git commit -m "type: description"`
4. Report completion summary

## Commit Format

```bash
git commit -m "type: description" /path/to/file
```

### Correct Examples

```bash
git commit -m "feat: add JWT authentication" src/auth.js
git commit -m "fix: correct email validation" src/validator.js
git commit -m "docs: update installation guide" README.md
git commit -m "refactor: simplify cache logic" src/cache.ts
```

### Incorrect Examples

- `git commit -m "feat: adiciona autenticacao JWT"` (Portuguese)
- `git commit -m "update files"` (missing type)
- `git commit -m "feat: adds authentication and fixes validation"` (multiple changes)
- Including `Co-Authored-By: Claude` (AI attribution)

## Prohibited Commands

**NEVER execute**:
- `git reset`
- `git stash`
- `git checkout` (except for branch switching when explicitly requested)
- `git commit --amend`
- `git rebase`
- Any command with `--force`
- Co-Authored-By tags
- AI/Claude mentions in commits

## Error Handling

- If conflicts detected: abort and notify user
- If file not ready: skip and report
- If commit fails: report error and continue with next file
- If directory not specified: ask before proceeding
