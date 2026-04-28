---
name: load-wiki
description: Load wiki context by running `qmd query` with the user's argument verbatim and reading the top-ranked pages. Cross-references are listed but not read unless explicitly requested.
user-invocable: true
argument-hint: "<query string — passed to qmd verbatim>"
---

# Load Wiki Context

Run `qmd query` with the argument **exactly as given** and read the top-ranked pages. Do not follow cross-references automatically.

## Prerequisites

- qmd installed (`npm install -g @tobilu/qmd`)
- Wiki collection indexed (`qmd collection add wiki/pages --name wiki && qmd embed`)

## Steps

### 1. Run the query

Pass the argument verbatim:

```bash
qmd query "<argument>" --files -n 8 --no-rerank
```

If no argument was given, report that and stop.

### 2. Read the top-ranked pages

Resolve the returned paths to files under `wiki/pages/` and read them in parallel.

### 3. Report

List what was loaded and surface the cross-references found, without reading them:

```
Wiki context loaded:
- Query: "<argument>"
- Loaded (M): <page1>, <page2>, ...
- Cross-references available (not loaded): <pageX>, <pageY>, ...
```

Read a cross-reference only if the user explicitly asks for it.
