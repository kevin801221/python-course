#!/usr/bin/env python3
"""
從 17.函数高级应用.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import random
import time


def download(filename):
    """下載檔案"""
    print(f'開始下載{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下載完成.')

    
def upload(filename):
    """上傳檔案"""
    print(f'開始上傳{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上傳完成.')

    
download('MySQL從刪庫到跑路.avi')
upload('Python從入門到住院.pdf')
# === 範例 2 ===
start = time.time()
download('MySQL從刪庫到跑路.avi')
end = time.time()
print(f'花費時間: {end - start:.2f}秒')
start = time.time()
upload('Python從入門到住院.pdf')
end = time.time()
print(f'花費時間: {end - start:.2f}秒')
# === 範例 3 ===
def record_time(func):
    
    def wrapper(*args, **kwargs):
        
        result = func(*args, **kwargs)
        
        return result
    
    return wrapper
# === 範例 4 ===
import time


def record_time(func):

    def wrapper(*args, **kwargs):
        # 在執行被裝飾的函式之前記錄開始時間
        start = time.time()
        # 執行被裝飾的函式並獲取返回值
        result = func(*args, **kwargs)
        # 在執行被裝飾的函式之後記錄結束時間
        end = time.time()
        # 計算和顯示被裝飾函式的執行時間
        print(f'{func.__name__}執行時間: {end - start:.2f}秒')
        # 返回被裝飾函式的返回值
        return result
    
    return wrapper
# === 範例 5 ===
download = record_time(download)
upload = record_time(upload)
download('MySQL從刪庫到跑路.avi')
upload('Python從入門到住院.pdf')
# === 範例 6 ===
import random
import time


def record_time(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__}執行時間: {end - start:.2f}秒')
        return result

    return wrapper


@record_time
def download(filename):
    print(f'開始下載{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下載完成.')


@record_time
def upload(filename):
    print(f'開始上傳{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上傳完成.')


download('MySQL從刪庫到跑路.avi')
upload('Python從入門到住院.pdf')
# === 範例 7 ===
import random
import time

from functools import wraps


def record_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__}執行時間: {end - start:.2f}秒')
        return result

    return wrapper


@record_time
def download(filename):
    print(f'開始下載{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下載完成.')


@record_time
def upload(filename):
    print(f'開始上傳{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上傳完成.')


# 呼叫裝飾後的函式會記錄執行時間
download('MySQL從刪庫到跑路.avi')
upload('Python從入門到住院.pdf')
# 取消裝飾器的作用不記錄執行時間
download.__wrapped__('MySQL必知必會.pdf')
upload.__wrapped__('Python從新手到大師.pdf')
# === 範例 8 ===
def fac(num):
    if num in (0, 1):
        return 1
    return num * fac(num - 1)
# === 範例 9 ===
# 遞迴呼叫函式入棧
# 5 * fac(4)
# 5 * (4 * fac(3))
# 5 * (4 * (3 * fac(2)))
# 5 * (4 * (3 * (2 * fac(1))))
# 停止遞迴函式出棧
# 5 * (4 * (3 * (2 * 1)))
# 5 * (4 * (3 * 2))
# 5 * (4 * 6)
# 5 * 24
# 120
print(fac(5))    # 120
# === 範例 10 ===
def fib1(n):
    if n in (1, 2):
        return 1
    return fib1(n - 1) + fib1(n - 2)


for i in range(1, 21):
    print(fib1(i))
# === 範例 11 ===
def fib2(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
# === 範例 12 ===
from functools import lru_cache


@lru_cache()
def fib1(n):
    if n in (1, 2):
        return 1
    return fib1(n - 1) + fib1(n - 2)


for i in range(1, 51):
    print(i, fib1(i))
