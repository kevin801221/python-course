"""
迴圈結構 - 進階練習解答
========================

這是進階練習題目的完整解答。
請先嘗試自己完成練習，再來對照答案。
"""

import random

# ============================================================
# 練習 1：印出九九乘法表（基礎）
# ============================================================
print("=" * 50)
print("【練習 1：九九乘法表】")
print("=" * 50)

for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i}x{j}={i*j:2d}", end="  ")
    print()  # 換行


# ============================================================
# 練習 2：計算 1 到 N 的總和（基礎）
# ============================================================
print()
print("=" * 50)
print("【練習 2：計算 1 到 N 的總和】")
print("=" * 50)

n = int(input("請輸入 N："))
total = 0

for i in range(1, n + 1):
    total += i

print(f"1 + 2 + 3 + ... + {n} = {total}")

# 也可以使用公式：n * (n + 1) / 2
formula_result = n * (n + 1) // 2
print(f"使用公式驗證：{formula_result}")


# ============================================================
# 練習 3：找出所有質數（進階）
# ============================================================
print()
print("=" * 50)
print("【練習 3：找出所有質數】")
print("=" * 50)

print("2 到 100 之間的質數：")
prime_count = 0

for num in range(2, 101):
    is_prime = True

    # 檢查是否能被 2 到 sqrt(num) 之間的數整除
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

    if is_prime:
        print(num, end=" ")
        prime_count += 1

print(f"\n共 {prime_count} 個質數")


# ============================================================
# 練習 4：密碼驗證系統（進階）
# ============================================================
print()
print("=" * 50)
print("【練習 4：密碼驗證系統】")
print("=" * 50)

correct_password = "python123"
max_attempts = 3
attempts = 0
logged_in = False

while attempts < max_attempts:
    password = input("請輸入密碼：")
    attempts += 1

    if password == correct_password:
        print("登入成功！歡迎使用系統。")
        logged_in = True
        break
    else:
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"密碼錯誤！剩餘 {remaining} 次機會。")
        else:
            print("帳號已鎖定！請聯繫管理員。")


# ============================================================
# 練習 5：繪製星星圖形（進階）
# ============================================================
print()
print("=" * 50)
print("【練習 5：繪製星星圖形】")
print("=" * 50)

n = int(input("請輸入層數："))
print()

for i in range(1, n + 1):
    # 印出空格
    spaces = " " * (n - i)
    # 印出星星
    stars = "*" * (2 * i - 1)
    print(spaces + stars)


# ============================================================
# 練習 6：費波那契數列（挑戰）
# ============================================================
print()
print("=" * 50)
print("【練習 6：費波那契數列】")
print("=" * 50)

n = int(input("請輸入項數："))

if n >= 1:
    # 初始化前兩項
    a, b = 1, 1

    print(f"費波那契數列前 {n} 項：")

    for i in range(n):
        if i == 0:
            print(a, end=" ")
        elif i == 1:
            print(b, end=" ")
        else:
            # 計算下一項
            c = a + b
            print(c, end=" ")
            # 更新變數
            a = b
            b = c

    print()  # 換行


# ============================================================
# 練習 7：猜數字遊戲（挑戰）
# ============================================================
print()
print("=" * 50)
print("【練習 7：猜數字遊戲】")
print("=" * 50)

secret = random.randint(1, 100)
attempts = 0

print("我想了一個 1 到 100 之間的數字，猜猜看！")
print()

while True:
    try:
        guess = int(input("請猜一個數字："))
        attempts += 1

        if guess < 1 or guess > 100:
            print("請輸入 1 到 100 之間的數字！")
            attempts -= 1  # 無效輸入不計次數
            continue

        if guess == secret:
            print(f"\n恭喜你猜對了！")
            print(f"答案是 {secret}，你用了 {attempts} 次猜中！")

            # 評價
            if attempts <= 5:
                print("太厲害了！")
            elif attempts <= 7:
                print("表現不錯！")
            else:
                print("下次可以試試二分法！")
            break
        elif guess < secret:
            print("太小了！\n")
        else:
            print("太大了！\n")

    except ValueError:
        print("請輸入有效的數字！")


# ============================================================
# 【迴圈結構整理】
# ============================================================
"""
【for 迴圈】
for 變數 in 可迭代物件:
    執行程式碼

常用的可迭代物件：
- range(n)：0 到 n-1
- range(start, end)：start 到 end-1
- range(start, end, step)：指定步長
- 字串、列表、元組等

【while 迴圈】
while 條件:
    執行程式碼

特點：
- 適合不確定執行次數的情況
- 條件為 True 時持續執行
- 注意避免無限迴圈

【迴圈控制】
break：立即跳出迴圈
continue：跳過本次迴圈，進入下一次

【巢狀迴圈】
for i in range(n):
    for j in range(m):
        # 內層迴圈
    # 外層迴圈
"""
