## 2024-05-24 - Optimize DataFrame apply with axis=1
**Learning:** Using `apply(axis=1)` in Pandas is very slow. It is often used to calculate 'open' issues/PRs over time for each day, resulting in O(N*M) where N is dates and M is rows in the dataframe. Vectorized operations using numpy's `searchsorted` and array math broadcasted operations can replace these expensive `apply(axis=1)` calls.
**Action:** Replace `apply(axis=1)` with numpy vectorized operations or pandas built-in aggregations to improve time-series calculation performance.
