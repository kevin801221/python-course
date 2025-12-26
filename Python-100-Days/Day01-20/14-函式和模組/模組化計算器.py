"""
模組化計算器 - Modular Calculator
==================================
進階應用：展示 Python 函式和模組的設計

功能：
1. 函式定義與呼叫
2. 參數處理（預設值、關鍵字參數）
3. 模組化設計
4. 數學運算庫
"""

import math
from typing import Union, List, Callable

Number = Union[int, float]


# ========================================
# 1. 基本數學運算模組
# ========================================

def add(a: Number, b: Number) -> Number:
    """加法"""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """減法"""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """乘法"""
    return a * b


def divide(a: Number, b: Number) -> float:
    """除法"""
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b


def power(base: Number, exponent: Number = 2) -> Number:
    """次方（預設平方）"""
    return base ** exponent


def sqrt(n: Number) -> float:
    """平方根"""
    if n < 0:
        raise ValueError("不能對負數取平方根")
    return math.sqrt(n)


def modulo(a: int, b: int) -> int:
    """取餘數"""
    if b == 0:
        raise ValueError("除數不能為零")
    return a % b


def floor_divide(a: Number, b: Number) -> int:
    """整除"""
    if b == 0:
        raise ValueError("除數不能為零")
    return int(a // b)


# ========================================
# 2. 進階數學函式
# ========================================

def factorial(n: int) -> int:
    """階乘（使用遞迴）"""
    if n < 0:
        raise ValueError("階乘不接受負數")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """費波那契數列第 n 項"""
    if n < 0:
        raise ValueError("不接受負數")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def gcd(a: int, b: int) -> int:
    """最大公因數（歐幾里得演算法）"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """最小公倍數"""
    return abs(a * b) // gcd(a, b)


def is_prime(n: int) -> bool:
    """判斷質數"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factors(n: int) -> List[int]:
    """質因數分解"""
    if n < 2:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


# ========================================
# 3. 統計函式
# ========================================

def mean(numbers: List[Number]) -> float:
    """平均值"""
    if not numbers:
        raise ValueError("列表不能為空")
    return sum(numbers) / len(numbers)


def median(numbers: List[Number]) -> Number:
    """中位數"""
    if not numbers:
        raise ValueError("列表不能為空")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]


def mode(numbers: List[Number]) -> Number:
    """眾數"""
    if not numbers:
        raise ValueError("列表不能為空")
    count = {}
    for n in numbers:
        count[n] = count.get(n, 0) + 1
    return max(count, key=count.get)


def variance(numbers: List[Number]) -> float:
    """變異數"""
    if len(numbers) < 2:
        raise ValueError("至少需要兩個數")
    avg = mean(numbers)
    return sum((x - avg) ** 2 for x in numbers) / len(numbers)


def std_dev(numbers: List[Number]) -> float:
    """標準差"""
    return math.sqrt(variance(numbers))


# ========================================
# 4. 高階函式應用
# ========================================

def apply_operation(numbers: List[Number], operation: Callable) -> List[Number]:
    """對列表每個元素應用函式"""
    return [operation(n) for n in numbers]


def reduce_operation(numbers: List[Number], operation: Callable, initial: Number = 0) -> Number:
    """將列表歸約為單一值"""
    result = initial
    for n in numbers:
        result = operation(result, n)
    return result


def compose(*functions: Callable) -> Callable:
    """函式組合"""
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed


# ========================================
# 5. 計算器類別
# ========================================

