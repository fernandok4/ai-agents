---
name: frontend-severity-standards
description: Unified severity level definitions used by all frontend reviewer agents for consistent finding classification.
---

# Severity Levels

Unified severity definitions used by all reviewer agents.

## Critical

Blocks deployment. Must fix before merge.

**Examples**: XSS vulnerability with user content, hardcoded secrets in client bundle, authentication bypass, complete keyboard inaccessibility on primary flow, infinite re-render loop, memory leak crashing the tab.

## High

User-facing impact. Should fix before deploy, blocks only if multiple exist.

**Examples**: Missing form labels on critical forms, invisible focus indicators, token stored in localStorage, render-blocking bundle >500KB, N+1 waterfall API calls, CLS-causing layout shifts, missing error handling on user-facing flows.

## Medium

Technical debt that compounds over time. Plan to address within the sprint.

**Examples**: Code duplication >20 lines, missing tests for non-trivial components, excessive prop drilling, full library imports, missing lazy loading on heavy routes, non-descriptive link text, minor heading hierarchy issues.

## Low

Style and polish. Track for later.

**Examples**: Formatting inconsistencies, minor naming improvements, redundant ARIA on semantic elements, optional memoization opportunities, missing autocomplete attributes.
