---
name: save-wiki
description: Save knowledge to the wiki following the schema conventions, then sync the qmd search index. Creates or updates pages with proper frontmatter, manages cross-references, and re-indexes qmd for semantic search.
user-invocable: true
argument-hint: "<description of what to save OR page name>"
---

# Save to Wiki (with qmd sync)

Saves knowledge to the wiki following the established schema in `wiki/CLAUDE.md`, then synchronizes the qmd search index so the new content is immediately discoverable via `/load-wiki`.

## Prerequisites

- qmd must be installed (`npm install -g @tobilu/qmd`)
- The wiki collection must exist in qmd (`qmd collection list` should show `wiki`)

## Instructions

When invoked, follow these steps:

### Step 0 — Understand what to save

Read the user's description to understand:
- **What knowledge** needs to be saved (new endpoint, service update, architecture decision, flow, etc.)
- **Which category** it belongs to (see wiki/CLAUDE.md for category definitions)
- **Whether it's a new page or an update** to an existing one

If the description is vague, ask the user for clarification before proceeding.

### Step 1 — Read the wiki schema

Read `wiki/CLAUDE.md` to understand the schema, frontmatter format, conventions, and content requirements. Use qmd (`qmd query` / `qmd search`) to check whether a page already exists for the topic.

### Step 2 — Determine the page category and path

Map the content to the correct category and directory:

| Category | Directory | When to use |
|----------|-----------|-------------|
| overview | `pages/overview/` | Platform-wide synthesis |
| services | `pages/services/` | Microservice documentation |
| architecture | `pages/architecture/` | Cross-cutting patterns |
| endpoints | `pages/endpoints/` | API endpoint documentation |
| flows | `pages/flows/` | Multi-step cross-service flows |
| security | `pages/security/` | JWT, encryption, auth |
| data | `pages/data/` | Database, Flyway, multi-tenancy |
| concepts | `pages/concepts/` | Domain concepts |
| decisions | `pages/decisions/` | Architectural decision records |

Filename: lowercase kebab-case, no date prefixes (e.g., `create-payment.md`, `webhook-patterns.md`).

### Step 3 — Search for related content with qmd

Before writing, use qmd to find related wiki pages that should be cross-referenced:

```bash
qmd query "<topic description>" --files -n 10 --no-rerank
```

Run 2-3 queries from different angles to find all related pages. These will be used for:
- The `related:` field in frontmatter
- Adding `[[wikilinks]]` to cross-reference from existing pages

### Step 4 — Write the page

Create or update the wiki page following ALL conventions from `wiki/CLAUDE.md`:

**Frontmatter** (required on every page):
```yaml
---
title: "Page Title"
aliases: ["alternative name"]
type: service | architecture | endpoint | flow | concept | decision | overview
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "../../relative/path/to/source"
tags: [relevant, tags]
related:
  - "[[related-page-1]]"
  - "[[related-page-2]]"
# For endpoint pages, also include:
service: authentication | communication | realtime | payment | product-catalog
method: GET | POST | PUT | DELETE | EVENT
path: "/api/kanasha/..."
auth: "ROLE_NAME" | null
---
```

**Content requirements by type:**

- **Endpoint pages** MUST include all 11 sections defined in wiki/CLAUDE.md (curl, errors, Mermaid, DB side effects, etc.)
- **Flow pages** MUST include Mermaid sequence diagrams
- **Service pages** MUST link to all their endpoints
- **Decision pages** should follow ADR format (context, decision, consequences)
- Use `[[wikilinks]]` to reference other pages
- Use `> [!warning]`, `> [!note]`, `> [!tip]` callouts appropriately
- Use `{{variableName}}` placeholders in curl commands

### Step 5 — Update cross-references

For each related page found in Step 3:
1. Read the related page
2. Add a `[[wikilink]]` to the new page where contextually appropriate
3. Add the related page to the new page's `related:` frontmatter if not already there

### Step 6 — Sync qmd index

Run these commands to make the new content immediately searchable:

```bash
# Re-index to pick up new/changed files
qmd update

# Re-generate embeddings for new content
qmd embed
```

This ensures `/load-wiki` can immediately find the new content via semantic search.

### Step 7 — Report what was saved

Provide a summary:

```
Wiki updated:
- Page: [path] (new|updated)
- Category: [category]
- Cross-references added: [list of pages that now link to this one]
- qmd index synced: [N] new/updated documents
```

## Examples

- `/save-wiki new endpoint POST /v1/webhooks for payment service`
  - Creates `wiki/pages/endpoints/create-webhook.md` with full endpoint documentation
  - Cross-references payment-service.md
  - Syncs qmd

- `/save-wiki architecture decision: we chose Redis over Memcached for SSE`
  - Creates `wiki/pages/decisions/redis-over-memcached.md` as ADR
  - Cross-references realtime-service.md
  - Syncs qmd

- `/save-wiki update authentication service with new MFA TOTP flow`
  - Updates existing `wiki/pages/services/authentication-service.md`
  - May create new flow page if complex enough
  - Syncs qmd
