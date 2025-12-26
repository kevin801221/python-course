"""
列表進階 - 進階練習解答
========================
"""

import random

# ============================================================
# 練習 1：列表生成式基礎（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：列表生成式基礎】")
print("=" * 40)

# 1 到 10 的平方
squares = [i ** 2 for i in range(1, 11)]
print(f"平方列表：{squares}")

# 1 到 20 的偶數
evens = [i for i in range(1, 21) if i % 2 == 0]
print(f"偶數列表：{evens}")

# 1 到 50 能被 3 整除的數
divisible_by_3 = [i for i in range(1, 51) if i % 3 == 0]
print(f"被3整除：{divisible_by_3}")


# ============================================================
# 練習 2：矩陣運算（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 2：矩陣運算】")
print("=" * 40)

# 建立 3x3 矩陣
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 顯示矩陣
print("矩陣：")
for row in matrix:
    print(" ".join(str(x) for x in row))

print()

# 所有元素總和
total = sum(sum(row) for row in matrix)
print(f"所有元素總和：{total}")

# 每行總和
for i, row in enumerate(matrix, 1):
    print(f"第 {i} 行總和：{sum(row)}")

# 每列總和
for j in range(3):
    col_sum = sum(matrix[i][j] for i in range(3))
    print(f"第 {j + 1} 列總和：{col_sum}")

# 對角線總和
diagonal_sum = sum(matrix[i][i] for i in range(3))
print(f"對角線總和：{diagonal_sum}")


# ============================================================
# 練習 3：成績排名系統（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：成績排名系統】")
print("=" * 40)

# 學生資料 [姓名, 國文, 英文, 數學]
students = [
    ["Alice", 85, 90, 88],
    ["Bob", 78, 82, 95],
    ["Carol", 92, 88, 85]
]

# 計算總分和平均，並添加到資料中
for student in students:
    total = student[1] + student[2] + student[3]
    avg = total / 3
    student.append(total)
    student.append(avg)

# 按總分排序（降序）
students.sort(key=lambda x: x[4], reverse=True)

# 顯示排名
print("\n【成績排名】")
print(f"{'排名':<4} {'姓名':<8} {'國文':<4} {'英文':<4} {'數學':<4} {'總分':<5} {'平均':<6}")
for rank, student in enumerate(students, 1):
    name, chinese, english, math, total, avg = student
    print(f"{rank:<4} {name:<8} {chinese:<4} {english:<4} {math:<4} {total:<5} {avg:<6.2f}")


# ============================================================
# 練習 4：樂透號碼產生器（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：樂透號碼產生器】")
print("=" * 40)

n = int(input("請輸入要產生幾注："))

print("\n【大樂透號碼】")
for i in range(1, n + 1):
    # 從 1-49 中隨機選取 6 個不重複的號碼
    numbers = random.sample(range(1, 50), 6)
    # 排序
    numbers.sort()
    # 格式化輸出（補零到兩位數）
    formatted = " ".join(f"{num:02d}" for num in numbers)
    print(f"第 {i} 注：{formatted}")


# ============================================================
# 【列表生成式語法】
# ============================================================
"""
【基本語法】
[運算式 for 變數 in 可迭代物件]

例：[x ** 2 for x in range(10)]

【帶條件的生成式】
[運算式 for 變數 in 可迭代物件 if 條件]

例：[x for x in range(20) if x % 2 == 0]

【巢狀生成式】
[運算式 for 變數1 in 可迭代物件1 for 變數2 in 可迭代物件2]

例：[[i * j for j in range(1, 4)] for i in range(1, 4)]
結果：[[1, 2, 3], [2, 4, 6], [3, 6, 9]]
"""
