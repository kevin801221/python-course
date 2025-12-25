#!/usr/bin/env python3
"""
從 81.浅谈机器学习.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
# 每月收入
x = [9558, 8835, 9313, 14990, 5564, 11227, 11806, 10242, 11999, 11630,
     6906, 13850, 7483, 8090, 9465, 9938, 11414, 3200, 10731, 19880,
     15500, 10343, 11100, 10020, 7587, 6120, 5386, 12038, 13360, 10885,
     17010, 9247, 13050, 6691, 7890, 9070, 16899, 8975, 8650, 9100,
     10990, 9184, 4811, 14890, 11313, 12547, 8300, 12400, 9853, 12890]
# 每月網購支出
y = [3171, 2183, 3091, 5928, 182, 4373, 5297, 3788, 5282, 4166,
     1674, 5045, 1617, 1707, 3096, 3407, 4674, 361, 3599, 6584,
     6356, 3859, 4519, 3352, 1634, 1032, 1106, 4951, 5309, 3800,
     5672, 2901, 5439, 1478, 1424, 2777, 5682, 2554, 2117, 2845,
     3867, 2962,  882, 5435, 4174, 4948, 2376, 4987, 3329, 5002]
# === 範例 2 ===
import numpy as np

np.corrcoef(x, y)
# === 範例 3 ===
from scipy import stats

stats.pearsonr(x, y)
# === 範例 4 ===
sample_data = {key: value for key, value in zip(x, y)}
# === 範例 5 ===
import heapq
import statistics


def predict_by_knn(history_data, param_in, k=5):
    """用kNN演算法做預測
    :param history_data: 歷史資料
    :param param_in: 模型的輸入
    :param k: 鄰居數量（預設值為5）
    :return: 模型的輸出（預測值）
    """
    neighbors = heapq.nsmallest(k, history_data, key=lambda x: (x - param_in) ** 2)
    return statistics.mean([history_data[neighbor] for neighbor in neighbors])
# === 範例 6 ===
incomes = [1800, 3500, 5200, 6600, 13400, 17800, 20000, 30000]
for income in incomes:
    print(f'月收入: {income:>5d}元, 月網購支出: {predict_by_knn(sample_data, income):>6.1f}元')
# === 範例 7 ===
import statistics


def get_loss(X_, y_, a_, b_):
    """損失函式
    :param X_: 迴歸模型的自變數
    :param y_: 迴歸模型的因變數
    :param a_: 迴歸模型的斜率
    :param b_: 迴歸模型的截距
    :return: MSE（均方誤差）
    """
    y_hat = [a_ * x + b_ for x in X_]
    return statistics.mean([(v1 - v2) ** 2 for v1, v2 in zip(y_, y_hat)])
# === 範例 8 ===
import random

# 先將最小損失定義為一個很大的值
min_loss, a, b = 1e12, 0, 0

for _ in range(100000):
    # 透過產生隨機數的方式獲得斜率和截距
    _a, _b = random.random(), random.random() * 4000 - 2000
    # 帶入損失函式計算迴歸模型的MSE
    curr_loss = get_loss(x, y, _a, _b)
    if curr_loss < min_loss:
        # 找到更小的MSE就記為最小損失
        min_loss = curr_loss
        # 記錄下當前最小損失對應的a和b
        a, b = _a, _b

print(f'MSE = {min_loss}')
print(f'{a = }, {b = }')
# === 範例 9 ===
import numpy as np

x_bar, y_bar = np.mean(x), np.mean(y)
a = np.dot((x - x_bar), (y - y_bar)) / np.sum((x - x_bar) ** 2)
b = y_bar - a * x_bar
print(f'{a = }, {b = }')
# === 範例 10 ===
a, b = np.polyfit(x, y, deg=1)
print(f'{a = }, {b = }')
# === 範例 11 ===
from numpy.polynomial import Polynomial

b, a = Polynomial.fit(x, y, deg=1).convert().coef
print(f'{a = }, {b = }')
