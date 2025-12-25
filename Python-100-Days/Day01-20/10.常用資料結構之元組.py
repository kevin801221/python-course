#!/usr/bin/env python3
"""
從 10.常用数据结构之元组.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
# 定義一個三元組
t1 = (35, 12, 98)
# 定義一個四元組
t2 = ('Kevin', 45, True, '四川成都')

# 檢視變數的型別
print(type(t1))  # <class 'tuple'>
print(type(t2))  # <class 'tuple'>

# 檢視元組中元素的數量
print(len(t1))  # 3
print(len(t2))  # 4

# 索引運算
print(t1[0])    # 35
print(t1[2])    # 98
print(t2[-1])   # 四川成都

# 切片運算
print(t2[:2])   # ('Kevin', 43)
print(t2[::3])  # ('Kevin', '四川成都')

# 迴圈遍歷元組中的元素
for elem in t1:
    print(elem)

# 成員運算
print(12 in t1)         # True
print(99 in t1)         # False
print('Hao' not in t2)  # True

# 拼接運算
t3 = t1 + t2
print(t3)  # (35, 12, 98, 'Kevin', 43, True, '四川成都')

# 比較運算
print(t1 == t3)            # False
print(t1 >= t3)            # False
print(t1 <= (35, 11, 99))  # False
# === 範例 2 ===
a = ()
print(type(a))  # <class 'tuple'>
b = ('hello')
print(type(b))  # <class 'str'>
c = (100)
print(type(c))  # <class 'int'>
d = ('hello', )
print(type(d))  # <class 'tuple'>
e = (100, )
print(type(e))  # <class 'tuple'>
# === 範例 3 ===
# 打包操作
a = 1, 10, 100
print(type(a))  # <class 'tuple'>
print(a)        # (1, 10, 100)
# 解包操作
i, j, k = a
print(i, j, k)  # 1 10 100
# === 範例 4 ===
a = 1, 10, 100, 1000
# i, j, k = a             # ValueError: too many values to unpack (expected 3)
# i, j, k, l, m, n = a    # ValueError: not enough values to unpack (expected 6, got 4)
# === 範例 5 ===
a = 1, 10, 100, 1000
i, j, *k = a
print(i, j, k)        # 1 10 [100, 1000]
i, *j, k = a
print(i, j, k)        # 1 [10, 100] 1000
*i, j, k = a
print(i, j, k)        # [1, 10] 100 1000
*i, j = a
print(i, j)           # [1, 10, 100] 1000
i, *j = a
print(i, j)           # 1 [10, 100, 1000]
i, j, k, *l = a
print(i, j, k, l)     # 1 10 100 [1000]
i, j, k, l, *m = a
print(i, j, k, l, m)  # 1 10 100 1000 []
# === 範例 6 ===
a, b, *c = range(1, 10)
print(a, b, c)
a, b, c = [1, 10, 100]
print(a, b, c)
a, *b, c = 'hello'
print(a, b, c)
# === 範例 7 ===
a, b = b, a
# === 範例 8 ===
a, b, c = b, c, a
# === 範例 9 ===
import timeit
   
   print('%.3f 秒' % timeit.timeit('[1, 2, 3, 4, 5, 6, 7, 8, 9]', number=10000000))
   print('%.3f 秒' % timeit.timeit('(1, 2, 3, 4, 5, 6, 7, 8, 9)', number=10000000))
# === 範例 10 ===
infos = ('Kevin', 43, True, '四川成都')
# 將元組轉換成列表
print(list(infos))  # ['Kevin', 43, True, '四川成都']

frts = ['apple', 'banana', 'orange']
# 將列表轉換成元組
print(tuple(frts))  # ('apple', 'banana', 'orange')
