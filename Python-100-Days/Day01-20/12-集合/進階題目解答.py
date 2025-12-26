"""
集合 - 進階練習解答
====================
"""

# ============================================================
# 練習 1：集合基本操作（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：集合基本操作】")
print("=" * 40)

A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

print(f"集合 A：{A}")
print(f"集合 B：{B}")
print(f"聯集：{A | B}")           # 或 A.union(B)
print(f"交集：{A & B}")           # 或 A.intersection(B)
print(f"A - B：{A - B}")          # 或 A.difference(B)
print(f"B - A：{B - A}")          # 或 B.difference(A)
print(f"對稱差集：{A ^ B}")       # 或 A.symmetric_difference(B)


# ============================================================
# 練習 2：去除重複元素（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：去除重複元素】")
print("=" * 40)

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print(f"原始列表：{numbers}")

# 去重
unique = list(set(numbers))
unique.sort()  # 保持順序
print(f"去重後：{unique}")

# 找出重複的元素
from collections import Counter
counter = Counter(numbers)
duplicates = {num for num, count in counter.items() if count > 1}
print(f"重複的元素：{duplicates}")


# ============================================================
# 練習 3：標籤管理系統（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：標籤管理系統】")
print("=" * 40)

# 兩篇文章的標籤
article1_tags = {'Python', '程式設計', '教學'}
article2_tags = {'Python', 'AI', '機器學習'}

print(f"文章 1 標籤：{article1_tags}")
print(f"文章 2 標籤：{article2_tags}")

# 共同標籤
common_tags = article1_tags & article2_tags
print(f"共同標籤：{common_tags}")

# 所有標籤
all_tags = article1_tags | article2_tags
print(f"所有標籤：{all_tags}")

# 互動式標籤管理
print("\n--- 互動式標籤管理 ---")
tags = set()

while True:
    print("\n1. 新增標籤")
    print("2. 刪除標籤")
    print("3. 顯示所有標籤")
    print("0. 退出")

    choice = input("\n請選擇：")

    if choice == "1":
        tag = input("請輸入標籤：")
        tags.add(tag)
        print(f"已新增：{tag}")
    elif choice == "2":
        if tags:
            print(f"目前標籤：{tags}")
            tag = input("請輸入要刪除的標籤：")
            if tag in tags:
                tags.remove(tag)
                print(f"已刪除：{tag}")
            else:
                print("標籤不存在！")
        else:
            print("沒有標籤。")
    elif choice == "3":
        print(f"所有標籤：{tags if tags else '（空）'}")
    elif choice == "0":
        break


# ============================================================
# 練習 4：共同好友推薦（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：共同好友推薦】")
print("=" * 40)

# 用戶的好友列表
friends = {
    'Alice': {'Bob', 'Carol', 'David'},
    'Bob': {'Alice', 'Carol', 'Eve'},
    'Carol': {'Alice', 'Bob', 'Eve', 'Frank'},
    'David': {'Alice', 'Frank'},
    'Eve': {'Bob', 'Carol'},
    'Frank': {'Carol', 'David'}
}

user1 = 'Alice'
user2 = 'Bob'

print(f"{user1} 的好友：{friends[user1]}")
print(f"{user2} 的好友：{friends[user2]}")

# 共同好友
common = friends[user1] & friends[user2]
print(f"\n{user1} 和 {user2} 的共同好友：{common}")

# 推薦好友（好友的好友，但不是自己的好友，也不是自己）
def recommend_friends(user, friends_dict):
    my_friends = friends_dict[user]
    recommendations = set()

    for friend in my_friends:
        # 好友的好友
        friends_of_friend = friends_dict.get(friend, set())
        recommendations |= friends_of_friend

    # 移除自己和已經是好友的人
    recommendations -= my_friends
    recommendations.discard(user)

    return recommendations

print(f"推薦給 {user1}：{recommend_friends(user1, friends)}")
print(f"推薦給 {user2}：{recommend_friends(user2, friends)}")


# ============================================================
# 【集合方法整理】
# ============================================================
"""
【建立集合】
set()           空集合
{1, 2, 3}       字面量
set([1,2,3])    從列表建立

【新增/刪除】
set.add(x)      新增元素
set.remove(x)   刪除元素（不存在會報錯）
set.discard(x)  刪除元素（不存在不報錯）
set.pop()       隨機刪除並返回一個元素
set.clear()     清空集合

【集合運算】
A | B           聯集（union）
A & B           交集（intersection）
A - B           差集（difference）
A ^ B           對稱差集（symmetric_difference）

【檢查】
x in set        是否在集合中
A <= B          A 是否為 B 的子集
A >= B          A 是否為 B 的超集
A.isdisjoint(B) A 和 B 是否沒有交集
"""
