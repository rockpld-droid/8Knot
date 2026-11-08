
## 2024-05-24 - Replace Pandas row-wise apply with vectorized numpy searchsorted for time series active counts
**Learning:** Using `pandas.DataFrame.apply()` with `axis=1` to calculate the number of "open" or active items (e.g. issues, PRs) for a given date is extremely slow because it evaluates row-by-row on dataframes that can be massive. Counting active issues requires checking properties of multiple rows at each date, which causes O(N*M) behavior if N is dates and M is total issues.
**Action:** When calculating active items over a time series, use vectorized `numpy.searchsorted` on sorted arrays of creation times and closing times. `active = created_counts - closed_counts`. This reduces computation time from seconds to milliseconds.
