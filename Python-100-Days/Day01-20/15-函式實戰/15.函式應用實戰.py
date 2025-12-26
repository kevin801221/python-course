#!/usr/bin/env python3
"""
從 15.函数应用实战.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import random
import string

ALL_CHARS = string.digits + string.ascii_letters


def generate_code(*, code_len=4):
    """
    生成指定長度的驗證碼
    :param code_len: 驗證碼的長度(預設4個字元)
    :return: 由大小寫英文字母和數字構成的隨機驗證碼字串
    """
    return ''.join(random.choices(ALL_CHARS, k=code_len))
# === 範例 2 ===
for _ in range(5):
    print(generate_code())
# === 範例 3 ===
for _ in range(5):
    print(generate_code(code_len=6))
# === 範例 4 ===
def is_prime(num: int) -> bool:
    """
    判斷一個正整數是不是質數
    :param num: 大於1的正整數
    :return: 如果num是質數返回True，否則返回False
    """
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
# === 範例 5 ===
def lcm(x: int, y: int) -> int:
    """求最小公倍數"""
    return x * y // gcd(x, y)


def gcd(x: int, y: int) -> int:
    """求最大公約數"""
    while y % x != 0:
        x, y = y % x, x
    return x
# === 範例 6 ===
def ptp(data):
    """極差（全距）"""
    return max(data) - min(data)


def mean(data):
    """算術平均"""
    return sum(data) / len(data)


def median(data):
    """中位數"""
    temp, size = sorted(data), len(data)
    if size % 2 != 0:
        return temp[size // 2]
    else:
        return mean(temp[size // 2 - 1:size // 2 + 1])


def var(data, ddof=1):
    """方差"""
    x_bar = mean(data)
    temp = [(num - x_bar) ** 2 for num in data]
    return sum(temp) / (len(temp) - ddof)


def std(data, ddof=1):
    """標準差"""
    return var(data, ddof) ** 0.5


def cv(data, ddof=1):
    """變異係數"""
    return std(data, ddof) / mean(data)


def describe(data):
    """輸出描述性統計資訊"""
    print(f'均值: {mean(data)}')
    print(f'中位數: {median(data)}')
    print(f'極差: {ptp(data)}')
    print(f'方差: {var(data)}')
    print(f'標準差: {std(data)}')
    print(f'變異係數: {cv(data)}')
# === 範例 7 ===
"""
雙色球隨機選號程式

Author: Kevin
Version: 1.3
"""
import random

RED_BALLS = [i for i in range(1, 34)]
BLUE_BALLS = [i for i in range(1, 17)]


def choose():
    """
    生成一組隨機號碼
    :return: 儲存隨機號碼的列表
    """
    selected_balls = random.sample(RED_BALLS, 6)
    selected_balls.sort()
    selected_balls.append(random.choice(BLUE_BALLS))
    return selected_balls


def display(balls):
    """
    格式輸出一組號碼
    :param balls: 儲存隨機號碼的列表
    """
    for ball in balls[:-1]:
        print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
    print(f'\033[034m{balls[-1]:0>2d}\033[0m')


n = int(input('生成幾注號碼: '))
for _ in range(n):
    display(choose())
