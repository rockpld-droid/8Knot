## 2024-05-15 - [Pandas Apply Bottleneck in Time Series Iteration]
**Learning:** Using `pandas.DataFrame.apply(..., axis=1)` to compute values by filtering a dataset per row (e.g., finding all open issues for a specific date) results in O(N*M) complexity. This is extremely slow for large datasets in 8Knot.
**Action:** Replace such loops with vectorized `numpy.searchsorted` operations. By sorting timestamps (`created_at`, `closed_at`) and finding insertion points for the time series dates, the complexity is reduced to O((N+M) log M) which is orders of magnitude faster.
