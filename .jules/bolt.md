## 2025-02-18 - Avoid defining @lru_cache functions inside methods
**Learning:** Defining a function with `@lru_cache` inside a class method or hot loop recreates the cache on every method call, negating its performance benefits and adding overhead.
**Action:** Always define functions that use `@lru_cache` at the module level or as statically defined methods, rather than as inner functions inside loops or methods.
