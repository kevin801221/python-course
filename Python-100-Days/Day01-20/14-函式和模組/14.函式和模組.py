#!/usr/bin/env python3
"""
從 14.函数和模块.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
"""
輸入m和n，計算組合數C(m,n)的值

Version: 1.0
Author: Kevin
"""

m = int(input('m = '))
n = int(input('n = '))
# 計算m的階乘
fm = 1
for num in range(1, m + 1):
    fm *= num
# 計算n的階乘
fn = 1
for num in range(1, n + 1):
    fn *= num
# 計算m-n的階乘
fk = 1
for num in range(1, m - n + 1):
    fk *= num
# 計算C(M,N)的值
print(fm // fn // fk)
# === 範例 2 ===
"""
輸入m和n，計算組合數C(m,n)的值

Version: 1.1
Author: Kevin
"""


# 透過關鍵字def定義求階乘的函式
# 自變數（引數）num是一個非負整數
# 因變數（返回值）是num的階乘
def fac(num):
    result = 1
    for n in range(2, num + 1):
        result *= n
    return result


m = int(input('m = '))
n = int(input('n = '))
# 計算階乘的時候不需要寫重複的程式碼而是直接呼叫函式
# 呼叫函式的語法是在函式名後面跟上圓括號並傳入引數
print(fac(m) // fac(n) // fac(m - n))
# === 範例 3 ===
"""
輸入m和n，計算組合數C(m,n)的值

Version: 1.2
Author: Kevin
"""
from math import factorial

m = int(input('m = '))
n = int(input('n = '))
print(factorial(m) // factorial(n) // factorial(m - n))
# === 範例 4 ===
"""
輸入m和n，計算組合數C(m,n)的值

Version: 1.3
Author: Kevin
"""
from math import factorial as f

m = int(input('m = '))
n = int(input('n = '))
print(f(m) // f(n) // f(m - n))
# === 範例 5 ===
def make_judgement(a, b, c):
    """判斷三條邊的長度能否構成三角形"""
    return a + b > c and b + c > a and a + c > b
# === 範例 6 ===
print(make_judgement(1, 2, 3))  # False
print(make_judgement(4, 5, 6))  # True
# === 範例 7 ===
print(make_judgement(b=2, c=3, a=1))  # False
print(make_judgement(c=6, b=4, a=5))  # True
# === 範例 8 ===
# /前面的引數是強制位置引數
def make_judgement(a, b, c, /):
    """判斷三條邊的長度能否構成三角形"""
    return a + b > c and b + c > a and a + c > b


# 下面的程式碼會產生TypeError錯誤，錯誤資訊提示“強制位置引數是不允許給出引數名的”
# TypeError: make_judgement() got some positional-only arguments passed as keyword arguments
# print(make_judgement(b=2, c=3, a=1))
# === 範例 9 ===
# *後面的引數是命名關鍵字引數
def make_judgement(*, a, b, c):
    """判斷三條邊的長度能否構成三角形"""
    return a + b > c and b + c > a and a + c > b


# 下面的程式碼會產生TypeError錯誤，錯誤資訊提示“函式沒有位置引數但卻給了3個位置引數”
# TypeError: make_judgement() takes 0 positional arguments but 3 were given
# print(make_judgement(1, 2, 3))
# === 範例 10 ===
from random import randrange


# 定義搖色子的函式
# 函式的自變數（引數）n表示色子的個數，預設值為2
# 函式的因變數（返回值）表示搖n顆色子得到的點數
def roll_dice(n=2):
    total = 0
    for _ in range(n):
        total += randrange(1, 7)
    return total


# 如果沒有指定引數，那麼n使用預設值2，表示搖兩顆色子
print(roll_dice())
# 傳入引數3，變數n被賦值為3，表示搖三顆色子獲得點數
print(roll_dice(3))
# === 範例 11 ===
def add(a=0, b=0, c=0):
    """三個數相加求和"""
    return a + b + c


# 呼叫add函式，沒有傳入引數，那麼a、b、c都使用預設值0
print(add())         # 0
# 呼叫add函式，傳入一個引數，該引數賦值給變數a, 變數b和c使用預設值0
print(add(1))        # 1
# 呼叫add函式，傳入兩個引數，分別賦值給變數a和b，變數c使用預設值0
print(add(1, 2))     # 3
# 呼叫add函式，傳入三個引數，分別賦值給a、b、c三個變數
print(add(1, 2, 3))  # 6
# === 範例 12 ===
# 用星號表示式來表示args可以接收0個或任意多個引數
# 呼叫函式時傳入的n個引數會組裝成一個n元組賦給args
# 如果一個引數都沒有傳入，那麼args會是一個空元組
def add(*args):
    total = 0
    # 對儲存可變引數的元組進行迴圈遍歷
    for val in args:
        # 對引數進行了型別檢查（數值型的才能求和）
        if type(val) in (int, float):
            total += val
    return total


# 在呼叫add函式時可以傳入0個或任意多個引數
print(add())         # 0
print(add(1))        # 1
print(add(1, 2, 3))  # 6
print(add(1, 2, 'hello', 3.45, 6))  # 12.45
# === 範例 13 ===
# 引數列表中的**kwargs可以接收0個或任意多個關鍵字引數
# 呼叫函式時傳入的關鍵字引數會組裝成一個字典（引數名是字典中的鍵，引數值是字典中的值）
# 如果一個關鍵字引數都沒有傳入，那麼kwargs會是一個空字典
def foo(*args, **kwargs):
    print(args)
    print(kwargs)


foo(3, 2.1, True, name='Kevin', age=43, gpa=4.95)
# === 範例 14 ===
def foo():
    print('hello, world!')


def foo():
    print('goodbye, world!')

    
foo()  # 大家猜猜呼叫foo函式會輸出什麼
# === 範例 15 ===
def foo():
    print('hello, world!')
# === 範例 16 ===
def foo():
    print('goodbye, world!')
# === 範例 17 ===
import module1
import module2

# 用“模組名.函式名”的方式（完全限定名）呼叫函式，
module1.foo()  # hello, world!
module2.foo()  # goodbye, world!
# === 範例 18 ===
import module1 as m1
import module2 as m2

m1.foo()  # hello, world!
m2.foo()  # goodbye, world!
# === 範例 19 ===
from module1 import foo

foo()  # hello, world!

from module2 import foo

foo()  # goodbye, world!
# === 範例 20 ===
from module1 import foo
from module2 import foo

foo()  # goodbye, world!
# === 範例 21 ===
from module1 import foo as f1
from module2 import foo as f2

f1()  # hello, world!
f2()  # goodbye, world!
