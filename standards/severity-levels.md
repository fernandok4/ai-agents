# Severity Levels

Unified severity definitions used by all reviewer agents.

## Critical

Blocks deployment. Must fix before merge.

**Examples**: SQL injection, hardcoded secrets, authentication bypass, data loss on write path, unhandled null on critical path causing crash.

## High

User-facing impact. Should fix before deploy, blocks only if multiple exist.

**Examples**: Performance degradation >500ms p95, weak cryptography (MD5/SHA1 for security), missing authorization checks on non-critical endpoints, N+1 queries on pages with >100 records.

## Medium

Technical debt that compounds over time. Plan to address within the sprint.

**Examples**: Code duplication >20 lines, missing tests for non-trivial logic, cyclomatic complexity >15, functions >50 lines, unclear naming patterns.

## Low

Style and polish. Track for later.

**Examples**: Formatting inconsistencies, optional micro-optimizations, minor naming improvements, missing optional logging.
