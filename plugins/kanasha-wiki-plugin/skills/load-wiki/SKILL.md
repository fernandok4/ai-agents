---
name: load-wiki
description: Load wiki context for development using qmd semantic search. Always loads core patterns (code-patterns, multi-tenancy, database, project-structure, configuration). Dynamically discovers additional pages via intelligent qmd queries based on arguments. Use before any development task.
user-invocable: true
argument-hint: "<description of what you're going to work on>"
---

# Load Wiki Context (powered by qmd)

Intelligently loads wiki pages as development context using **qmd** semantic search. Core patterns are ALWAYS loaded. Additional pages are discovered dynamically through multiple intelligent queries based on what the user describes.

## Prerequisites

- qmd must be installed (`npm install -g @tobilu/qmd`)
- The wiki collection must be indexed (`qmd collection add wiki/pages --name wiki && qmd embed`)

## Instructions

When invoked, follow these steps:

### Step 1 — Always load core patterns

Read ALL of these files (they are mandatory for any development):

1. `wiki/pages/overview/platform-overview.md`
2. `wiki/pages/architecture/project-structure.md`
3. `wiki/pages/architecture/code-patterns.md`
4. `wiki/pages/architecture/configuration-patterns.md`
5. `wiki/pages/data/database-patterns.md`
6. `wiki/pages/data/multi-tenancy.md`

### Step 2 — Intelligent dynamic search with qmd

If the user provides arguments describing what they're going to work on, perform **multiple qmd queries** to discover all relevant wiki pages. The goal is to be thorough — cast a wide net with diverse queries.

#### How to generate queries

Analyze the user's description and decompose it into multiple search angles:

1. **Service-level query**: Which service(s) are involved?
   - Example: user says "SMS provider" → query for "communication service SMS"
2. **Endpoint-level query**: Which API endpoints might be relevant?
   - Example: user says "create user" → query for "create user endpoint API"
3. **Pattern-level query**: Which architectural patterns apply?
   - Example: user says "new entity" → query for "entity pattern repository service"
4. **Security query**: Does the task touch auth, encryption, or roles?
   - Example: user says "login flow" → query for "JWT authentication token security"
5. **Flow query**: Is there a cross-service flow involved?
   - Example: user says "registration" → query for "user registration flow"
6. **Data query**: Does it involve database, migrations, or multi-tenancy?
   - Example: user says "new table" → query for "Flyway migration database naming"
7. **Infrastructure query**: Does it involve gateway, messaging, or config?
   - Example: user says "events" → query for "RabbitMQ messaging exchange routing"
8. **Frontend query**: Does it involve UI, Flutter, or navigation?
   - Example: user says "profile screen" → query for "Flutter navigation state management"

#### How to execute queries

Run each query using the Bash tool with `qmd query`:

```bash
qmd query "<your search query>" --files -n 8 --no-rerank
```

Use `--no-rerank` for speed. Use `--files` to get just file paths. Use `-n 8` to get enough candidates.

**Generate at least 3 queries, up to 6 queries** depending on the complexity of the task. Run them in parallel when possible.

#### Deduplication

Collect all unique file paths from all queries. Remove duplicates and remove any files that were already loaded in Step 1 (core patterns).

### Step 3 — Read discovered pages

Read all unique wiki pages discovered by qmd that are relevant to the task. Use your judgment — if a result seems irrelevant based on its filename, skip it.

### Step 4 — Report what was loaded

After reading all files, provide a brief summary:

```
Wiki context loaded via qmd:
- Core patterns (6 pages): platform-overview, project-structure, code-patterns, configuration-patterns, database-patterns, multi-tenancy
- Dynamic (N pages via qmd search):
  - [list each page loaded with one-line description]
- Queries used: [list the qmd queries you ran]
```

## Examples

- `/load-wiki vou criar um novo endpoint de SMS no communication service`
  - Core patterns loaded
  - qmd queries: "communication service SMS", "SMS provider endpoint API curl", "service controller DTO pattern", "RabbitMQ messaging communication"
  - Discovers: communication-service.md, sms-provider-config.md, email-provider-config.md (similar pattern), service-communication.md

- `/load-wiki preciso implementar o fluxo de pagamento no payment service`
  - Core patterns loaded
  - qmd queries: "payment service processing", "payment flow event-driven", "RabbitMQ payment events", "product catalog entitlements"
  - Discovers: payment-service.md, payment-flow.md, service-communication.md, product-catalog-service.md

- `/load-wiki vou mexer na tela de login do frontend Flutter`
  - Core patterns loaded
  - qmd queries: "Flutter login screen authentication", "frontend navigation routing", "JWT token security OAuth2", "frontend state management"
  - Discovers: frontend-monorepo.md, frontend-navigation.md, frontend-state-management.md, login.md, oauth2-token.md, jwt-security-model.md

- `/load-wiki` (no arguments)
  - Only core patterns loaded (no qmd queries needed)
