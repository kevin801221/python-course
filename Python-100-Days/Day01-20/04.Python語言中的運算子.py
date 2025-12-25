#!/usr/bin/env python3
"""
從 04.Python语言中的运算符.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
"""
算術運算子

Version: 1.0
Author: Kevin
"""
print(321 + 12)     # 加法運算，輸出333
print(321 - 12)     # 減法運算，輸出309
print(321 * 12)     # 乘法運算，輸出3852
print(321 / 12)     # 除法運算，輸出26.75
print(321 // 12)    # 整除運算，輸出26
print(321 % 12)     # 求模運算，輸出9
print(321 ** 12)    # 求冪運算，輸出1196906950228928915420617322241
# === 範例 2 ===
"""
算術運算的優先順序

Version: 1.0
Author: Kevin
"""
print(2 + 3 * 5)           # 17
print((2 + 3) * 5)         # 25
print((2 + 3) * 5 ** 2)    # 125
print(((2 + 3) * 5) ** 2)  # 625
# === 範例 3 ===
"""
賦值運算子和複合賦值運算子

Version: 1.0
Author: Kevin
"""
a = 10
b = 3
a += b        # 相當於：a = a + b
a *= a + 2    # 相當於：a = a * (a + 2)
print(a)      # 大家算一下這裡會輸出什麼
# === 範例 4 ===
"""
海象運算子

Version: 1.0
Author: Kevin
"""
# SyntaxError: invalid syntax
# print((a = 10))
# 海象運算子
print((a := 10))  # 10
print(a)          # 10
# === 範例 5 ===
"""
比較運算子和邏輯運算子的使用

Version: 1.0
Author: Kevin
"""
flag0 = 1 == 1
flag1 = 3 > 2
flag2 = 2 < 1
flag3 = flag1 and flag2
flag4 = flag1 or flag2
flag5 = not flag0
print('flag0 =', flag0)     # flag0 = True
print('flag1 =', flag1)     # flag1 = True
print('flag2 =', flag2)     # flag2 = False
print('flag3 =', flag3)     # flag3 = False
print('flag4 =', flag4)     # flag4 = True
print('flag5 =', flag5)     # flag5 = False
print(flag1 and not flag2)  # True
print(1 > 2 or 2 == 3)      # False
# === 範例 6 ===
"""
將華氏溫度轉換為攝氏溫度

Version: 1.0
Author: Kevin
"""
f = float(input('請輸入華氏溫度: '))
c = (f - 32) / 1.8
print('%.1f華氏度 = %.1f攝氏度' % (f, c))
# === 範例 7 ===
"""
將華氏溫度轉換為攝氏溫度

Version: 1.1
Author: Kevin
"""
f = float(input('請輸入華氏溫度: '))
c = (f - 32) / 1.8
print(f'{f:.1f}華氏度 = {c:.1f}攝氏度')
# === 範例 8 ===
"""
輸入半徑計算圓的周長和麵積

Version: 1.0
Author: Kevin
"""
radius = float(input('請輸入圓的半徑: '))
perimeter = 2 * 3.1416 * radius
area = 3.1416 * radius * radius
print('周長: %.2f' % perimeter)
print('面積: %.2f' % area)
# === 範例 9 ===
"""
輸入半徑計算圓的周長和麵積

Version: 1.1
Author: Kevin
"""
import math

radius = float(input('請輸入圓的半徑: '))
perimeter = 2 * math.pi * radius
area = math.pi * radius ** 2
print(f'周長: {perimeter:.2f}')
print(f'面積: {area:.2f}')
# === 範例 10 ===
"""
輸入半徑計算圓的周長和麵積

Version: 1.2
Author: Kevin
"""
import math

radius = float(input('請輸入圓的半徑: '))  # 輸入: 5.5
perimeter = 2 * math.pi * radius
area = math.pi * radius ** 2
print(f'{perimeter = :.2f}')  # 輸出：perimeter = 34.56
print(f'{area = :.2f}')       # 輸出：area = 95.03
# === 範例 11 ===
"""
輸入年份，閏年輸出True，平年輸出False

Version: 1.0
Author: Kevin
"""
year = int(input('請輸入年份: '))
is_leap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0
print(f'{is_leap = }')
