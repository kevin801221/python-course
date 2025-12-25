#!/usr/bin/env python3
"""
從 69.NumPy的应用-2.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from scipy import stats

print(np.mean(array1))                # 算術平均值
print(stats.gmean(array1))            # 幾何平均值
print(stats.hmean(array1))            # 調和平均值
print(stats.tmean(array1, [10, 90]))  # 去尾平均值
print(stats.variation(array1))        # 變異係數
print(stats.skew(array1))             # 偏態係數
print(stats.kurtosis(array1))         # 峰度係數