class Calculator:
    """模組化計算器"""

    def __init__(self):
        self.history = []
        self.memory = 0
        self.operations = {
            '+': add,
            '-': subtract,
            '*': multiply,
            '/': divide,
            '^': power,
            '%': modulo,
            '//': floor_divide,
        }

    def calculate(self, expression: str) -> Number:
        """計算表達式"""
        # 簡單解析器
        expression = expression.replace(' ', '')

        # 處理二元運算
        for op in ['//'] + list('+-*/%^'):
            if op in expression:
                parts = expression.split(op, 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    a = float(parts[0])
                    b = float(parts[1])
                    result = self.operations[op](a, b)
                    self.history.append(f"{a} {op} {b} = {result}")
                    return result

        # 處理單一數字
        return float(expression)

    def memory_store(self, value: Number):
        """儲存到記憶體"""
        self.memory = value

    def memory_recall(self) -> Number:
        """取回記憶體"""
        return self.memory

    def memory_clear(self):
        """清除記憶體"""
        self.memory = 0

    def show_history(self):
        """顯示歷史記錄"""
        return self.history[-10:]  # 最近 10 筆


# ========================================
# 主程式
# ========================================

def main():
    calc = Calculator()

    print("""
╔══════════════════════════════════════════════════════╗
║             模組化計算器 v1.0                          ║
║           展示 Python 函式與模組設計                    ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print("""
【選單】
  1. 基本計算        2. 進階數學
  3. 統計分析        4. 質數工具
  5. 記憶體操作      6. 歷史記錄
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n🔢 基本計算")
            print("=" * 40)
            print("支援運算: + - * / ^ % //")
            print("範例: 10 + 5, 2 ^ 8, 17 % 5")

            expr = input("\n輸入算式: ").strip()
            if expr:
                try:
                    result = calc.calculate(expr)
                    print(f"結果: {result}")
                except Exception as e:
                    print(f"❌ 錯誤: {e}")

        elif choice == '2':
            print("\n📐 進階數學")
            print("=" * 40)
            print("""
  1. 階乘 (n!)      2. 費波那契
  3. 平方根         4. 次方
  5. 最大公因數     6. 最小公倍數
""")
            sub = input("選擇: ").strip()

            try:
                if sub == '1':
                    n = int(input("輸入 n: "))
                    print(f"{n}! = {factorial(n)}")

                elif sub == '2':
                    n = int(input("第幾項: "))
                    print(f"F({n}) = {fibonacci(n)}")
                    print(f"數列: {[fibonacci(i) for i in range(n+1)]}")

                elif sub == '3':
                    n = float(input("輸入數字: "))
                    print(f"√{n} = {sqrt(n):.6f}")

                elif sub == '4':
                    base = float(input("底數: "))
                    exp = float(input("指數: "))
                    print(f"{base}^{exp} = {power(base, exp)}")

                elif sub == '5':
                    a = int(input("數字 a: "))
                    b = int(input("數字 b: "))
                    print(f"GCD({a}, {b}) = {gcd(a, b)}")

                elif sub == '6':
                    a = int(input("數字 a: "))
                    b = int(input("數字 b: "))
                    print(f"LCM({a}, {b}) = {lcm(a, b)}")

            except Exception as e:
                print(f"❌ 錯誤: {e}")

        elif choice == '3':
            print("\n📊 統計分析")
            print("=" * 40)

            data_input = input("輸入數字（空格分隔）: ").strip()
            if not data_input:
                data_input = "10 20 30 40 50 60 70 80 90"
                print(f"使用範例資料: {data_input}")

            try:
                numbers = [float(x) for x in data_input.split()]

                print(f"\n資料: {numbers}")
                print(f"數量: {len(numbers)}")
                print(f"總和: {sum(numbers)}")
                print(f"最小: {min(numbers)}")
                print(f"最大: {max(numbers)}")
                print(f"平均: {mean(numbers):.2f}")
                print(f"中位: {median(numbers):.2f}")
                print(f"眾數: {mode(numbers)}")

                if len(numbers) >= 2:
                    print(f"變異: {variance(numbers):.2f}")
                    print(f"標差: {std_dev(numbers):.2f}")

            except Exception as e:
                print(f"❌ 錯誤: {e}")

        elif choice == '4':
            print("\n🔍 質數工具")
            print("=" * 40)
            print("""
  1. 判斷質數
  2. 質因數分解
  3. 找出範圍內質數
""")
            sub = input("選擇: ").strip()

            try:
                if sub == '1':
                    n = int(input("輸入數字: "))
                    if is_prime(n):
                        print(f"✅ {n} 是質數")
                    else:
                        print(f"❌ {n} 不是質數")

                elif sub == '2':
                    n = int(input("輸入數字: "))
                    factors = prime_factors(n)
                    print(f"{n} = {' × '.join(map(str, factors))}")

                elif sub == '3':
                    start = int(input("起始: "))
                    end = int(input("結束: "))
                    primes = [n for n in range(start, end + 1) if is_prime(n)]
                    print(f"質數: {primes}")
                    print(f"共 {len(primes)} 個")

            except Exception as e:
                print(f"❌ 錯誤: {e}")

        elif choice == '5':
            print("\n💾 記憶體操作")
            print("=" * 40)
            print(f"目前記憶體: {calc.memory}")
            print("""
  1. 儲存 (MS)
  2. 取回 (MR)
  3. 清除 (MC)
""")
            sub = input("選擇: ").strip()

            if sub == '1':
                try:
                    value = float(input("儲存值: "))
                    calc.memory_store(value)
                    print(f"✅ 已儲存 {value}")
                except ValueError:
                    print("❌ 請輸入數字")

            elif sub == '2':
                print(f"記憶體: {calc.memory_recall()}")

            elif sub == '3':
                calc.memory_clear()
                print("✅ 記憶體已清除")

        elif choice == '6':
            print("\n📜 歷史記錄")
            print("=" * 40)
            history = calc.show_history()
            if history:
                for i, record in enumerate(history, 1):
                    print(f"  {i}. {record}")
            else:
                print("  (無記錄)")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
