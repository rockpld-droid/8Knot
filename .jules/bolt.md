## 2024-11-07 - Vectorize cumulative counts over time
**Learning:** Using `df.apply(lambda row: func(df, row.Date), axis=1)` to compute active items (like open issues or PRs) over a time series results in $O(N \times M)$ complexity and is very slow for large datasets.
**Action:** When calculating "active" counts over time (e.g. cumulative created minus cumulative closed), sort the timestamp arrays and use `numpy.searchsorted` for binary search, reducing complexity to $O(M \log M + N \log M)$. This resulted in a massive speedup (~300x in local benchmarks).
