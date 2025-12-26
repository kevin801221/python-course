"""
分支與迴圈實戰 - 進階練習解答
==============================
"""

import random

# ============================================================
# 練習 1：簡易待辦事項（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：簡易待辦事項】")
print("=" * 40)

todos = []

while True:
    print("\n=== 待辦事項管理 ===")
    print("1. 新增待辦事項")
    print("2. 顯示所有待辦事項")
    print("3. 刪除待辦事項")
    print("0. 退出")

    choice = input("\n請選擇功能：")

    if choice == "1":
        item = input("請輸入待辦事項：")
        todos.append(item)
        print(f"已新增：{item}")

    elif choice == "2":
        if todos:
            print("\n【待辦事項清單】")
            for i, item in enumerate(todos, 1):
                print(f"  {i}. {item}")
        else:
            print("\n目前沒有待辦事項。")

    elif choice == "3":
        if todos:
            print("\n【待辦事項清單】")
            for i, item in enumerate(todos, 1):
                print(f"  {i}. {item}")
            try:
                num = int(input("\n請輸入要刪除的編號："))
                if 1 <= num <= len(todos):
                    removed = todos.pop(num - 1)
                    print(f"已刪除：{removed}")
                else:
                    print("編號無效！")
            except ValueError:
                print("請輸入有效數字！")
        else:
            print("\n目前沒有待辦事項。")

    elif choice == "0":
        print("\n感謝使用！再見！")
        break

    else:
        print("無效選項，請重新選擇。")


# ============================================================
# 練習 2：成績統計系統（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 2：成績統計系統】")
print("=" * 40)

scores = []

while True:
    try:
        score = float(input("請輸入成績（-1 結束）："))
        if score == -1:
            break
        if 0 <= score <= 100:
            scores.append(score)
        else:
            print("成績必須在 0 到 100 之間！")
    except ValueError:
        print("請輸入有效的數字！")

if scores:
    total = sum(scores)
    count = len(scores)
    average = total / count
    highest = max(scores)
    lowest = min(scores)
    passed = sum(1 for s in scores if s >= 60)
    failed = count - passed

    print("\n【成績統計報告】")
    print(f"總人數：{count} 人")
    print(f"總分：{total:.0f} 分")
    print(f"平均分：{average:.2f} 分")
    print(f"最高分：{highest:.0f} 分")
    print(f"最低分：{lowest:.0f} 分")
    print(f"及格人數：{passed} 人")
    print(f"不及格人數：{failed} 人")
else:
    print("\n沒有輸入任何成績。")


# ============================================================
# 練習 3：自動販賣機（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 3：自動販賣機】")
print("=" * 40)

# 商品清單
products = {
    1: ("可樂", 25),
    2: ("紅茶", 20),
    3: ("咖啡", 35),
    4: ("礦泉水", 15)
}

while True:
    print("\n=== 歡迎使用自動販賣機 ===")
    for num, (name, price) in products.items():
        print(f"{num}. {name} - {price} 元")
    print("0. 退出")

    # 投幣
    try:
        money = int(input("\n請投入金額："))
        if money <= 0:
            print("請投入有效金額！")
            continue
    except ValueError:
        print("請輸入有效數字！")
        continue

    print(f"目前金額：{money} 元")

    # 選擇商品
    try:
        choice = int(input("\n請選擇商品編號："))
        if choice == 0:
            print(f"退還金額：{money} 元")
            print("感謝光臨！")
            break
        elif choice in products:
            name, price = products[choice]
            if money >= price:
                change = money - price
                print(f"購買成功！您購買了 {name}")
                print(f"找零 {change} 元")
            else:
                print(f"金額不足！{name} 需要 {price} 元")
        else:
            print("無效的商品編號！")
    except ValueError:
        print("請輸入有效數字！")

    # 繼續購買？
    cont = input("\n是否繼續購買？(y/n)：").lower()
    if cont != 'y':
        print("感謝光臨！")
        break


# ============================================================
# 練習 4：猜拳遊戲（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：猜拳遊戲】")
print("=" * 40)

choices = {1: "剪刀", 2: "石頭", 3: "布"}
wins = 0
losses = 0
ties = 0

while True:
    print("\n=== 猜拳遊戲 ===")
    print("1. 剪刀")
    print("2. 石頭")
    print("3. 布")
    print("0. 結束")

    try:
        player_choice = int(input("\n請出拳："))

        if player_choice == 0:
            break

        if player_choice not in choices:
            print("無效選擇！")
            continue

        # 電腦隨機出拳
        computer_choice = random.randint(1, 3)

        print(f"你出：{choices[player_choice]}")
        print(f"電腦出：{choices[computer_choice]}")

        # 判斷勝負
        # 1=剪刀, 2=石頭, 3=布
        # 剪刀(1) 勝 布(3)
        # 石頭(2) 勝 剪刀(1)
        # 布(3) 勝 石頭(2)
        if player_choice == computer_choice:
            print("平手！")
            ties += 1
        elif (player_choice == 1 and computer_choice == 3) or \
             (player_choice == 2 and computer_choice == 1) or \
             (player_choice == 3 and computer_choice == 2):
            print("你贏了！")
            wins += 1
        else:
            print("你輸了！")
            losses += 1

        print(f"\n目前戰績：{wins} 勝 {losses} 敗 {ties} 平")

    except ValueError:
        print("請輸入有效數字！")

# 顯示最終戰績
total_games = wins + losses + ties
if total_games > 0:
    win_rate = wins / total_games * 100
    print("\n=== 最終戰績 ===")
    print(f"勝利：{wins} 次")
    print(f"失敗：{losses} 次")
    print(f"平手：{ties} 次")
    print(f"勝率：{win_rate:.1f}%")
else:
    print("\n沒有進行任何遊戲。")

print("\n感謝遊玩！")
