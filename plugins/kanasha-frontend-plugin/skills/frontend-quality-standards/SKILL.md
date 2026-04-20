---
name: frontend-quality-standards
description: Shared frontend code quality thresholds and criteria used by the frontend-quality-reviewer agent.
user-invocable: false
---

# Frontend Quality Standards

Shared thresholds for frontend code quality. Agents referencing this skill use these as their baseline.

## Component Size

- Component file: **< 200 lines** (including template/JSX)
- Props count: **≤ 8** per component (use composition or object props otherwise)
- Nesting levels in JSX/template: **≤ 4**
- Custom hooks: **< 50 lines** per hook

## Function Size

- Functions: **< 50 lines**
- Event handlers: **< 20 lines** (extract logic to hooks or utilities)
- Parameters per function: **≤ 3** (use options object otherwise)

## Complexity

- Cyclomatic complexity: **< 15** per function
- Conditional rendering branches: **≤ 5** per component (extract to sub-components otherwise)
- Code duplication: **< 20 lines** of identical logic

## Test Coverage

- New components: **80%** minimum
- Custom hooks: **100%** — hooks contain reusable logic and must be thoroughly tested
- Utility functions: **100%**
- Critical user flows (auth, checkout, data mutation): **100%**
- Tests must be meaningful, not coverage padding

## Component Design Principles

- **Single Responsibility**: each component does one thing well
- **Composition over Configuration**: prefer children/slots/render props over boolean props that switch behavior
- **Controlled vs. Uncontrolled**: be intentional about state ownership
- **Separation of Concerns**: presentation components don't fetch data; container components don't render complex UI
- **Naming**: clear, descriptive, intent-revealing. Component names match file names.

## State Management

- **Minimal state**: if it can be derived from props or other state, it's not state
- **Colocated state**: state lives as close to where it's used as possible
- **No prop drilling > 3 levels**: use composition, context, or state management
- **Normalized state shape**: avoid deeply nested or duplicated state

## Over-Engineering Threshold

**Flag** as over-engineered when:
- >100 LOC to solve a problem achievable in <30 LOC
- Abstraction layers with only one component using them
- Design pattern applied where a simple component would suffice
- Configuration/props system for variations that don't exist yet
- Custom state management when the framework's built-in solution works

**Do NOT flag**:
- Abstractions used by 2+ components
- Standard framework patterns (even if verbose)
- Code following existing project conventions
- Accessibility patterns that add verbosity but are required
