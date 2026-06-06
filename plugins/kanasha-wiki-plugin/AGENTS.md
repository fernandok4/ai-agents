# Wiki Plugin

## Git Commits

Never add `Co-Authored-By` lines to commit messages. Do not include Claude as a co-author.

## Design Principles

### Skills Must Be Generic and Portable

When creating or editing skills, never include references that are specific to a particular machine, user, or environment. They must work for any user without modification.

- Never hardcode absolute paths (e.g., `/Users/someone/...`)
- Never reference specific project names or local workspace structures
- Use relative paths, glob patterns, or environment-based discovery instead

### Wiki Schema Is the Source of Truth

All wiki operations must follow the schema defined in the project's `wiki/CLAUDE.md`. Skills in this plugin do not define the wiki format — they read it from the project.

### qmd Is the Search Engine

This plugin uses [qmd](https://github.com/tobi/qmd) — an on-device semantic search engine — for intelligent wiki discovery. Skills must:

- Use `qmd query` for semantic search (hybrid: BM25 + vector + reranking)
- Use `qmd search` for fast keyword-only search (no LLM)
- Use `--no-rerank` when speed matters more than precision
- Always sync the index after writes (`qmd update && qmd embed`)

### Multiple Search Angles

When loading wiki context, never rely on a single query. Decompose the user's intent into multiple search angles (service, endpoint, pattern, security, data, etc.) to ensure comprehensive coverage.

## Project Structure

```
skills/          # Skills invoked via /skill-name (each has SKILL.md)
```
