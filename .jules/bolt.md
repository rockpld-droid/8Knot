## 2023-10-27 - Vectorizing Time-Series Cumulative Counts
**Learning:** In pandas, iterating over a date range using `df.apply(..., axis=1)` to slice `df` dynamically to count open issues/PRs (where `created_at <= date` and `closed_at > date`) takes O(N*M) and is a massive bottleneck.
**Action:** Replace dynamic boolean slicing with `numpy.searchsorted` on sorted `created_at` and `closed_at` arrays to calculate cumulative differences. This reduces complexity from O(N*M) to O(M log N) and speeds up execution significantly (measured local scratchpad test from ~1.0s to ~0.01s).
