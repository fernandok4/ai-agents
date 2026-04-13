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

### Step 2 — Generate N query variations (scope-locked)

Produce **multiple diverse query variations**, but every variation must stay inside the **scope the user explicitly named**. Vary the angle, not the subject.

**Scope lock — MANDATORY:**

1. Before generating queries, identify the scope anchors from the user's request:
   - **Service/project** named (e.g., `authentication`, `communication`, `payment`, `frontend-monorepo`)
   - **Feature/flow** named (e.g., "password reset", "SMS sending")
   - **Layer/component** named (e.g., "repository", "BLoC", "endpoint")
2. **Every query variation must reference at least one scope anchor.** If the user said "authentication", do not generate queries about communication, payment, realtime, etc. — even if they seem topically adjacent.
3. Cross-cutting pages (multi-tenancy, security, code-patterns) are only fair game when the user's task actually touches them. When in doubt, qualify them with the scope anchor (e.g., `authentication multi-tenancy application_id`, not bare `multi-tenancy`).
4. If you are tempted to widen scope "just in case", stop — ask the user instead of searching.

The goal is **targeted coverage within the user's scope**, not broad sweeps across the platform.

**How to scale N to request complexity:**

| Request type | Suggested N |
|---|---|
| Narrow/specific ("como a tela de login valida email?") | 3–4 queries |
| Feature implementation ("criar endpoint X no serviço Y") | 5–7 queries |
| Cross-service flow ("implementar fluxo de pagamento ponta a ponta") | 8–10 queries |
| Architecture/exploratory ("como o frontend é organizado?", "explica a arquitetura multi-tenant") | 6–9 queries |
| Refactor / migration / large change | 10–12 queries |

**Diversity heuristics — vary the ANGLE within the user's scope (pick the ones that apply):**

Every heuristic below must be applied **inside the scope anchors** from Step 2. The axis is how you phrase the query; the subject stays locked to what the user asked about.

1. **Direct rephrasing** — the user's own words, cleaned up
2. **Synonym/alternate terms** — e.g., "tela" → "screen", "auth" → "JWT token security" (still within the same service)
3. **Layer/pattern, scoped** — e.g., `authentication repository pattern`, not bare `repository pattern`
4. **Flow/lifecycle, scoped** — named flows belonging to the target service ("password reset flow" when the user is on authentication)
5. **Cross-cutting concerns, scoped** — only when the task actually touches them, and qualified with the scope anchor (`authentication multi-tenancy`, not bare `multi-tenancy`)
6. **Stack-specific vocabulary, scoped** — `Quarkus ConfigMapping authentication`, `Flutter BLoC login screen`
7. **Decision/ADR angle, scoped** — `authentication permissive auth model` for architecture questions about that service
8. **Infrastructure, scoped** — only if the user's task touches gateway/messaging/Docker for their service

**Forbidden:** pulling in another service's name, flow, or components just to "increase coverage". If the user said authentication, queries mentioning communication/payment/realtime/etc. are off-scope unless the user explicitly named the integration.

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
4. **Enforce scope lock on results** — any file whose name clearly belongs to a different service/feature than the user's scope anchors must be dropped. qmd similarity can leak across adjacent domains; the filename is the final guard
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
- **Scope lock beats coverage.** Targeted coverage *within the user's scope* is the goal. Searching another service's pages "just in case" is a bug, not thoroughness. If the user asks about authentication, communication/payment/realtime pages must not be queried or loaded.
- **Vary the angle, not the subject.** Diversity across phrasings, layers, and lifecycles — never across unrelated services.
- **Parallelize aggressively.** All qmd queries in one message, all Read calls in one message.
- **Filenames are the final scope guard.** qmd ranks by embedding similarity, which leaks across adjacent domains — if a filename clearly belongs to a service the user didn't name, skip it.

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

### Scope lock — anti-example (what NOT to do)

`/load-wiki quero entender como a autenticação valida o código do e-mail`
- Scope anchors: `authentication`, `email challenge validation`
- ✅ Correct queries: "authentication validate challenge email", "authentication challenge code verification", "authentication email provider challenge"
- ❌ Wrong queries: "communication challenge validation" (different service), "payment email receipts" (off-scope), "realtime SSE events" (off-scope)
- ❌ Wrong loads: `communication-service.md`, `validate-challenge.md` under communication — drop even if qmd ranks them, because the user asked about authentication

### No arguments
`/load-wiki`
- Report: "No arguments given — pass a description of what you're going to work on so I can run targeted qmd queries."
