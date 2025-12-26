"""
不可變配置管理器 - Immutable Config Manager
============================================
進階應用：展示 Python 元組的特性與應用

功能：
1. 展示元組的不可變性
2. 作為字典鍵值
3. 函式多返回值
4. 命名元組應用
"""

from collections import namedtuple
from typing import Tuple


# ========================================
# 1. 使用元組定義常數配置
# ========================================

# 應用程式版本資訊（不可修改）
VERSION = (1, 0, 0)  # 主版本, 次版本, 修訂版

# 支援的檔案格式
SUPPORTED_FORMATS = ('jpg', 'png', 'gif', 'bmp', 'webp')

# RGB 顏色常數
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}

# 方向常數
DIRECTIONS = (
    ('north', 0, -1),
    ('south', 0, 1),
    ('east', 1, 0),
    ('west', -1, 0),
)


# ========================================
# 2. 命名元組 - 更可讀的元組
# ========================================

# 定義座標點
Point = namedtuple('Point', ['x', 'y'])

# 定義使用者資訊
User = namedtuple('User', ['id', 'name', 'email', 'role'])

# 定義商品
Product = namedtuple('Product', ['id', 'name', 'price', 'stock'])


# ========================================
# 3. 函式返回多個值（使用元組）
# ========================================

def get_min_max(numbers: list) -> Tuple[int, int]:
    """返回最小值和最大值"""
    return (min(numbers), max(numbers))


def get_statistics(numbers: list) -> Tuple[float, float, float]:
    """返回平均值、最小值、最大值"""
    avg = sum(numbers) / len(numbers)
    return (avg, min(numbers), max(numbers))


def divide_with_remainder(a: int, b: int) -> Tuple[int, int]:
    """返回商和餘數"""
    return (a // b, a % b)


def parse_fullname(fullname: str) -> Tuple[str, str]:
    """解析全名為姓和名"""
    parts = fullname.split()
    if len(parts) >= 2:
        return (parts[0], ' '.join(parts[1:]))
    return (fullname, '')


# ========================================
# 4. 元組作為字典鍵值
# ========================================

class ChessBoard:
    """棋盤 - 使用元組座標作為鍵"""

    def __init__(self):
        self.pieces = {}  # {(x, y): 'piece'}

    def place(self, x: int, y: int, piece: str):
        """放置棋子"""
        position = (x, y)  # 元組作為鍵
        self.pieces[position] = piece

    def get(self, x: int, y: int) -> str:
        """取得棋子"""
        return self.pieces.get((x, y), '.')

    def move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """移動棋子"""
        if from_pos in self.pieces:
            piece = self.pieces.pop(from_pos)
            self.pieces[to_pos] = piece
            return True
        return False

    def display(self, size: int = 8):
        """顯示棋盤"""
        print("\n  " + " ".join(str(i) for i in range(size)))
        for y in range(size):
            row = str(y) + " "
            for x in range(size):
                row += self.get(x, y) + " "
            print(row)


# ========================================
# 5. 展示元組不可變性
# ========================================

def demonstrate_immutability():
    """展示元組不可變性"""
    print("\n" + "=" * 50)
    print("  展示元組的不可變性")
    print("=" * 50)

    # 建立元組
    my_tuple = (1, 2, 3, 4, 5)
    print(f"\n原始元組: {my_tuple}")

    # 嘗試修改會報錯
    print("\n嘗試修改元組...")
    try:
        my_tuple[0] = 100
    except TypeError as e:
        print(f"❌ 錯誤: {e}")
        print("   元組是不可變的，無法修改元素！")

    # 但可以重新賦值
    print("\n重新賦值（創建新元組）...")
    my_tuple = my_tuple + (6, 7)
    print(f"新元組: {my_tuple}")

    # 元組中的可變物件
    print("\n元組中包含可變物件（列表）...")
    mixed = (1, 2, [3, 4])
    print(f"原始: {mixed}")
    mixed[2].append(5)  # 可以修改列表內容
    print(f"修改列表後: {mixed}")
    print("⚠️ 注意：元組中的列表內容可以修改！")


# ========================================
# 主程式
# ========================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║          不可變配置管理器 v1.0                         ║
║           展示 Python 元組的特性                       ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print("""
【選單】
  1. 查看系統常數配置
  2. 命名元組示範
  3. 多返回值函式
  4. 棋盤遊戲（元組作為鍵）
  5. 元組不可變性展示
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n📋 系統常數配置")
            print("=" * 50)
            print(f"\n版本號: {'.'.join(map(str, VERSION))}")
            print(f"版本元組: {VERSION}")
            print(f"\n支援的圖片格式: {SUPPORTED_FORMATS}")
            print(f"\n顏色定義:")
            for name, rgb in COLORS.items():
                print(f"  {name}: RGB{rgb}")
            print(f"\n方向定義:")
            for name, dx, dy in DIRECTIONS:
                print(f"  {name}: ({dx}, {dy})")

        elif choice == '2':
            print("\n👤 命名元組示範")
            print("=" * 50)

            # 建立使用者
            user = User(1, "王小明", "ming@email.com", "admin")
            print(f"\n使用者: {user}")
            print(f"姓名: {user.name}")  # 可用名稱存取
            print(f"Email: {user.email}")

            # 建立商品
            products = [
                Product(1, "筆電", 35000, 10),
                Product(2, "滑鼠", 500, 50),
                Product(3, "鍵盤", 1200, 30),
            ]

            print("\n商品列表:")
            for p in products:
                print(f"  {p.id}. {p.name}: ${p.price} (庫存: {p.stock})")

            # 座標點
            p1 = Point(3, 4)
            p2 = Point(6, 8)
            print(f"\n座標點: P1{p1}, P2{p2}")

            # 計算距離
            distance = ((p2.x - p1.x)**2 + (p2.y - p1.y)**2) ** 0.5
            print(f"兩點距離: {distance:.2f}")

        elif choice == '3':
            print("\n🔢 多返回值函式")
            print("=" * 50)

            numbers = [23, 45, 12, 67, 89, 34, 56]
            print(f"\n數字列表: {numbers}")

            # 解包元組返回值
            min_val, max_val = get_min_max(numbers)
            print(f"最小值: {min_val}, 最大值: {max_val}")

            avg, min_v, max_v = get_statistics(numbers)
            print(f"統計: 平均={avg:.1f}, 最小={min_v}, 最大={max_v}")

            a, b = 17, 5
            quotient, remainder = divide_with_remainder(a, b)
            print(f"\n{a} ÷ {b} = {quotient} 餘 {remainder}")

            fullname = "王 小明"
            last, first = parse_fullname(fullname)
            print(f"\n解析姓名 '{fullname}': 姓={last}, 名={first}")

        elif choice == '4':
            print("\n♟️ 棋盤遊戲（元組作為字典鍵）")
            print("=" * 50)

            board = ChessBoard()

            # 初始化一些棋子
            board.place(0, 0, '♜')
            board.place(7, 0, '♜')
            board.place(4, 0, '♚')
            board.place(3, 0, '♛')
            for i in range(8):
                board.place(i, 1, '♟')

            board.place(4, 7, '♔')
            board.place(3, 7, '♕')
            for i in range(8):
                board.place(i, 6, '♙')

            print("\n初始棋盤:")
            board.display()

            print("\n移動棋子 (1,1) -> (1,3)")
            board.move((1, 1), (1, 3))
            board.display()

        elif choice == '5':
            demonstrate_immutability()

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
