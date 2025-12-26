"""
成績分析系統 - Grade Analysis System
====================================

【學習目標】
這個範例展示如何使用各種運算子來分析成績。
透過這個範例，你將學會：
1. 算術運算子：+, -, *, /, //, %, **
2. 比較運算子：>, <, >=, <=, ==, !=
3. 邏輯運算子：and, or, not
4. 複合賦值運算子：+=, -=, *=, /=

【前置知識】
- 第 02 課：print()、input()
- 第 03 課：變數
- 第 04 課：運算子

【程式碼難度】★★☆☆☆ 基礎級
"""

# ============================================================
# 第一步：顯示歡迎訊息
# ============================================================
print("=" * 50)
print("           成績分析系統")
print("=" * 50)
print()

# ============================================================
# 第二步：輸入成績資料
# ============================================================
print("【請輸入三科成績】")
print("-" * 50)

# 讀取三科成績
chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))

# ============================================================
# 第三步：使用算術運算子計算統計資料
# ============================================================
print()
print("=" * 50)
print("           成績分析報告")
print("=" * 50)

print()
print("【算術運算子示範】")
print("-" * 50)

# 加法運算子 (+)：計算總分
total = chinese + english + math
print(f"總分 = {chinese} + {english} + {math} = {total}")

# 除法運算子 (/)：計算平均分
average = total / 3
print(f"平均 = {total} / 3 = {average:.2f}")

# 整數除法運算子 (//)：只取整數部分
average_int = total // 3
print(f"平均（取整數）= {total} // 3 = {average_int}")

# 取餘數運算子 (%)：計算餘數
remainder = total % 3
print(f"餘數 = {total} % 3 = {remainder}")

# 次方運算子 (**)：計算平方
chinese_squared = chinese ** 2
print(f"國文成績的平方 = {chinese} ** 2 = {chinese_squared}")

# 減法和乘法
score_range = max(chinese, english, math) - min(chinese, english, math)
print(f"最高分 - 最低分 = {score_range}")

# ============================================================
# 第四步：使用比較運算子分析成績
# ============================================================
print()
print("【比較運算子示範】")
print("-" * 50)

# 大於 (>)
is_excellent = average > 90
print(f"平均 {average:.1f} > 90？ 結果：{is_excellent}")

# 大於等於 (>=)
is_passing = average >= 60
print(f"平均 {average:.1f} >= 60？ 結果：{is_passing}")

# 小於 (<)
is_failing = average < 60
print(f"平均 {average:.1f} < 60？ 結果：{is_failing}")

# 等於 (==)
is_perfect = average == 100
print(f"平均 {average:.1f} == 100？ 結果：{is_perfect}")

# 不等於 (!=)
is_not_zero = average != 0
print(f"平均 {average:.1f} != 0？ 結果：{is_not_zero}")

# 比較科目分數
chinese_better = chinese > english
print(f"國文 {chinese} > 英文 {english}？ 結果：{chinese_better}")

# ============================================================
# 第五步：使用邏輯運算子判斷條件
# ============================================================
print()
print("【邏輯運算子示範】")
print("-" * 50)

# and（且）：兩個條件都要成立
all_pass = chinese >= 60 and english >= 60 and math >= 60
print(f"三科都及格嗎？")
print(f"  {chinese}>=60 and {english}>=60 and {math}>=60")
print(f"  結果：{all_pass}")

# or（或）：至少一個條件成立
any_excellent = chinese >= 90 or english >= 90 or math >= 90
print(f"有任何一科90分以上嗎？")
print(f"  {chinese}>=90 or {english}>=90 or {math}>=90")
print(f"  結果：{any_excellent}")

# not（非）：反轉布林值
not_failing = not (average < 60)
print(f"不是不及格？")
print(f"  not ({average:.1f} < 60)")
print(f"  結果：{not_failing}")

# 組合使用
good_student = average >= 80 and all_pass
print(f"是好學生嗎（平均80以上且三科都及格）？")
print(f"  結果：{good_student}")

# ============================================================
# 第六步：使用複合賦值運算子
# ============================================================
print()
print("【複合賦值運算子示範】")
print("-" * 50)

# 初始值
bonus = 0
print(f"獎勵分數初始值：{bonus}")

# += 加法賦值
print()
print("假設規則：")
print("  - 平均 >= 90：加 10 分")
print("  - 平均 >= 80：加 5 分")
print("  - 三科都及格：加 3 分")
print()

# 模擬加分過程
if average >= 90:
    bonus += 10  # 相當於 bonus = bonus + 10
    print(f"平均 >= 90，bonus += 10，現在 bonus = {bonus}")
elif average >= 80:
    bonus += 5
    print(f"平均 >= 80，bonus += 5，現在 bonus = {bonus}")

if all_pass:
    bonus += 3
    print(f"三科都及格，bonus += 3，現在 bonus = {bonus}")

print(f"最終獎勵分數：{bonus}")

# ============================================================
# 第七步：輸出最終報告
# ============================================================
print()
print("=" * 50)
print("           最終成績單")
print("=" * 50)
print()
print(f"  國文：{chinese} 分")
print(f"  英文：{english} 分")
print(f"  數學：{math} 分")
print("-" * 30)
print(f"  總分：{total} 分")
print(f"  平均：{average:.1f} 分")
print(f"  獎勵：{bonus} 分")
print("-" * 30)
print(f"  最終平均：{average + bonus:.1f} 分")
print()

# 根據平均分判斷等第
if average >= 90:
    grade = "A（優秀）"
elif average >= 80:
    grade = "B（良好）"
elif average >= 70:
    grade = "C（中等）"
elif average >= 60:
    grade = "D（及格）"
else:
    grade = "F（不及格）"

print(f"  等第：{grade}")
print()
print("=" * 50)


# ============================================================
# 【運算子整理表】
# ============================================================
"""
【算術運算子】
+   加法        10 + 3 = 13
-   減法        10 - 3 = 7
*   乘法        10 * 3 = 30
/   除法        10 / 3 = 3.333...
//  整數除法    10 // 3 = 3
%   取餘數      10 % 3 = 1
**  次方        10 ** 3 = 1000

【比較運算子】
>   大於        10 > 3  → True
<   小於        10 < 3  → False
>=  大於等於    10 >= 10 → True
<=  小於等於    10 <= 10 → True
==  等於        10 == 10 → True
!=  不等於      10 != 3  → True

【邏輯運算子】
and  且（兩者都要成立）    True and False → False
or   或（至少一個成立）    True or False  → True
not  非（反轉）           not True       → False

【複合賦值運算子】
+=   a += 1   相當於  a = a + 1
-=   a -= 1   相當於  a = a - 1
*=   a *= 2   相當於  a = a * 2
/=   a /= 2   相當於  a = a / 2
"""


# ============================================================
# 【練習題】
# ============================================================
"""
試著修改程式，完成以下練習：

1. 基礎練習：
   - 增加一個科目（例如：社會或自然）
   - 計算四科的總分和平均

2. 進階練習：
   - 計算各科與平均分的差距
   - 找出最強科目和最弱科目

3. 挑戰練習：
   - 加入加權計算（例如：國文佔 30%、英文佔 30%、數學佔 40%）
   - 計算標準差（需要學習更多數學公式）
"""
