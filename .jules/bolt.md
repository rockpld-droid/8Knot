## 2024-11-01 - Vectorize Cumulative Time Series Counts
**Learning:** Using `pandas.DataFrame.apply(..., axis=1)` to filter the DataFrame repeatedly for each date to compute running totals (e.g., number of open PRs) scales poorly (O(N*M)).
**Action:** Use vectorized operations like `numpy.searchsorted` on sorted arrays instead. By sorting the start/end date columns and using `np.searchsorted` to count occurrences up to each date, the time complexity becomes O((N+M) log N). This technique dramatically reduced the time taken from ~1.87s to ~0.003s for 10k rows.
