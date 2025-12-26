"""
列表基礎 - 進階練習解答
========================
"""

# ============================================================
# 練習 1：列表基本操作（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：列表基本操作】")
print("=" * 40)

# 建立列表
numbers = [1, 2, 3, 4, 5]
print(f"原始列表：{numbers}")

# 在末尾添加 6
numbers.append(6)
print(f"添加 6 後：{numbers}")

# 在開頭插入 0
numbers.insert(0, 0)
print(f"插入 0 後：{numbers}")

# 刪除數字 3
numbers.remove(3)
print(f"刪除 3 後：{numbers}")

# 顯示列表長度
print(f"列表長度：{len(numbers)}")


# ============================================================
# 練習 2：成績管理（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：成績管理】")
print("=" * 40)

scores = []

# 輸入 5 個學生成績
for i in range(1, 6):
    score = float(input(f"請輸入第 {i} 位學生成績："))
    scores.append(score)

# 計算統計資料
average = sum(scores) / len(scores)
highest = max(scores)
lowest = min(scores)
passed = sum(1 for s in scores if s >= 60)

print()
print("【成績報告】")
print(f"所有成績：{scores}")
print(f"平均分：{average}")
print(f"最高分：{highest}")
print(f"最低分：{lowest}")
print(f"及格人數：{passed}")


# ============================================================
# 練習 3：列表排序與反轉（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：列表排序與反轉】")
print("=" * 40)

# 輸入數字
input_str = input("請輸入數字（逗號分隔）：")
numbers = [int(x.strip()) for x in input_str.split(",")]

print(f"\n原始列表：{numbers}")

# 升序排列（使用 sorted 不改變原列表）
ascending = sorted(numbers)
print(f"升序排列：{ascending}")

# 降序排列
descending = sorted(numbers, reverse=True)
print(f"降序排列：{descending}")

# 反轉列表
reversed_list = numbers[::-1]
print(f"反轉列表：{reversed_list}")


# ============================================================
# 練習 4：列表篩選（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 4：列表篩選】")
print("=" * 40)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 分離奇數和偶數
odd_numbers = [x for x in numbers if x % 2 == 1]
even_numbers = [x for x in numbers if x % 2 == 0]

print(f"原始列表：{numbers}")
print(f"奇數列表：{odd_numbers}")
print(f"偶數列表：{even_numbers}")


# ============================================================
# 練習 5：通訊錄（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 5：通訊錄】")
print("=" * 40)

contacts = []  # 儲存 [姓名, 電話] 的列表

while True:
    print("\n=== 通訊錄 ===")
    print("1. 新增聯絡人")
    print("2. 顯示所有聯絡人")
    print("3. 搜尋聯絡人")
    print("4. 刪除聯絡人")
    print("0. 退出")

    choice = input("\n請選擇功能：")

    if choice == "1":
        name = input("請輸入姓名：")
        phone = input("請輸入電話：")
        contacts.append([name, phone])
        print(f"已新增聯絡人：{name}")

    elif choice == "2":
        if contacts:
            print("\n【聯絡人清單】")
            for i, (name, phone) in enumerate(contacts, 1):
                print(f"  {i}. {name}: {phone}")
        else:
            print("\n通訊錄是空的。")

    elif choice == "3":
        keyword = input("請輸入搜尋關鍵字：")
        found = []
        for name, phone in contacts:
            if keyword.lower() in name.lower():
                found.append((name, phone))

        if found:
            print("\n【搜尋結果】")
            for name, phone in found:
                print(f"  {name}: {phone}")
        else:
            print("\n找不到符合的聯絡人。")

    elif choice == "4":
        if contacts:
            print("\n【聯絡人清單】")
            for i, (name, phone) in enumerate(contacts, 1):
                print(f"  {i}. {name}: {phone}")

            try:
                num = int(input("\n請輸入要刪除的編號："))
                if 1 <= num <= len(contacts):
                    removed = contacts.pop(num - 1)
                    print(f"已刪除：{removed[0]}")
                else:
                    print("編號無效！")
            except ValueError:
                print("請輸入有效數字！")
        else:
            print("\n通訊錄是空的。")

    elif choice == "0":
        print("\n感謝使用！再見！")
        break

    else:
        print("無效選項，請重新選擇。")


# ============================================================
# 【列表方法整理】
# ============================================================
"""
【新增元素】
list.append(x)     在末尾添加元素
list.insert(i, x)  在指定位置插入元素
list.extend(list2) 合併另一個列表

【刪除元素】
list.remove(x)     刪除第一個值為 x 的元素
list.pop(i)        刪除並返回指定位置的元素
list.clear()       清空列表
del list[i]        刪除指定位置的元素

【查詢】
list.index(x)      返回第一個值為 x 的索引
list.count(x)      計算 x 出現的次數
x in list          檢查 x 是否在列表中

【排序】
list.sort()        原地排序
list.reverse()     原地反轉
sorted(list)       返回排序後的新列表

【其他】
len(list)          列表長度
max(list)          最大值
min(list)          最小值
sum(list)          總和
"""
