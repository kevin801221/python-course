"""
成績分析系統 - 進階練習解答
============================

這是進階練習題目的完整解答。
請先嘗試自己完成練習，再來對照答案。
"""

# ============================================================
# 練習 1：增加第四科成績（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：增加第四科成績】")
print("=" * 40)

chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))
social = float(input("請輸入社會成績："))

total = chinese + english + math + social
average = total / 4

print()
print("【四科成績統計】")
print(f"總分：{total}")
print(f"平均：{average:.2f}")


# ============================================================
# 練習 2：計算各科與平均分的差距（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 2：各科與平均分的差距】")
print("=" * 40)

chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))

average = (chinese + english + math) / 3

# 計算各科差距
chinese_diff = chinese - average
english_diff = english - average
math_diff = math - average

# 判斷高於或低於平均
chinese_status = "高於平均" if chinese_diff > 0 else "低於平均"
english_status = "高於平均" if english_diff > 0 else "低於平均"
math_status = "高於平均" if math_diff > 0 else "低於平均"

print()
print(f"平均分：{average:.2f}")
print(f"國文差距：{chinese_diff:+.2f}（{chinese_status}）")
print(f"英文差距：{english_diff:+.2f}（{english_status}）")
print(f"數學差距：{math_diff:+.2f}（{math_status}）")


# ============================================================
# 練習 3：找出最強科目和最弱科目（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：找出最強和最弱科目】")
print("=" * 40)

chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))

highest = max(chinese, english, math)
lowest = min(chinese, english, math)
score_range = highest - lowest

# 判斷最高分是哪科
if highest == chinese:
    highest_subject = "國文"
elif highest == english:
    highest_subject = "英文"
else:
    highest_subject = "數學"

# 判斷最低分是哪科
if lowest == chinese:
    lowest_subject = "國文"
elif lowest == english:
    lowest_subject = "英文"
else:
    lowest_subject = "數學"

print()
print(f"最高分：{highest}（{highest_subject}）")
print(f"最低分：{lowest}（{lowest_subject}）")
print(f"最高與最低差距：{score_range} 分")


# ============================================================
# 練習 4：加權平均計算（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：加權平均計算】")
print("=" * 40)

# 定義權重
CHINESE_WEIGHT = 0.3
ENGLISH_WEIGHT = 0.3
MATH_WEIGHT = 0.4

chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))

# 計算各科加權分數
weighted_chinese = chinese * CHINESE_WEIGHT
weighted_english = english * ENGLISH_WEIGHT
weighted_math = math * MATH_WEIGHT

# 計算加權平均
weighted_average = weighted_chinese + weighted_english + weighted_math

print()
print("【加權平均計算】")
print(f"國文 {chinese} × 30% = {weighted_chinese}")
print(f"英文 {english} × 30% = {weighted_english}")
print(f"數學 {math} × 40% = {weighted_math}")
print("-" * 23)
print(f"加權平均：{weighted_average} 分")


# ============================================================
# 練習 5：多條件等第判斷（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 5：多條件等第判斷】")
print("=" * 40)

chinese = float(input("請輸入國文成績："))
english = float(input("請輸入英文成績："))
math = float(input("請輸入數學成績："))

average = (chinese + english + math) / 3
all_above_80 = chinese >= 80 and english >= 80 and math >= 80
all_above_60 = chinese >= 60 and english >= 60 and math >= 60

# 使用 if-elif-else 判斷等第
if average >= 90 and all_above_80:
    grade = "A+（特優）"
elif average >= 90:
    grade = "A（優秀）"
elif average >= 80 and all_above_60:
    grade = "B（良好）"
elif average >= 70:
    grade = "C（中等）"
elif average >= 60:
    grade = "D（及格）"
else:
    grade = "F（不及格）"

print()
print(f"平均分：{average:.2f}")
print(f"三科都 80 以上：{'是' if all_above_80 else '否'}")
print(f"綜合評等：{grade}")


# ============================================================
# 練習 6：成績進步追蹤（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 6：成績進步追蹤】")
print("=" * 40)

midterm = float(input("請輸入期中考成績："))
final = float(input("請輸入期末考成績："))

# 計算變化
change = final - midterm
change_percent = (change / midterm) * 100

# 判斷評語
if change > 10:
    comment = "表現大幅進步，非常優秀！"
elif change > 0:
    comment = "表現進步，繼續加油！"
elif change == 0:
    comment = "表現持平，再接再厲！"
elif change > -10:
    comment = "稍微退步，需要加強！"
else:
    comment = "退步較多，請多加努力！"

print()
print("【成績變化分析】")
print(f"期中考：{midterm} 分")
print(f"期末考：{final} 分")
print(f"分數變化：{change:+.0f} 分")
print(f"變化比例：{change_percent:+.2f}%")
print(f"評語：{comment}")


# ============================================================
# 【運算子整理】
# ============================================================
"""
【算術運算子】
+   加法        10 + 3 = 13
-   減法        10 - 3 = 7
*   乘法        10 * 3 = 30
/   除法        10 / 3 = 3.333...
//  整數除法    10 // 3 = 3
%   取餘數      10 % 3 = 1
**  次方        10 ** 2 = 100

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

【格式化技巧】
{value:.2f}    保留兩位小數
{value:+.2f}   顯示正負號 + 兩位小數
"""
