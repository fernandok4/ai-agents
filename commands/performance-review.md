# Performance Review Command

Performs deep performance analysis focusing on algorithm complexity, resource usage, scalability, and optimization opportunities.

## Objective

Identify performance bottlenecks, inefficient algorithms, resource waste, and scalability issues that could impact production performance.

## Usage

**Pattern**: `/performance-review [what to review]`

**Examples**:
- `/performance-review` → performance scan of uncommitted changes
- `/performance-review my branch` → performance scan of current branch
- `/performance-review src/api/users.ts` → specific file analysis
- `/performance-review the getUserData method` → method optimization review
- `/performance-review for N+1 queries` → focused database query analysis

## Instructions

### 1. Target Identification

Same as general code review:
- Parse natural language to identify what to review
- Default to uncommitted changes if not specified
- Use Grep/Glob to locate specific methods/classes
- Check conversation history for context

### 2. Performance Analysis Layers

#### Algorithm Complexity

**Time Complexity Analysis**:
- Identify Big-O complexity for each function
- Flag O(n²) or worse in production hot paths
- Check for unnecessary nested loops
- Identify recursive calls without memoization
- Look for exponential complexity algorithms

**Space Complexity**:
- Memory allocation patterns
- Data structure size growth
- Stack usage in recursion
- Memory leaks (objects not released)

**Examples to Flag**:
```javascript
// ❌ O(n²) - nested iteration
users.forEach(user => {
  posts.forEach(post => {
    if (post.userId === user.id) { ... }
  })
})

// ✅ O(n) - use Map/hash lookup
const postsByUser = new Map()
posts.forEach(post => {
  if (!postsByUser.has(post.userId)) postsByUser.set(post.userId, [])
  postsByUser.get(post.userId).push(post)
})
```

#### Database Performance

**N+1 Query Problem**:
- Detect loops with database queries inside
- Missing eager loading/joins
- Suggest batch loading

**Query Optimization**:
- SELECT * anti-pattern
- Missing WHERE clauses on large tables
- No pagination on large result sets
- Missing indexes on queried columns
- Inefficient JOINs
- Subqueries that could be JOINs

**Examples to Flag**:
```python
# ❌ N+1 query problem
users = User.query.all()
for user in users:
    posts = Post.query.filter_by(user_id=user.id).all()  # N queries!

# ✅ Use eager loading
users = User.query.options(joinedload(User.posts)).all()
```

**Connection Management**:
- Connection pooling used?
- Connections properly closed?
- Transaction scope appropriate?

#### Caching Opportunities

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

**Examples**:
```javascript
// ❌ Expensive computation on every request
function getStats(userId) {
  return db.query('SELECT ... complex aggregation ...')
}

// ✅ Cache with appropriate TTL
const cache = new Map()
function getStats(userId) {
  const cached = cache.get(userId)
  if (cached && Date.now() - cached.time < 300000) return cached.data
  const data = db.query('SELECT ... complex aggregation ...')
  cache.set(userId, { data, time: Date.now() })
  return data
}
```

#### Resource Usage

**CPU Usage**:
- Tight loops without breaks
- Heavy computation in request handlers
- Regex performance (catastrophic backtracking)
- Synchronous blocking operations
- No use of multi-threading/async where appropriate

**Memory Usage**:
- Loading entire datasets into memory
- Memory leaks (event listeners, timers not cleaned)
- Large object allocations
- String concatenation in loops
- Inefficient data structures

**I/O Operations**:
- Excessive disk reads/writes
- File operations in loops
- Synchronous I/O in async contexts
- No buffering for large files

**Network**:
- Multiple sequential API calls (use parallel)
- Large payloads without compression
- Missing connection reuse
- No request batching

#### Concurrency & Scalability

**Concurrency Issues**:
- Race conditions
- Deadlocks potential
- Lock contention
- Global state in multi-threaded context

**Scalability Concerns**:
- Algorithms that don't scale linearly
- Single-threaded bottlenecks
- Shared state preventing horizontal scaling
- Session affinity requirements

**Load Handling**:
- Can handle expected traffic?
- Graceful degradation under load?
- Circuit breakers for external services?
- Request queuing/throttling?

#### Code-Level Performance

**Inefficient Patterns**:
```javascript
// ❌ Array operations in loop
for (let i = 0; i < items.length; i++) {  // length recalculated each time
  // ...
}

// ✅ Cache length
const len = items.length
for (let i = 0; i < len; i++) {
  // ...
}

// ❌ String concatenation in loop
let result = ''
for (const item of items) {
  result += item  // Creates new string each time
}

// ✅ Use array join
const result = items.join('')

// ❌ Unnecessary object creation
function process(data) {
  return { ...data, processed: true }  // Creates new object
}

// ✅ Mutate if appropriate
function process(data) {
  data.processed = true
  return data
}
```

**Early Returns**:
- Check for expensive operations after cheap validations
- Use guard clauses
- Short-circuit evaluation

#### Framework/Library Specific

**React/Frontend**:
- Unnecessary re-renders
- Missing memoization (useMemo, useCallback)
- Large bundle sizes
- Missing code splitting
- Images not optimized

**Node.js**:
- Blocking event loop
- Missing async/await
- Synchronous file operations
- Buffer misuse

**Python**:
- List comprehensions vs generators
- Missing NumPy for large arrays
- GIL contention in multi-threading

**Java**:
- Stream API misuse
- Unnecessary object creation
- Missing connection pooling
- Reflection in hot paths

