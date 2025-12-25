#!/usr/bin/env python3
"""
從 16.函数使用进阶.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
def calc(*args, **kwargs):
    items = list(args) + list(kwargs.values())
    result = 0
    for item in items:
        if type(item) in (int, float):
            result += item
    return result
# === 範例 2 ===
def calc(init_value, op_func, *args, **kwargs):
    items = list(args) + list(kwargs.values())
    result = init_value
    for item in items:
        if type(item) in (int, float):
            result = op_func(result, item)
    return result
# === 範例 3 ===
def add(x, y):
    return x + y


def mul(x, y):
    return x * y
# === 範例 4 ===
print(calc(0, add, 1, 2, 3, 4, 5))  # 15
# === 範例 5 ===
print(calc(1, mul, 1, 2, 3, 4, 5))  # 120
# === 範例 6 ===
import operator

print(calc(0, operator.add, 1, 2, 3, 4, 5))  # 15
print(calc(1, operator.mul, 1, 2, 3, 4, 5))  # 120
# === 範例 7 ===
def is_even(num):
    """判斷num是不是偶數"""
    return num % 2 == 0


def square(num):
    """求平方"""
    return num ** 2


old_nums = [35, 12, 8, 99, 60, 52]
new_nums = list(map(square, filter(is_even, old_nums)))
print(new_nums)  # [144, 64, 3600, 2704]
# === 範例 8 ===
old_nums = [35, 12, 8, 99, 60, 52]
new_nums = [num ** 2 for num in old_nums if num % 2 == 0]
print(new_nums)  # [144, 64, 3600, 2704]
# === 範例 9 ===
old_strings = ['in', 'apple', 'zoo', 'waxberry', 'pear']
new_strings = sorted(old_strings)
print(new_strings)  # ['apple', 'in', 'pear', waxberry', 'zoo']
# === 範例 10 ===
old_strings = ['in', 'apple', 'zoo', 'waxberry', 'pear']
new_strings = sorted(old_strings, key=len)
print(new_strings)  # ['in', 'zoo', 'pear', 'apple', 'waxberry']
# === 範例 11 ===
old_nums = [35, 12, 8, 99, 60, 52]
new_nums = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, old_nums)))
print(new_nums)  # [144, 64, 3600, 2704]
# === 範例 12 ===
import functools
import operator

# 用一行程式碼實現計算階乘的函式
fac = lambda n: functools.reduce(operator.mul, range(2, n + 1), 1)

# 用一行程式碼實現判斷素數的函式
is_prime = lambda x: all(map(lambda f: x % f, range(2, int(x ** 0.5) + 1)))

# 呼叫Lambda函式
print(fac(6))        # 720
print(is_prime(37))  # True
# === 範例 13 ===
import functools

int2 = functools.partial(int, base=2)
int8 = functools.partial(int, base=8)
int16 = functools.partial(int, base=16)

print(int('1001'))    # 1001

print(int2('1001'))   # 9
print(int8('1001'))   # 513
print(int16('1001'))  # 4097
