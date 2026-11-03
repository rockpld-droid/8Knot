## 2024-05-14 - [Vectorized Overlap Counting]
**Learning:** Using `pandas.DataFrame.apply()` with `axis=1` to count overlapping intervals (e.g. open issues on a given day by checking created <= date < closed) is O(N*M) and causes severe performance bottlenecks.
**Action:** Replace row-by-row apply operations with vectorized `numpy.searchsorted`. By sorting the start and end dates and using `searchsorted`, the time complexity reduces to O((N+M) log N), typically resulting in ~1000x speedup for moderate data sizes.
