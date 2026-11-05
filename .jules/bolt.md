
## 2024-05-24 - Replace Pandas row-wise apply with vectorized numpy searchsorted
**Learning:** `pandas.DataFrame.apply()` with `axis=1` can cause massive performance bottlenecks when performing row-by-row comparisons against entire dataframe columns, creating $O(N \times M)$ complexity.
**Action:** Replace `df.apply` for counting items across time intervals with vectorized `numpy.searchsorted()` on sorted arrays, reducing complexity to $O(N \log M)$ and executing orders of magnitude faster.
