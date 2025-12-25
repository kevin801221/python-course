#!/usr/bin/env python3
"""
從 77.深入浅出pandas-6.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
ser.index = index.reorder_categories(['香蕉', '桃子', '蘋果'])
ser.groupby(level=0).sum()
# === 範例 2 ===
tuples = [(1, 'red'), (1, 'blue'), (2, 'red'), (2, 'blue')]
index = pd.MultiIndex.from_tuples(tuples, names=['no', 'color'])
index
# === 範例 3 ===
arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue']]
index = pd.MultiIndex.from_arrays(arrays, names=['no', 'color'])
index
# === 範例 4 ===
sales_data = np.random.randint(1, 100, 4)
ser = pd.Series(data=sales_data, index=index)
ser
# === 範例 5 ===
ser.groupby('no').sum()
# === 範例 6 ===
ser.groupby(level=1).sum()
# === 範例 7 ===
index = pd.interval_range(start=0, end=5)
index
# === 範例 8 ===
index.contains(1.5)
# === 範例 9 ===
index.overlaps(pd.Interval(1.5, 3.5))
# === 範例 10 ===
index = pd.interval_range(start=0, end=5, closed='left')
index
# === 範例 11 ===
index = pd.interval_range(start=pd.Timestamp('2022-01-01'), end=pd.Timestamp('2022-01-04'), closed='both')
index
# === 範例 12 ===
baidu_df.resample('1M').agg(['mean', 'std'])
