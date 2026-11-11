## 2024-05-15 - [Pandas Apply Bottleneck in Time Series Iteration]
**Learning:** Using `pandas.DataFrame.apply(..., axis=1)` to compute values by filtering a dataset per row (e.g., finding all open issues for a specific date) results in O(N*M) complexity. This is extremely slow for large datasets in 8Knot.
**Action:** Replace such loops with vectorized `numpy.searchsorted` operations. By sorting timestamps (`created_at`, `closed_at`) and finding insertion points for the time series dates, the complexity is reduced to O((N+M) log M) which is orders of magnitude faster.

## 2024-03-20 - [Optimize dataframe row-by-row apply]
**Learning:** Using `pandas.DataFrame.apply()` with `axis=1` for date interval counting is extremely slow (O(M*N)) because it iterates Python lambda functions row-by-row and filters the main dataframe for each date. This pattern occurs in visualization files like `issues_over_time.py` and `pr_over_time.py` when computing the number of open issues/PRs for each point in time.
**Action:** When computing counts over time in Pandas (e.g., number of open items at time T), prefer `numpy.searchsorted` instead of `.apply(axis=1)` with dataframe filtering. Sort the `created_at` and `closed_at` arrays once, then use `np.searchsorted` to find the number of created items minus the number of closed items up to each time `T`.

## 2024-05-16 - [Pandas Apply Bottleneck in String Matching]
**Learning:** Using `pandas.DataFrame.apply(..., axis=1)` to perform fuzzy string matching across rows (comparing each row's string to a list of strings) is incredibly slow and results in O(N^2) complexity because of row-by-row iteration in Python instead of using optimized C++ code paths.
**Action:** Replace `df.apply(lambda row: fuzzy_match(..., row["string_col"]), axis=1)` with vectorized or highly optimized batched equivalents. For `rapidfuzz` specifically, extract the list of strings and use `rapidfuzz.process.extract(name, list_of_names)` in a loop, which executes matching significantly faster by leveraging optimized internal loops.
