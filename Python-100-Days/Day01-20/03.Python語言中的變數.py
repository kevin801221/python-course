#!/usr/bin/env python3
"""
從 03.Python语言中的变量.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
print(0b100)  # 二進位制整數
print(0o100)  # 八進位制整數
print(100)    # 十進位制整數
print(0x100)  # 十六進位制整數
# === 範例 2 ===
print(123.456)    # 數學寫法
print(1.23456e2)  # 科學計數法
# === 範例 3 ===
"""
使用變數儲存資料並進行加減乘除運算

Version: 1.0
Author: Kevin
"""
a = 45        # 定義變數a，賦值45
b = 12        # 定義變數b，賦值12
print(a, b)   # 45 12
print(a + b)  # 57
print(a - b)  # 33
print(a * b)  # 540
print(a / b)  # 3.75
# === 範例 4 ===
"""
使用type函式檢查變數的型別

Version: 1.0
Author: Kevin
"""
a = 100
b = 123.45
c = 'hello, world'
d = True
print(type(a))  # <class 'int'>
print(type(b))  # <class 'float'>
print(type(c))  # <class 'str'>
print(type(d))  # <class 'bool'>
# === 範例 5 ===
"""
變數的型別轉換操作

Version: 1.0
Author: Kevin
"""
a = 100
b = 123.45
c = '123'
d = '100'
e = '123.45'
f = 'hello, world'
g = True
print(float(a))         # int型別的100轉成float，輸出100.0
print(int(b))           # float型別的123.45轉成int，輸出123
print(int(c))           # str型別的'123'轉成int，輸出123
print(int(c, base=16))  # str型別的'123'按十六進位制轉成int，輸出291
print(int(d, base=2))   # str型別的'100'按二進位制轉成int，輸出4
print(float(e))         # str型別的'123.45'轉成float，輸出123.45
print(bool(f))          # str型別的'hello, world'轉成bool，輸出True
print(int(g))           # bool型別的True轉成int，輸出1
print(chr(a))           # int型別的100轉成str，輸出'd'
print(ord('d'))         # str型別的'd'轉成int，輸出100
