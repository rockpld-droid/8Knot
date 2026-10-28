## 2024-10-28 - [Pandas DataFrame Row-by-Row Optimization]
**Learning:** Avoid using `pandas.DataFrame.apply(axis=1)` for row-by-row operations involving calculations over arrays, especially on time-series graphs like issues/PRs over time. This approach has O(n * m) time complexity.
**Action:** Replace `apply(axis=1)` with vectorized NumPy operations, such as `np.searchsorted`, to reduce computational complexity to O(m log n) and significantly improve rendering times for visualizations.
