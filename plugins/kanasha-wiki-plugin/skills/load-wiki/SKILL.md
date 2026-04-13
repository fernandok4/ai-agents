---
name: load-wiki
description: Load wiki context for development using qmd semantic search. Generates N intelligent query variations of the user's request (scaled by complexity) and loads only the pages qmd ranks as relevant. No hardcoded core — qmd decides what matters for the topic.
user-invocable: true
argument-hint: "<description of what you're going to work on>"
---

# Load Wiki Context (powered by qmd)

Load wiki pages as development context using **qmd** semantic search. No files are loaded blindly — every page read is one that qmd ranked as relevant to N intelligent variations of the user's request.

## Prerequisites

- qmd must be installed (`npm install -g @tobilu/qmd`)
- The wiki collection must be indexed (`qmd collection add wiki/pages --name wiki && qmd embed`)

## Instructions

### Step 1 — Read the user's request carefully

Understand what the user is about to do. Key axes to identify:

- **Scope**: single file? one feature? cross-service flow? architecture change?
- **Stack**: backend (Kotlin/Quarkus), frontend (Flutter), infra, docs portal?
- **Nature**: implementation, debugging, exploration/question, refactor?
- **Implicit concerns**: does it touch auth? multi-tenancy? persistence? messaging? UI state?

If no arguments are provided, skip to Step 4 and report nothing was loaded.

### Step 2 — Generate N query variations

Produce **multiple diverse query variations** covering every angle the request might touch. The goal is coverage: better to run one extra query than to miss a relevant page.

**How to scale N to request complexity:**

| Request type | Suggested N |
|---|---|
| Narrow/specific ("como a tela de login valida email?") | 3–4 queries |
| Feature implementation ("criar endpoint X no serviço Y") | 5–7 queries |
| Cross-service flow ("implementar fluxo de pagamento ponta a ponta") | 8–10 queries |
| Architecture/exploratory ("como o frontend é organizado?", "explica a arquitetura multi-tenant") | 6–9 queries |
| Refactor / migration / large change | 10–12 queries |

**Diversity heuristics — vary the queries across these axes (pick the ones that apply):**

1. **Direct rephrasing** — the user's own words, cleaned up
2. **Synonym/alternate terms** — e.g., "tela" → "screen", "auth" → "JWT token security"
3. **Service/component name** — name the likely service(s) explicitly
4. **Layer/pattern** — "repository pattern", "BLoC state management", "Flyway migration"
5. **Cross-cutting concerns** — multi-tenancy, security, rate limiting, if plausibly relevant
6. **Flow/lifecycle** — named flows ("user registration flow", "password reset flow")
7. **Infrastructure** — gateway, messaging, Docker, Nginx — if the task touches them
8. **Decision/ADR angle** — "why native SQL", "permissive auth model" for architecture questions
9. **Stack-specific vocabulary** — "Flutter Clean Architecture", "Quarkus ConfigMapping"

Write queries in **English** (the wiki is in English, embeddings match better). Keep them 3–8 words, concrete nouns over verbs.

### Step 3 — Execute queries and gather ranked files

Run all queries **in parallel** via a single message with multiple Bash calls:

```bash
qmd query "<variation>" --files -n 6 --no-rerank
```

- `--files` → file paths only
- `-n 6` → top 6 per query (adjust 5–10 based on N and expected breadth)
- `--no-rerank` → speed

**After collecting results:**

1. Deduplicate file paths across all queries
2. Weight by frequency — files that appear in multiple queries are higher signal
3. Trim by filename relevance — if a filename obviously doesn't match the topic, drop it even if qmd ranked it
4. Target final set: typically 5–15 pages. If you have >20 candidates, keep only those appearing in ≥2 queries or ranked high in ≥1

### Step 4 — Read selected pages

Read the final deduplicated set of wiki pages. Prefer reading them in parallel (multiple Read calls in one message).

If the task is purely exploratory and the user just asked a question, you may answer directly after reading. If the task is implementation, the loaded context stays in memory for the follow-up work.

### Step 5 — Report

Brief summary, in this format:

```
Wiki context loaded via qmd:
- Queries ran (N): "<q1>", "<q2>", ...
- Pages loaded (M): <page1>, <page2>, ...
- Dropped as off-topic: <pageX> (optional, only if you filtered anything notable)
```

Keep the report concise — the user cares that coverage was thorough, not verbose lists of every filename.

## Principles

- **qmd is the filter, not a hardcoded list.** Don't load "core" pages by path unless qmd ranks them relevant for this specific request.
- **Coverage > minimalism.** A missed page causes bad suggestions later. Run one more query when in doubt.
- **Parallelize aggressively.** All qmd queries in one message, all Read calls in one message.
- **Filenames are a sanity check.** qmd ranks by embedding similarity, which isn't perfect — if a filename is clearly unrelated, skip it.

## Examples

### Narrow question (N=3)
`/load-wiki como o LoginBloc lida com erro de senha inválida?`
- Queries: "login BLoC error handling", "login screen password validation", "frontend authentication error"
- Loads: frontend-code-patterns, frontend-state-management, login.md (endpoint)

### Feature implementation (N=6)
`/load-wiki vou criar um endpoint de SMS no communication service`
- Queries: "communication service SMS", "SMS provider configuration", "REST endpoint controller pattern", "multi-tenancy application_id", "RabbitMQ message producer", "rate limiting service"
- Loads: communication-service, sms-provider-config, code-patterns, multi-tenancy, service-communication, configuration-patterns

### Cross-service flow (N=9)
`/load-wiki implementar fluxo completo de pagamento com Stripe`
- Queries: "payment service Stripe gateway", "payment processing flow", "product catalog entitlements", "RabbitMQ payment events", "payment invoice transaction", "multi-tenancy payment", "encryption keys AES payment", "webhook signature verification", "database migration payment tables"
- Loads: 10–12 pages across services/, flows/, data/, security/

### Exploratory / architecture question (N=7)
`/load-wiki como o frontend é organizado?`
- Queries: "frontend Flutter monorepo structure", "Melos workspace packages", "Clean Architecture layers frontend", "frontend navigation routing", "BLoC state management frontend", "shared components kanasha_components", "frontend Docker deployment"
- Loads: frontend-monorepo, frontend-project-structure, frontend-clean-architecture, frontend-navigation, frontend-state-management, frontend-code-patterns, frontend-docker-deployment

### No arguments
`/load-wiki`
- Report: "No arguments given — pass a description of what you're going to work on so I can run targeted qmd queries."
