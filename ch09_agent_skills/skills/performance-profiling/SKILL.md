---
name: performance-profiling
description: Profile and optimize application performance. Use when asked to improve speed, reduce latency, fix memory leaks, find bottlenecks, or optimize a slow function or endpoint.
license: MIT
compatibility: Requires python 3.10+ or node 18+
---

## Overview

You do not optimize what you have not measured. Every performance investigation starts with a profiler, not a hypothesis.

## Process

1. **Establish a baseline.** Before changing anything, measure the current performance:
   - For a function: time it with actual production-representative data
   - For an endpoint: measure p50, p95, p99 latency under realistic load
   - For memory: record heap size at start, peak, and end of operation

   ```python
   import cProfile, pstats, io

   pr = cProfile.Profile()
   pr.enable()
   result = slow_function(data)
   pr.disable()

   s = io.StringIO()
   ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
   ps.print_stats(20)  # Top 20 by cumulative time
   print(s.getvalue())
   ```

2. **Read the profiler output.** Identify the top 3 functions by cumulative time. Do not optimize anything that is NOT in the top 3 — this is Amdahl's Law in practice.

3. **Form ONE hypothesis** for why the top bottleneck is slow. Common causes, in order of frequency:
   - N+1 query (calling the database once per item in a loop)
   - Missing index on a frequently queried column
   - Serialization of large objects in a hot path
   - Synchronous I/O blocking an async event loop
   - Unnecessary repeated computation (missing cache)

4. **Apply ONE change.** The smallest possible change that addresses the hypothesis. Do not refactor the entire module.

5. **Measure again.** Compare against the baseline. Report the improvement as a percentage.

6. **Repeat.** If there is still a performance gap, return to step 2 with the updated profile.

## Common Patterns

**N+1 query fix:**
```python
# Before: queries once per user
for user in users:
    user.orders = db.query(f"SELECT * FROM orders WHERE user_id={user.id}")

# After: one query for all users
user_ids = [u.id for u in users]
orders = db.query("SELECT * FROM orders WHERE user_id = ANY(%s)", [user_ids])
orders_by_user = defaultdict(list)
for o in orders: orders_by_user[o.user_id].append(o)
for user in users: user.orders = orders_by_user[user.id]
```

**Caching a pure function:**
```python
from functools import lru_cache

@lru_cache(maxsize=512)
def expensive_computation(input_id: int) -> dict:
    ...
```

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "I know what the bottleneck is without profiling" | You don't. Everyone thinks they know. Profile first, always. |
| "Let me optimize the whole module while I'm here" | Scope creep disguised as diligence. Fix the top bottleneck, measure, then decide if more work is needed. |
| "It's fast enough on my machine" | Production data is 100x larger. Profile with production-scale data. |

## Verification

- [ ] Baseline performance was measured before any change
- [ ] Profiler output was read (not guessed)
- [ ] Only the top bottleneck was targeted
- [ ] Performance was measured after the change and improvement percentage was reported
