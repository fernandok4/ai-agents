---
name: performance-standards
description: Shared performance, scalability, and optimization criteria used by software-architect and performance-reviewer agents.
user-invocable: false
---

# Performance Standards

Shared thresholds for performance and scalability analysis. Agents referencing this skill use these as their baseline.

## Default Scale Assumptions

Use these baselines unless the project specifies otherwise:

| Metric | Default Value |
|--------|--------------|
| Concurrent users | 1,000 |
| Records per table | 100,000 |
| Response time (p95) | 100ms |
| Memory budget per instance | 512MB |
| Database connections per pool | 20 |

If the project contains load test configs, SLAs, or infrastructure limits, use those values instead.

## Algorithm Complexity

**Time Complexity**:
- Identify Big-O complexity for each function
- Flag O(n^2) or worse in production hot paths
- Check for unnecessary nested loops
- Identify recursive calls without memoization

**Space Complexity**:
- Memory allocation patterns
- Data structure size growth
- Stack usage in recursion
- Memory leaks (objects not released)

## Database Performance

**N+1 Query Detection**:
- Detect loops with database queries inside
- Missing eager loading/joins
- Suggest batch loading

**Query Optimization**:
- SELECT * anti-pattern
- Missing WHERE clauses on large tables
- No pagination on large result sets
- Missing indexes on queried columns (>10K rows)
- Inefficient JOINs

## Caching

**Identify Cacheable Data**:
- Frequently accessed, rarely changed data
- Expensive computations with same inputs
- External API calls
- Database query results

**Cache Strategy**:
- Appropriate TTL set?
- Cache invalidation logic correct?
- Cache key design efficient?
- Right caching layer (memory, Redis, CDN)?

## Resource Usage

**CPU**: tight loops without breaks, heavy computation in request handlers, regex catastrophic backtracking, synchronous blocking operations.

**Memory**: loading entire datasets into memory, memory leaks (event listeners, timers not cleaned), large object allocations, string concatenation in loops.

**I/O**: excessive disk reads/writes, file operations in loops, synchronous I/O in async contexts, no buffering for large files.

**Network**: multiple sequential API calls (use parallel), large payloads without compression, missing connection reuse, no request batching.

## Concurrency & Scalability

**Concurrency**: race conditions, deadlock potential, lock contention, global state in multi-threaded context.

**Scalability**: algorithms that don't scale linearly, single-threaded bottlenecks, shared state preventing horizontal scaling, session affinity requirements, stateless preferred over stateful, data partitioning at 10x/100x growth.

## Premature Optimization Thresholds

**Flag** (worth reporting):
- O(n^2) or worse on collections that could exceed 100 items
- N+1 queries on any endpoint
- Loading entire tables into memory without pagination
- Synchronous blocking in async contexts
- Missing indexes on columns used in WHERE/JOIN with >10K rows

**Ignore** (do not flag):
- O(n^2) on collections guaranteed <20 items
- String concatenation with <10 iterations
- Micro-optimizations that save <1ms in typical usage
- One-time startup operations
