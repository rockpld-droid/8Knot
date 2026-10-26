## 2024-05-14 - [Vectorized time-series cumulative counts vs row-by-row apply()]
**Learning:** Using `pandas.DataFrame.apply()` with `axis=1` to filter a dataframe for cumulative rolling counts (e.g., getting the number of open issues/PRs for each date) is $O(N \cdot M)$ and can cause massive performance bottlenecks.
**Action:** Always prefer `numpy.searchsorted()` for cumulative timeseries lookups by comparing sorted arrays of "opened" and "closed" timestamps against an array of query dates. This reduces complexity to $O((N+M) \log(N))$ and executes practically instantly.
