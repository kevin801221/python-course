"""
分支結構 - 進階練習解答
========================

這是進階練習題目的完整解答。
請先嘗試自己完成練習，再來對照答案。
"""

# ============================================================
# 練習 1：成年判斷器（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：成年判斷器】")
print("=" * 40)

age = int(input("請輸入您的年齡："))

if age >= 18:
    print("您已成年，可以辦理各項業務。")
else:
    print("您未成年，部分業務需要監護人陪同。")


# ============================================================
# 練習 2：成績等第判定（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：成績等第判定】")
print("=" * 40)

score = int(input("請輸入成績："))

if score >= 90:
    grade = "A（優秀）"
elif score >= 80:
    grade = "B（良好）"
elif score >= 70:
    grade = "C（中等）"
elif score >= 60:
    grade = "D（及格）"
else:
    grade = "F（不及格）"

print(f"您的等第是：{grade}")


# ============================================================
# 練習 3：閏年判斷器（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：閏年判斷器】")
print("=" * 40)

year = int(input("請輸入年份："))

# 閏年規則：
# 1. 能被 4 整除，且不能被 100 整除
# 2. 或者能被 400 整除
is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

if is_leap_year:
    print(f"{year} 年是閏年！")
    print(f"這一年的二月有 29 天。")
else:
    print(f"{year} 年不是閏年。")
    print(f"這一年的二月有 28 天。")


# ============================================================
# 練習 4：BMI 健康評估（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 4：BMI 健康評估】")
print("=" * 40)

height = float(input("請輸入身高（公分）："))
weight = float(input("請輸入體重（公斤）："))

# 計算 BMI
height_m = height / 100
bmi = weight / (height_m ** 2)

# 判斷健康狀態
if bmi < 18.5:
    status = "過輕"
    advice = "建議增加營養攝取，適度運動增肌。"
elif bmi < 24:
    status = "正常"
    advice = "請繼續保持良好的生活習慣！"
elif bmi < 27:
    status = "過重"
    advice = "建議控制飲食，增加運動量。"
elif bmi < 30:
    status = "輕度肥胖"
    advice = "建議諮詢醫師，制定健康計畫。"
else:
    status = "重度肥胖"
    advice = "建議立即就醫，進行專業評估。"

print()
print(f"您的 BMI 是：{bmi:.2f}")
print(f"健康狀態：{status}")
print(f"建議：{advice}")


# ============================================================
# 練習 5：簡易計算機（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 5：簡易計算機】")
print("=" * 40)

num1 = float(input("請輸入第一個數字："))
operator = input("請輸入運算符號（+ - * /）：")
num2 = float(input("請輸入第二個數字："))

if operator == "+":
    result = num1 + num2
    print(f"\n計算結果：{num1} + {num2} = {result}")
elif operator == "-":
    result = num1 - num2
    print(f"\n計算結果：{num1} - {num2} = {result}")
elif operator == "*":
    result = num1 * num2
    print(f"\n計算結果：{num1} × {num2} = {result}")
elif operator == "/":
    if num2 != 0:
        result = num1 / num2
        print(f"\n計算結果：{num1} ÷ {num2} = {result}")
    else:
        print("\n錯誤：除數不能為零！")
else:
    print("\n錯誤：無效的運算符號！")


# ============================================================
# 練習 6：票價計算器（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 6：票價計算器】")
print("=" * 40)

BASE_PRICE = 300

age = int(input("請輸入年齡："))
weekday = int(input("今天是星期幾（1-7）："))
session = int(input("請選擇場次（1=早場 2=午場 3=晚場）："))

# 計算身份折扣
if age < 12:
    identity = "兒童"
    discount_rate = 0.5
elif age <= 22:
    identity = "學生"
    discount_rate = 0.7
elif age <= 64:
    identity = "成人"
    discount_rate = 1.0
else:
    identity = "敬老"
    discount_rate = 0.5

# 計算基本票價
price = BASE_PRICE * discount_rate
discount_text = f"{int(discount_rate * 10)} 折" if discount_rate < 1 else "原價"

# 週三優惠
wednesday_discount = 0
if weekday == 3:
    wednesday_discount = price * 0.1
    price = price * 0.9

# 早場優惠
early_discount = 0
if session == 1:
    early_discount = 50
    price = price - 50

print()
print("【票價計算明細】")
print(f"基本票價：{BASE_PRICE} 元")
print(f"身份折扣：{identity}（{discount_text}）")
if weekday == 3:
    print(f"週三優惠：9 折（-{wednesday_discount:.0f} 元）")
if session == 1:
    print(f"早場優惠：-{early_discount} 元")
print("-" * 17)
print(f"實付金額：{price:.0f} 元")


# ============================================================
# 練習 7：三角形判斷器（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 7：三角形判斷器】")
print("=" * 40)

a = float(input("請輸入第一邊長度："))
b = float(input("請輸入第二邊長度："))
c = float(input("請輸入第三邊長度："))

# 檢查是否能構成三角形
if a + b > c and b + c > a and a + c > b:
    print()
    # 判斷三角形類型
    if a == b == c:
        print("這是一個等邊三角形！")
    elif a == b or b == c or a == c:
        print("這是一個等腰三角形！")
    else:
        # 檢查是否為直角三角形
        # 將三邊排序，最長邊為斜邊
        sides = sorted([a, b, c])
        # 使用近似比較，避免浮點數精度問題
        if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 0.0001:
            print("這是一個直角三角形！")
        else:
            print("這是一個普通三角形。")
else:
    print()
    print("這三個邊長無法構成三角形！")
    print("（任意兩邊之和必須大於第三邊）")


# ============================================================
# 【分支結構整理】
# ============================================================
"""
【if 語句基本結構】

1. 單分支：
   if 條件:
       執行程式碼

2. 雙分支：
   if 條件:
       執行程式碼 A
   else:
       執行程式碼 B

3. 多分支：
   if 條件1:
       執行程式碼 A
   elif 條件2:
       執行程式碼 B
   elif 條件3:
       執行程式碼 C
   else:
       執行程式碼 D

【條件運算子】
==  等於
!=  不等於
>   大於
<   小於
>=  大於等於
<=  小於等於

【邏輯運算子】
and  且（兩個條件都要成立）
or   或（至少一個條件成立）
not  非（反轉條件）

【條件表達式（三元運算子）】
結果 = 值A if 條件 else 值B
"""
