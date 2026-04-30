---
name: frontend-performance-standards
description: Shared frontend performance, scalability, and optimization criteria used by the frontend-performance-reviewer agent.
---

# Frontend Performance Standards

Shared thresholds for frontend performance analysis. Agents referencing this skill use these as their baseline.

## Web Vitals Targets

Use these baselines unless the project specifies otherwise:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| FCP (First Contentful Paint) | ≤ 1.8s | ≤ 3.0s | > 3.0s |
| TTFB (Time to First Byte) | ≤ 800ms | ≤ 1.8s | > 1.8s |

## Bundle Size Budgets

| Category | Budget |
|----------|--------|
| Initial JS bundle (compressed) | < 200KB |
| Per-route chunk (compressed) | < 50KB |
| Total CSS (compressed) | < 50KB |
| Single image (hero/banner) | < 200KB |
| Total page weight (initial load) | < 1MB |

If the project has its own bundle budgets (webpack/vite config), use those instead.

## Rendering Performance

**Re-render Detection**:
- Flag components that re-render on every parent render without prop changes
- Flag missing memoization on expensive computations (> 1ms estimated)
- Flag inline object/array/function creation in render that causes child re-renders
- Do NOT flag memoization of trivial operations (string concatenation, simple conditionals)

**DOM Performance**:
- Flag lists > 100 items rendered without virtualization
- Flag layout-triggering CSS properties in animations (use transform/opacity)
- Flag forced synchronous layouts (read-then-write DOM patterns)

## Data Fetching

**Waterfall Detection**:
- Flag sequential API calls that could be parallelized
- Flag data fetching in child components that blocks rendering (fetch in parent instead)
- Flag missing prefetching for predictable navigation targets

**Caching**:
- Frequently accessed, rarely changed data should be cached
- API responses should leverage HTTP caching headers
- Appropriate stale-while-revalidate patterns
- Cache invalidation on mutations

## Network Optimization

**Assets**:
- Images: modern formats (WebP/AVIF), responsive srcset, lazy loading below fold
- Fonts: subset to used characters, font-display: swap/optional, preload critical fonts
- Scripts: defer/async non-critical scripts, no render-blocking third-party scripts

**API Calls**:
- Batch multiple small requests when possible
- Use compression (gzip/brotli)
- Connection reuse (HTTP/2+)

## Memory

**Leak Detection**:
- Event listeners without cleanup on component unmount
- Subscriptions (WebSocket, observables) without unsubscribe
- Intervals/timeouts without clearance
- References to detached DOM nodes
- Closures capturing large objects unnecessarily

**Budget**:
- Page memory usage: < 50MB typical, < 100MB maximum
- No continuous memory growth during normal usage

## Premature Optimization Thresholds

**Flag** (worth reporting):
- Lists > 100 items without virtualization
- Bundle > 200KB initial JS
- Waterfall API calls on critical path
- Images > 200KB without optimization
- Missing code splitting on routes
- Expensive computations (> 1ms) in render without memoization
- Memory leaks (event listeners, subscriptions not cleaned)

**Ignore** (do not flag):
- Memoization on trivial computations
- Lists < 50 items without virtualization
- One-time startup operations
- Development-only overhead (HMR, dev tools)
- Micro-optimizations saving < 1ms in typical usage
