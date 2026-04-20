---
name: quality-standards
description: Shared code quality thresholds and criteria used by the quality-reviewer agent.
user-invocable: false
---

# Quality Standards

Shared thresholds for code quality. Agents referencing this skill use these as their baseline.

## Function & Class Size

- Functions: **< 50 lines**
- Classes: **< 500 lines**
- Nesting levels: **≤ 3**
- Parameters per function: **≤ 3** (use options object otherwise)

## Complexity

- Cyclomatic complexity: **< 15** per function
- Code duplication: **< 20 lines** of identical logic

## Test Coverage

- New code: **80%** minimum
- Critical paths: **100%**
- Tests must be meaningful, not coverage padding

## Design Principles

- **Single Responsibility**: each function/class does one thing well
- **DRY**: no duplicated logic, but avoid premature abstraction
- **SOLID**: applied appropriately, not dogmatically
- **Naming**: clear, descriptive, intent-revealing. No abbreviations unless universally understood. Consistent conventions (camelCase, snake_case, etc.)

## Over-Engineering Threshold

**Flag** as over-engineered when:
- \>100 LOC to solve a problem achievable in <30 LOC
- Abstraction layers with only one implementation and no planned extension
- Design pattern applied where a simple function would suffice
- Configuration system for values that never change

**Do NOT flag**:
- Abstractions with 2+ implementations
- Standard framework patterns (even if verbose)
- Code following existing project conventions
