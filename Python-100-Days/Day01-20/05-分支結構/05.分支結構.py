#!/usr/bin/env python3
"""
從 05.分支结构.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
"""
BMI計算器

Version: 1.0
Author: Kevin
"""
height = float(input('身高(cm)：'))
weight = float(input('體重(kg)：'))
bmi = weight / (height / 100) ** 2
print(f'{bmi = :.1f}')
if 18.5 <= bmi < 24:
    print('你的身材很棒！')
# === 範例 2 ===
"""
BMI計算器

Version: 1.1
Author: Kevin
"""
height = float(input('身高(cm)：'))
weight = float(input('體重(kg)：'))
bmi = weight / (height / 100) ** 2
print(f'{bmi = :.1f}')
if 18.5 <= bmi < 24:
    print('你的身材很棒！')
else:
    print('你的身材不夠標準喲！')
# === 範例 3 ===
"""
BMI計算器

Version: 1.2
Author: Kevin
"""
height = float(input('身高(cm)：'))
weight = float(input('體重(kg)：'))
bmi = weight / (height / 100) ** 2
print(f'{bmi = :.1f}')
if bmi < 18.5:
    print('你的體重過輕！')
elif bmi < 24:
    print('你的身材很棒！')
elif bmi < 27:
    print('你的體重過重！')
elif bmi < 30:
    print('你已輕度肥胖！')
elif bmi < 35:
    print('你已中度肥胖！')
else:
    print('你已重度肥胖！')
# === 範例 4 ===
status_code = int(input('響應狀態碼: '))
if status_code == 400:
    description = 'Bad Request'
elif status_code == 401:
    description = 'Unauthorized'
elif status_code == 403:
    description = 'Forbidden'
elif status_code == 404:
    description = 'Not Found'
elif status_code == 405:
    description = 'Method Not Allowed'
elif status_code == 418:
    description = 'I am a teapot'
elif status_code == 429:
    description = 'Too many requests'
else:
    description = 'Unknown status Code'
print('狀態碼描述:', description)
# === 範例 5 ===
status_code = int(input('響應狀態碼: '))
match status_code:
    case 400: description = 'Bad Request'
    case 401: description = 'Unauthorized'
    case 403: description = 'Forbidden'
    case 404: description = 'Not Found'
    case 405: description = 'Method Not Allowed'
    case 418: description = 'I am a teapot'
    case 429: description = 'Too many requests'
    case _: description = 'Unknown Status Code'
print('狀態碼描述:', description)
# === 範例 6 ===
status_code = int(input('響應狀態碼: '))
match status_code:
    case 400 | 405: description = 'Invalid Request'
    case 401 | 403 | 404: description = 'Not Allowed'
    case 418: description = 'I am a teapot'
    case 429: description = 'Too many requests'
    case _: description = 'Unknown Status Code'
print('狀態碼描述:', description)
# === 範例 7 ===
"""
分段函式求值

Version: 1.0
Author: Kevin
"""
x = float(input('x = '))
if x > 1:
    y = 3 * x - 5
elif x >= -1:
    y = x + 2
else:
    y = 5 * x + 3
print(f'{y = }')
# === 範例 8 ===
"""
分段函式求值

Version: 1.1
Author: Kevin
"""
x = float(input('x = '))
if x > 1:
    y = 3 * x - 5
else:
    if x >= -1:
        y = x + 2
    else:
        y = 5 * x + 3
print(f'{y = }')
# === 範例 9 ===
"""
百分制成績轉換為等級製成績

Version: 1.0
Author: Kevin
"""
score = float(input('請輸入成績: '))
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'E'
print(f'{grade = }')
# === 範例 10 ===
"""
計算三角形的周長和麵積

Version: 1.0
Author: Kevin
"""
a = float(input('a = '))
b = float(input('b = '))
c = float(input('c = '))
if a + b > c and a + c > b and b + c > a:
    perimeter = a + b + c
    print(f'周長: {perimeter}')
    s = perimeter / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print(f'面積: {area}')
else:
    print('不能構成三角形')
