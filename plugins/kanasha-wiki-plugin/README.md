# Wiki Plugin for Claude Code

A plugin that provides intelligent wiki management powered by [qmd](https://github.com/tobi/qmd) semantic search. Load development context dynamically and save knowledge back to the wiki — all with automatic index synchronization.

---

## Table of Contents

- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Skills](#skills)
  - [/load-wiki](#load-wiki)
  - [/save-wiki](#save-wiki)
- [How It Works](#how-it-works)

---

## Installation

This plugin is available through the Claude Code plugin marketplace.

**Source**: [github.com/fernandok4/ai-agents](https://github.com/fernandok4/ai-agents)

---

## Prerequisites

1. **qmd** must be installed:
   ```bash
   npm install -g @tobilu/qmd
   ```

2. **Wiki collection** must be indexed in qmd:
   ```bash
   qmd collection add wiki/pages --name wiki
   qmd embed
   ```

3. **Wiki schema** must exist at `wiki/CLAUDE.md` in the project (defines page format, frontmatter, and conventions).

---

## Quick Start

```bash
# Load context before starting development
/load-wiki I need to create a new SMS endpoint in the communication service

# After implementing, save new knowledge back to the wiki
/save-wiki new endpoint POST /v1/messages/sms for sending SMS messages
```

---

## Skills

### `/load-wiki <description>`

**Purpose**: Load relevant wiki context before development using intelligent semantic search.

**What it does**:
1. **Always loads core patterns** — project structure, code patterns, configuration, database patterns, multi-tenancy, platform overview
2. **Runs multiple qmd queries** — decomposes your description into 3-6 search angles (service, endpoint, security, data, flows, infrastructure)
3. **Reads discovered pages** — loads all relevant wiki pages as context
4. **Reports what was loaded** — summary of core + dynamic pages

**Examples**:
```bash
# Core patterns only
/load-wiki

# Backend service development
/load-wiki I'm adding a payment webhook endpoint

# Frontend work
/load-wiki I need to build the login screen in Flutter

# Cross-service flow
/load-wiki implement the password reset flow
```

---

### `/save-wiki <description>`

**Purpose**: Save knowledge to the wiki with proper formatting and automatic qmd sync.

**What it does**:
1. **Reads wiki schema** — follows `wiki/CLAUDE.md` conventions (frontmatter, categories, naming)
2. **Searches for related pages** — uses qmd to find pages for cross-referencing
3. **Creates or updates the page** — with proper frontmatter, wikilinks, callouts, Mermaid diagrams
4. **Adds cross-references** — bidirectional wikilinks with related pages
5. **Syncs qmd index** — runs `qmd update && qmd embed` so the content is immediately searchable

**Examples**:
```bash
# New endpoint documentation
/save-wiki new endpoint POST /v1/webhooks for payment service

# Architecture decision
/save-wiki decision: chose Redis over Memcached for SSE session storage

# Update existing service page
/save-wiki update authentication service with new MFA TOTP flow

# New cross-service flow
/save-wiki document the invoice generation flow between payment and product-catalog
```

---

## How It Works

### qmd Semantic Search

This plugin uses **qmd** for intelligent wiki discovery. qmd combines three search approaches:

- **BM25** — fast keyword matching
- **Vector search** — semantic similarity via embeddings
- **LLM reranking** — contextual relevance scoring

All processing runs locally on your machine — no cloud dependencies.

### Search Strategy

When loading context, the plugin doesn't just run one query. It decomposes your description into multiple search angles:

| Angle | Example Query |
|-------|--------------|
| Service | "communication service SMS" |
| Endpoint | "SMS provider endpoint API curl" |
| Pattern | "entity pattern repository service" |
| Security | "JWT authentication token" |
| Flow | "user registration cross-service" |
| Data | "Flyway migration database naming" |
| Infra | "RabbitMQ messaging exchange" |
| Frontend | "Flutter navigation state management" |

This ensures comprehensive coverage — you get all relevant context, not just the most obvious match.

---

## Project Structure

```
kanasha-wiki-plugin/
├── README.md           # This file
├── CLAUDE.md           # Design principles
└── skills/
    ├── load-wiki/
    │   └── SKILL.md    # /load-wiki skill definition
    └── save-wiki/
        └── SKILL.md    # /save-wiki skill definition
```

---

## Contributing

Contributions are welcome! Please follow the semantic commit conventions when submitting changes.