### 3. Profiling Recommendations

Suggest profiling for:
- Functions with high cyclomatic complexity
- Loops with non-constant iterations
- Recursive functions
- Database-heavy operations
- External API calls

### 4. Performance Report

```markdown
# Performance Review Report

**Target**: [what was reviewed]
**Date**: [timestamp]
**Performance Rating**: 🟢 EXCELLENT | 🟡 NEEDS OPTIMIZATION | 🔴 CRITICAL ISSUES

## Executive Summary

[Brief performance assessment]

**Production Impact**: [Expected performance under production load]

**Recommendation**: [Can deploy / Should optimize / Must fix before deploy]

---

## Critical Performance Issues (X)

### [Issue Title]
**Severity**: CRITICAL
**File**: path/to/file.ext:line
**Complexity**: O(n²) [or relevant metric]

**Problem**: [What's inefficient]

**Impact**:
- Expected load: [X requests/sec]
- Estimated latency: [Xms at scale]
- Resource consumption: [CPU/Memory impact]

**Current Code**:
```language
[Inefficient code]
```

**Optimized Solution**:
```language
[Efficient code]
```

**Expected Improvement**: [X% faster / X% less memory]

---

## High-Impact Optimizations (X)

[Same format, HIGH priority]

---

## Medium-Impact Optimizations (X)

[Same format, MEDIUM priority]

---

## Micro-Optimizations (X)

[Small improvements, LOW priority]

---

## Algorithm Complexity Analysis

| Function | Current | Optimal | Status |
|----------|---------|---------|--------|
| getUserPosts | O(n²) | O(n) | ❌ Optimize |
| searchItems | O(n log n) | O(n log n) | ✅ Optimal |
| calculateStats | O(n) | O(n) | ✅ Optimal |

---

## Database Performance

### N+1 Queries Detected (X)
- [File:line with description]

### Missing Indexes (X)
- Table: `users`, Column: `email` (used in WHERE)
- Table: `posts`, Column: `created_at` (used in ORDER BY)

### Query Optimization Opportunities (X)
- [Specific query improvements]

---

## Caching Opportunities

### High-Value Caching (X)
1. **getUserProfile()** - Called 1000x/min, data changes hourly
   - Recommendation: Redis cache, 1h TTL
   - Expected: 95% cache hit rate, 50ms → 2ms

2. **getPopularPosts()** - Expensive aggregation, changes daily
   - Recommendation: Scheduled cache warm-up
   - Expected: 99% cache hit rate, 500ms → 5ms

---

## Resource Usage Analysis

**CPU**:
- [Hot paths identified]
- [Blocking operations]

**Memory**:
- [Large allocations]
- [Potential leaks]

**I/O**:
- [Disk operations]
- [Network calls]

**Database**:
- [Connection usage]
- [Query efficiency]

---

## Scalability Assessment

**Current Capacity**: [Estimated requests/sec]
**Bottlenecks**:
1. [Primary bottleneck]
2. [Secondary bottleneck]

**Scaling Strategy**:
- Horizontal: [Can/Cannot scale horizontally, why]
- Vertical: [Resource limits]
- Recommendations: [How to improve scalability]

---

## Performance Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg Response Time | Xms | <100ms | ✅/⚠️/❌ |
| P95 Latency | Xms | <200ms | ✅/⚠️/❌ |
| P99 Latency | Xms | <500ms | ✅/⚠️/❌ |
| Memory Usage | XMB | <512MB | ✅/⚠️/❌ |
| DB Query Time | Xms | <50ms | ✅/⚠️/❌ |
| Cache Hit Rate | X% | >80% | ✅/⚠️/❌ |

---

## Prioritized Optimizations

### Must Fix (Blocking)
1. [Performance issues that will cause production problems]

### High Priority (Significant Impact)
2. [Optimizations with major performance gains]

### Medium Priority (Moderate Impact)
3. [Worthwhile optimizations]

### Low Priority (Micro-optimizations)
4. [Minor improvements]

---

## Load Testing Recommendations

**Scenarios to Test**:
1. [Specific load scenarios based on findings]
2. [Edge cases identified]

**Expected Bottlenecks**:
1. [What will fail first under load]

---

## Deployment Decision

**APPROVE FOR PRODUCTION**: ✅ YES | ⚠️ WITH MONITORING | ❌ OPTIMIZE FIRST

**Reasoning**: [Performance assessment]

**Required Actions**:
1. [Must-fix performance issues]

**Monitoring Requirements**:
1. [Specific metrics to watch]
```

## Benchmarking Guidelines

When suggesting optimizations, provide:
- Time/space complexity comparison (O(n²) → O(n))
- Estimated performance impact ("50x faster at 10k items")
- Trade-offs (e.g., "uses 2x memory but 10x faster")
- When to apply optimization (scale threshold)

## Principles

1. **Measure First**: Profile before optimizing
2. **Focus on Hot Paths**: Optimize what matters most
3. **Consider Scale**: Small data != production load
4. **Trade-offs**: Faster often means more memory
5. **Premature Optimization**: Avoid optimizing unnecessarily
6. **Read Production**: Base recommendations on expected production load
7. **Maintainability**: Don't sacrifice readability for 1% gain

## Notes

- This review identifies performance issues but is not a substitute for:
  - Actual profiling with production data
  - Load testing
  - APM (Application Performance Monitoring) tools
- Always benchmark optimizations with realistic data
- Consider the 80/20 rule: 20% of code causes 80% of performance issues
