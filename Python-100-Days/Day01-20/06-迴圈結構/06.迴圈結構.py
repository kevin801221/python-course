# #!/usr/bin/env python3
# """
# 從 06.循環結構.md 提取的 Python 範例代碼
# """
#
# # === 範例 1 ===
# import time
#
# print('hello, world')
# time.sleep(1)
# # === 範例 2 ===
# """
# 每隔1秒輸出一次“hello, world”，持續1小時
#
# Author: Kevin
# Version: 1.0
# """
# import time
#
# for i in range(3600):
#     print('hello, world')
#     time.sleep(1)
# # === 範例 3 ===
# """
# 每隔1秒輸出一次“hello, world”，持續1小時
#
# Author: Kevin
# Version: 1.1
# """
# import time
#
# for _ in range(3600):
#     print('hello, world')
#     time.sleep(1)
# # === 範例 4 ===
# """
# 從1到100的整數求和
#
# Version: 1.0
# Author: Kevin
# """
# total = 0
# for i in range(1, 101):
#     total += i
# print(total)
# # === 範例 5 ===
# """
# 從1到100的偶數求和
#
# Version: 1.0
# Author: Kevin
# """
# total = 0
# for i in range(1, 101):
#     if i % 2 == 0:
#         total += i
# print(total)
# # === 範例 6 ===
# """
# 從1到100的偶數求和
#
# Version: 1.1
# Author: Kevin
# """
# total = 0
# for i in range(2, 101, 2):
#     total += i
# print(total)
# # === 範例 7 ===
# """
# 從1到100的偶數求和
#
# Version: 1.2
# Author: Kevin
# """
# print(sum(range(2, 101, 2)))
# # === 範例 8 ===
# """
# 從1到100的整數求和
#
# Version: 1.1
# Author: Kevin
# """
# total = 0
# i = 1
# while i <= 100:
#     total += i
#     i += 1
# print(total)
# # === 範例 9 ===
# """
# 從1到100的偶數求和
#
# Version: 1.3
# Author: Kevin
# """
# total = 0
# i = 2
# while i <= 100:
#     total += i
#     i += 2
# print(total)
# # === 範例 10 ===
# """
# 從1到100的偶數求和
#
# Version: 1.4
# Author: Kevin
# """
# total = 0
# i = 2
# while True:
#     total += i
#     i += 2
#     if i > 100:
#         break
# print(total)
# # === 範例 11 ===
# """
# 從1到100的偶數求和
#
# Version: 1.5
# Author: Kevin
# """
# total = 0
# for i in range(1, 101):
#     if i % 2 != 0:
#         continue
#     total += i
# print(total)
# === 範例 12 ===
"""
列印乘法口訣表

Version: 1.0
Author: Kevin
"""
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{i}×{j}={i * j}', end='\t')
    print()
# === 範例 13 ===
"""
輸入一個大於1的正整數判斷它是不是素數

Version: 1.0
Author: Kevin
"""
num = int(input('請輸入一個正整數: '))
end = int(num ** 0.5)
is_prime = True
for i in range(2, end + 1):
    if num % i == 0:
        is_prime = False
        break
if is_prime:
    print(f'{num}是素數')
else:
    print(f'{num}不是素數')
# === 範例 14 ===
"""
輸入兩個正整數求它們的最大公約數

Version: 1.0
Author: Kevin
"""
x = int(input('x = '))
y = int(input('y = '))
for i in range(x, 0, -1):
    if x % i == 0 and y % i == 0:
        print(f'最大公約數: {i}')
        break
# === 範例 15 ===
"""
輸入兩個正整數求它們的最大公約數

Version: 1.1
Author: Kevin
"""
x = int(input('x = '))
y = int(input('y = '))
while y % x != 0:
    x, y = y % x, x
print(f'最大公約數: {x}')
# === 範例 16 ===
"""
猜數字小遊戲

Version: 1.0
Author: Kevin
"""
import random

answer = random.randrange(1, 101)
counter = 0
while True:
    counter += 1
    num = int(input('請輸入: '))
    if num < answer:
        print('大一點.')
    elif num > answer:
        print('小一點.')
    else:
        print('猜對了.')
        break
print(f'你一共猜了{counter}次.')
