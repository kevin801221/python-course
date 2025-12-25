#!/usr/bin/env python3
"""
從 72.深入浅出pandas-1.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
ser1 += 10
ser1
# === 範例 2 ===
ser1 + ser2
# === 範例 3 ===
print(ser2.dtype)                    # 資料型別
print(ser2.hasnans)                  # 有沒有空值
print(ser2.index)                    # 索引
print(ser2.values)                   # 值
print(ser2.is_monotonic_increasing)  # 是否單調遞增
print(ser2.is_unique)                # 是否每個值都獨一無二
# === 範例 4 ===
ser3.mode()
