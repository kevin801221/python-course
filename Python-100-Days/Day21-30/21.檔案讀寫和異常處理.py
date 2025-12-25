#!/usr/bin/env python3
"""
從 21.文件读写和异常处理.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
file = open('致橡樹.txt', 'r', encoding='utf-8')
print(file.read())
file.close()
# === 範例 2 ===
file = open('致橡樹.txt', 'r', encoding='utf-8')
for line in file:
    print(line, end='')
file.close()

file = open('致橡樹.txt', 'r', encoding='utf-8')
lines = file.readlines()
for line in lines:
    print(line, end='')
file.close()
# === 範例 3 ===
file = open('致橡樹.txt', 'a', encoding='utf-8')
file.write('\n標題：《致橡樹》')
file.write('\n作者：舒婷')
file.write('\n時間：1977年3月')
file.close()
# === 範例 4 ===
file = None
try:
    file = open('致橡樹.txt', 'r', encoding='utf-8')
    print(file.read())
except FileNotFoundError:
    print('無法開啟指定的檔案!')
except LookupError:
    print('指定了未知的編碼!')
except UnicodeDecodeError:
    print('讀取檔案時解碼錯誤!')
finally:
    if file:
        file.close()
# === 範例 5 ===
class InputError(ValueError):
    """自定義異常型別"""
    pass


def fac(num):
    """求階乘"""
    if num < 0:
        raise InputError('只能計算非負整數的階乘')
    if num in (0, 1):
        return 1
    return num * fac(num - 1)
# === 範例 6 ===
flag = True
while flag:
    num = int(input('n = '))
    try:
        print(f'{num}! = {fac(num)}')
        flag = False
    except InputError as err:
        print(err)
# === 範例 7 ===
try:
    with open('致橡樹.txt', 'r', encoding='utf-8') as file:
        print(file.read())
except FileNotFoundError:
    print('無法開啟指定的檔案!')
except LookupError:
    print('指定了未知的編碼!')
except UnicodeDecodeError:
    print('讀取檔案時解碼錯誤!')
# === 範例 8 ===
try:
    with open('guido.jpg', 'rb') as file1:
        data = file1.read()
    with open('吉多.jpg', 'wb') as file2:
        file2.write(data)
except FileNotFoundError:
    print('指定的檔案無法開啟.')
except IOError:
    print('讀寫檔案時出現錯誤.')
print('程式執行結束.')
# === 範例 9 ===
try:
    with open('guido.jpg', 'rb') as file1, open('吉多.jpg', 'wb') as file2:
        data = file1.read(512)
        while data:
            file2.write(data)
            data = file1.read()
except FileNotFoundError:
    print('指定的檔案無法開啟.')
except IOError:
    print('讀寫檔案時出現錯誤.')
print('程式執行結束.')
