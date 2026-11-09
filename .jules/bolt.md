## 2024-05-18 - [Replaced apply with numpy searchsorted in pandas for row-by-row time window functions]
**Learning:** Using `pandas.DataFrame.apply()` with `axis=1` to count objects inside an expanding/sliding time window (e.g., finding open issues or open PRs at each date) is extremely slow (O(n * m)).
**Action:** Always prefer `numpy.searchsorted` for calculating active/open counts over time by comparing the sorted array of creation times and closing times.
