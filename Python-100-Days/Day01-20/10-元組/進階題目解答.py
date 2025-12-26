"""
元組 - 進階練習解答
====================
"""

import math

# ============================================================
# 練習 1：元組基本操作（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：元組基本操作】")
print("=" * 40)

# 建立元組
fruits = ('蘋果', '香蕉', '橘子', '葡萄', '西瓜')
print(f"水果元組：{fruits}")

# 索引
print(f"第一個水果：{fruits[0]}")
print(f"最後一個水果：{fruits[-1]}")

# 切片
print(f"前三個水果：{fruits[:3]}")

# 長度
print(f"元組長度：{len(fruits)}")

# 成員檢查
print(f"香蕉在元組中嗎？{'香蕉' in fruits}")


# ============================================================
# 練習 2：元組解包（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：元組解包】")
print("=" * 40)

# 交換變數
a, b = 10, 20
print(f"交換前：a={a}, b={b}")

a, b = b, a  # 元組解包交換
print(f"交換後：a={a}, b={b}")

# 函式返回多個值
def get_coordinates():
    return (3, 4)  # 返回元組

coord = get_coordinates()
print(f"\n座標：{coord}")

x, y = get_coordinates()  # 元組解包
print(f"x={x}, y={y}")


# ============================================================
# 練習 3：不可變設定檔（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：不可變設定檔】")
print("=" * 40)

# 資料庫設定（使用元組確保不被修改）
DB_CONFIG = ('localhost', 3306, 'my_database')
db_host, db_port, db_name = DB_CONFIG

print("【資料庫設定】")
print(f"主機：{db_host}")
print(f"連接埠：{db_port}")
print(f"資料庫：{db_name}")

# 應用程式設定
APP_CONFIG = ('My App', '1.0.0', 'Kevin')
app_name, app_version, app_author = APP_CONFIG

print("\n【應用程式設定】")
print(f"名稱：{app_name}")
print(f"版本：{app_version}")
print(f"作者：{app_author}")


# ============================================================
# 練習 4：座標計算器（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：座標計算器】")
print("=" * 40)

# 定義兩個點
point_a = (0, 0)
point_b = (3, 4)

print(f"點 A：{point_a}")
print(f"點 B：{point_b}")

# 計算距離
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

dist = distance(point_a, point_b)
print(f"兩點距離：{dist}")

# 計算中點
def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

mid = midpoint(point_a, point_b)
print(f"中點座標：{mid}")

# 計算重心
def centroid(points):
    n = len(points)
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    return (sum_x / n, sum_y / n)

points = [(0, 0), (3, 0), (0, 4)]
print("\n三個點的重心：")
for i, p in enumerate(points, 1):
    print(f"點 {i}：{p}")

center = centroid(points)
print(f"重心：({center[0]:.2f}, {center[1]:.2f})")


# ============================================================
# 【元組 vs 列表】
# ============================================================
"""
【元組特性】
1. 不可變（immutable）：建立後不能修改
2. 使用小括號 () 或直接用逗號分隔
3. 可以作為字典的鍵（因為不可變）
4. 比列表更節省記憶體

【使用時機】
- 不需要修改的資料（座標、設定）
- 函式返回多個值
- 字典的鍵
- 保護資料不被意外修改

【元組方法】
tuple.count(x)  計算 x 出現的次數
tuple.index(x)  返回 x 的索引

【元組解包】
x, y = (1, 2)
a, b, c = (1, 2, 3)
first, *rest = (1, 2, 3, 4, 5)  # first=1, rest=[2,3,4,5]
"""
