#!/usr/bin/env python3
"""
從 09.常用数据结构之列表-2.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
languages = ['Python', 'Java', 'C++']
languages.append('JavaScript')
print(languages)  # ['Python', 'Java', 'C++', 'JavaScript']
languages.insert(1, 'SQL')
print(languages)  # ['Python', 'SQL', 'Java', 'C++', 'JavaScript']
# === 範例 2 ===
languages = ['Python', 'SQL', 'Java', 'C++', 'JavaScript']
if 'Java' in languages:
    languages.remove('Java')
if 'Swift' in languages:
    languages.remove('Swift')
print(languages)  # ['Python', 'SQL', C++', 'JavaScript']
languages.pop()
temp = languages.pop(1)
print(temp)       # SQL
languages.append(temp)
print(languages)  # ['Python', C++', 'SQL']
languages.clear()
print(languages)  # []
# === 範例 3 ===
items = ['Python', 'Java', 'C++']
del items[1]
print(items)  # ['Python', 'C++']
# === 範例 4 ===
items = ['Python', 'Java', 'Java', 'C++', 'Kotlin', 'Python']
print(items.index('Python'))     # 0
# 從索引位置1開始查詢'Python'
print(items.index('Python', 1))  # 5
print(items.count('Python'))     # 2
print(items.count('Kotlin'))     # 1
print(items.count('Swfit'))      # 0
# 從索引位置3開始查詢'Java'
print(items.index('Java', 3))    # ValueError: 'Java' is not in list
# === 範例 5 ===
items = ['Python', 'Java', 'C++', 'Kotlin', 'Swift']
items.sort()
print(items)  # ['C++', 'Java', 'Kotlin', 'Python', 'Swift']
items.reverse()
print(items)  # ['Swift', 'Python', 'Kotlin', 'Java', 'C++']
# === 範例 6 ===
items = []
for i in range(1, 100):
    if i % 3 == 0 or i % 5 == 0:
        items.append(i)
print(items)
# === 範例 7 ===
items = [i for i in range(1, 100) if i % 3 == 0 or i % 5 == 0]
print(items)
# === 範例 8 ===
nums1 = [35, 12, 97, 64, 55]
nums2 = []
for num in nums1:
    nums2.append(num ** 2)
print(nums2)
# === 範例 9 ===
nums1 = [35, 12, 97, 64, 55]
nums2 = [num ** 2 for num in nums1]
print(nums2)
# === 範例 10 ===
nums1 = [35, 12, 97, 64, 55]
nums2 = []
for num in nums1:
    if num > 50:
        nums2.append(num)
print(nums2)
# === 範例 11 ===
nums1 = [35, 12, 97, 64, 55]
nums2 = [num for num in nums1 if num > 50]
print(nums2)
# === 範例 12 ===
scores = [[95, 83, 92], [80, 75, 82], [92, 97, 90], [80, 78, 69], [65, 66, 89]]
print(scores[0])
print(scores[0][1])
# === 範例 13 ===
scores = []
for _ in range(5):
    temp = []
    for _ in range(3):
        score = int(input('請輸入: '))
        temp.append(score)
    scores.append(temp)
print(scores)
# === 範例 14 ===
import random

scores = [[random.randrange(60, 101) for _ in range(3)] for _ in range(5)]
print(scores)
# === 範例 15 ===
"""
雙色球隨機選號程式

Author: Kevin
Version: 1.0
"""
import random

red_balls = list(range(1, 34))
selected_balls = []
# 新增6個紅色球到選中列表
for _ in range(6):
    # 生成隨機整數代表選中的紅色球的索引位置
    index = random.randrange(len(red_balls))
    # 將選中的球從紅色球列表中移除並新增到選中列表
    selected_balls.append(red_balls.pop(index))
# 對選中的紅色球排序
selected_balls.sort()
# 輸出選中的紅色球
for ball in selected_balls:
    print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
# 隨機選擇1個藍色球
blue_ball = random.randrange(1, 17)
# 輸出選中的藍色球
print(f'\033[034m{blue_ball:0>2d}\033[0m')
# === 範例 16 ===
"""
雙色球隨機選號程式

Author: Kevin
Version: 1.1
"""
import random

red_balls = [i for i in range(1, 34)]
blue_balls = [i for i in range(1, 17)]
# 從紅色球列表中隨機抽出6個紅色球（無放回抽樣）
selected_balls = random.sample(red_balls, 6)
# 對選中的紅色球排序
selected_balls.sort()
# 輸出選中的紅色球
for ball in selected_balls:
    print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
# 從藍色球列表中隨機抽出1個藍色球
blue_ball = random.choice(blue_balls)
# 輸出選中的藍色球
print(f'\033[034m{blue_ball:0>2d}\033[0m')
# === 範例 17 ===
"""
雙色球隨機選號程式

Author: Kevin
Version: 1.2
"""
import random

n = int(input('生成幾注號碼: '))
red_balls = [i for i in range(1, 34)]
blue_balls = [i for i in range(1, 17)]
for _ in range(n):
    # 從紅色球列表中隨機抽出6個紅色球（無放回抽樣）
    selected_balls = random.sample(red_balls, 6)
    # 對選中的紅色球排序
    selected_balls.sort()
    # 輸出選中的紅色球
    for ball in selected_balls:
        print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
    # 從藍色球列表中隨機抽出1個藍色球
    blue_ball = random.choice(blue_balls)
    # 輸出選中的藍色球
    print(f'\033[034m{blue_ball:0>2d}\033[0m')
# === 範例 18 ===
"""
雙色球隨機選號程式

Author: Kevin
Version: 1.3
"""
import random

from rich.console import Console
from rich.table import Table

# 建立控制檯
console = Console()

n = int(input('生成幾注號碼: '))
red_balls = [i for i in range(1, 34)]
blue_balls = [i for i in range(1, 17)]

# 建立表格並新增表頭
table = Table(show_header=True)
for col_name in ('序號', '紅球', '藍球'):
    table.add_column(col_name, justify='center')

for i in range(n):
    selected_balls = random.sample(red_balls, 6)
    selected_balls.sort()
    blue_ball = random.choice(blue_balls)
    # 向表格中新增行（序號，紅色球，藍色球）
    table.add_row(
        str(i + 1),
        f'[red]{" ".join([f"{ball:0>2d}" for ball in selected_balls])}[/red]',
        f'[blue]{blue_ball:0>2d}[/blue]'
    )

# 透過控制檯輸出表格
console.print(table)
