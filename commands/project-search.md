# Project Search Command

Analyzes the project and generates a `CLAUDE.md` file with product description and tech stack.

## Usage

```
/project-search
```

## Instructions

Use the **project-researcher** subagent to analyze the current project and generate a `CLAUDE.md` file at the project root. This file provides context about what the project does (in product-friendly terms) and what technologies it uses.

## Output

The command generates `CLAUDE.md` at the project root with:
- **What the project does** (non-technical description)
- **Tech stack used** (brief list)

## When to Use

Run this command when starting work on a new project to create shared context for all agents.
