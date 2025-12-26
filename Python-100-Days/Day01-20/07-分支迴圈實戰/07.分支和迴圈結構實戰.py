#!/usr/bin/env python3
"""
從 07.分支和循环结构实战.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
"""
輸出100以內的素數

Version: 1.0
Author: Kevin
"""
for num in range(2, 100):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num)
# === 範例 2 ===
"""
輸出斐波那契數列中的前20個數

Version: 1.0
Author: Kevin
"""

a, b = 0, 1
for _ in range(20):
    a, b = b, a + b
    print(a)
# === 範例 3 ===
"""
找出100到999範圍內的水仙花數

Version: 1.0
Author: Kevin
"""
for num in range(100, 1000):
    low = num % 10
    mid = num // 10 % 10
    high = num // 100
    if num == low ** 3 + mid ** 3 + high ** 3:
        print(num)
# === 範例 4 ===
"""
正整數的反轉

Version: 1.0
Author: Kevin
"""
num = int(input('num = '))
reversed_num = 0
while num > 0:
    reversed_num = reversed_num * 10 + num % 10
    num //= 10
print(reversed_num)
# === 範例 5 ===
"""
百錢百雞問題

Version: 1.0
Author: Kevin
"""
for x in range(0, 21):
    for y in range(0, 34):
        for z in range(0, 100, 3):
            if x + y + z == 100 and 5 * x + 3 * y + z // 3 == 100:
                print(f'公雞: {x}只, 母雞: {y}只, 小雞: {z}只')
# === 範例 6 ===
"""
百錢百雞問題

Version: 1.1
Author: Kevin
"""
for x in range(0, 21):
    for y in range(0, 34):
        z = 100 - x - y
        if z % 3 == 0 and 5 * x + 3 * y + z // 3 == 100:
            print(f'公雞: {x}只, 母雞: {y}只, 小雞: {z}只')
# === 範例 7 ===
"""
Craps賭博遊戲

Version: 1.0
Author: Kevin
"""
import random

money = 1000
while money > 0:
    print(f'你的總資產為: {money}元')
    # 下注金額必須大於0且小於等於玩家的總資產
    while True:
        debt = int(input('請下注: '))
        if 0 < debt <= money:
            break
    # 用兩個1到6均勻分佈的隨機數相加模擬搖兩顆色子得到的點數
    first_point = random.randrange(1, 7) + random.randrange(1, 7)
    print(f'\n玩家搖出了{first_point}點')
    if first_point == 7 or first_point == 11:
        print('玩家勝!\n')
        money += debt
    elif first_point == 2 or first_point == 3 or first_point == 12:
        print('莊家勝!\n')
        money -= debt
    else:
        # 如果第一次搖色子沒有分出勝負，玩家需要重新搖色子
        while True:
            current_point = random.randrange(1, 7) + random.randrange(1, 7)
            print(f'玩家搖出了{current_point}點')
            if current_point == 7:
                print('莊家勝!\n')
                money -= debt
                break
            elif current_point == first_point:
                print('玩家勝!\n')
                money += debt
                break
print('你破產了, 遊戲結束!')
