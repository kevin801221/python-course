#!/usr/bin/env python3
"""
從 71.NumPy的应用-4.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
u = np.array([5, 1, 3])
m1 = np.array([4, 5, 1])
m2 = np.array([5, 1, 5])
print(np.dot(u, m1) / (np.linalg.norm(u) * np.linalg.norm(m1)))  # 0.7302967433402214
print(np.dot(u, m2) / (np.linalg.norm(u) * np.linalg.norm(m2)))  # 0.9704311900788593
# === 範例 2 ===
print(np.cross(u, m1))  # [-14   7  21]
print(np.cross(m1, u))  # [ 14  -7 -21]
# === 範例 3 ===
p1 = np.poly1d([3, 2, 1])
p2 = np.poly1d([1, 2, 3])
print(p1)
print(p2)
# === 範例 4 ===
print(p1.coefficients)
print(p2.coeffs)
# === 範例 5 ===
print(p1 + p2)
print(p1 * p2)
# === 範例 6 ===
print(p1(3))
print(p2(3))
# === 範例 7 ===
print(p1.deriv())
print(p1.integ())
# === 範例 8 ===
p3 = np.poly1d([1, 3, 2])
print(p3.roots)
# === 範例 9 ===
from numpy.polynomial import Polynomial

p3 = Polynomial((2, 3, 1))
print(p3)           # 輸出多項式
print(p3(3))        # 令x=3，計算多項式的值
print(p3.roots())   # 計算多項式的根
print(p3.degree())  # 獲得多項式的次數
print(p3.deriv())   # 求導
print(p3.integ())   # 求不定積分
# === 範例 10 ===
x = np.array([
    25000, 15850, 15500, 20500, 22000, 20010, 26050, 12500, 18500, 27300,
    15000,  8300, 23320,  5250,  5800,  9100,  4800, 16000, 28500, 32000,
    31300, 10800,  6750,  6020, 13300, 30020,  3200, 17300,  8835,  3500
])
y = np.array([
    2599, 1400, 1120, 2560, 1900, 1200, 2320,  800, 1650, 2200,
     980,  580, 1885,  600,  400,  800,  420, 1380, 1980, 3999,
    3800,  725,  520,  420, 1200, 4020,  350, 1500,  560,  500
])
# === 範例 11 ===
import matplotlib.pyplot as plt

plt.figure(dpi=120)
plt.scatter(x, y, color='blue')
plt.show()
# === 範例 12 ===
np.corrcoef(x, y)
# === 範例 13 ===
from numpy.polynomial import Polynomial

Polynomial.fit(x, y, deg=1).convert().coef
# === 範例 14 ===
import matplotlib.pyplot as plt

plt.scatter(x, y, color='blue')
plt.scatter(x, 0.110333716 * x - 294.883437, color='red')
plt.plot(x, 0.110333716 * x - 294.883437, color='darkcyan')
plt.show()
