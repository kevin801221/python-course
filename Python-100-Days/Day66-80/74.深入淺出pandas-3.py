#!/usr/bin/env python3
"""
從 74.深入浅出pandas-3.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
all_emp_df.drop_duplicates(['ename', 'job'], inplace=True)
