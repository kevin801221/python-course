"""
函式和模組 - 進階練習解答
==========================
"""

import math

# ============================================================
# 練習 1：基本函式（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：基本函式】")
print("=" * 40)


def greet(name):
    """返回問候語"""
    return f"Hello, {name}!"


def add(a, b):
    """返回兩數之和"""
    return a + b


def is_even(n):
    """判斷是否為偶數"""
    return n % 2 == 0


def factorial(n):
    """計算階乘"""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print(f'greet("Alice") → {greet("Alice")}')
print(f'add(3, 5) → {add(3, 5)}')
print(f'is_even(4) → {is_even(4)}')
print(f'factorial(5) → {factorial(5)}')


# ============================================================
# 練習 2：預設參數和關鍵字參數（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：預設參數和關鍵字參數】")
print("=" * 40)


def format_name(first_name, last_name, uppercase=False, reverse=False):
    """格式化姓名"""
    if reverse:
        full_name = f"{last_name} {first_name}"
    else:
        full_name = f"{first_name} {last_name}"

    if uppercase:
        full_name = full_name.upper()

    return full_name


print(f'format_name("John", "Doe") → {format_name("John", "Doe")}')
print(f'format_name("John", "Doe", uppercase=True) → {format_name("John", "Doe", uppercase=True)}')
print(f'format_name("John", "Doe", reverse=True) → {format_name("John", "Doe", reverse=True)}')


# ============================================================
# 練習 3：可變參數（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：可變參數】")
print("=" * 40)


def sum_all(*args):
    """計算所有參數的總和"""
    return sum(args)


def build_profile(name, **kwargs):
    """建立個人檔案字典"""
    profile = {'name': name}
    profile.update(kwargs)
    return profile


print(f'sum_all(1, 2, 3, 4, 5) → {sum_all(1, 2, 3, 4, 5)}')
print(f'build_profile("Alice", age=25, city="Taipei")')
print(f'→ {build_profile("Alice", age=25, city="Taipei")}')


# ============================================================
# 練習 4：遞迴函式（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 4：遞迴函式】")
print("=" * 40)


def fibonacci(n):
    """返回費波那契數列第 n 項（使用記憶化優化）"""
    if n <= 1:
        return n
    if n <= 2:
        return 1

    # 使用迭代避免遞迴深度問題
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b


def sum_digits(n):
    """計算數字各位數之和（遞迴）"""
    n = abs(n)
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


def binary(n):
    """將十進位轉二進位（遞迴）"""
    if n == 0:
        return "0"
    if n == 1:
        return "1"
    return binary(n // 2) + str(n % 2)


print(f'fibonacci(10) → {fibonacci(10)}')
print(f'sum_digits(12345) → {sum_digits(12345)}')
print(f'binary(10) → {binary(10)}')


# ============================================================
# 練習 5：計算機模組（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 5：計算機模組】")
print("=" * 40)


class Calculator:
    """計算機模組"""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("除數不能為零")
        return a / b

    @staticmethod
    def power(base, exp):
        return base ** exp

    @staticmethod
    def sqrt(n):
        if n < 0:
            raise ValueError("不能對負數開根號")
        return math.sqrt(n)

    @staticmethod
    def absolute(n):
        return abs(n)

    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def factorial(n):
        if n < 0:
            raise ValueError("不能計算負數的階乘")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def gcd(a, b):
        """最大公因數"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a, b):
        """最小公倍數"""
        return abs(a * b) // Calculator.gcd(a, b)


calculator = Calculator()

print(f'calculator.add(10, 5) → {calculator.add(10, 5)}')
print(f'calculator.power(2, 10) → {calculator.power(2, 10)}')
print(f'calculator.is_prime(17) → {calculator.is_prime(17)}')
print(f'calculator.gcd(48, 18) → {calculator.gcd(48, 18)}')
print(f'calculator.lcm(12, 18) → {calculator.lcm(12, 18)}')


# ============================================================
# 【函式語法整理】
# ============================================================
"""
【定義函式】
def function_name(parameters):
    '''文件字串'''
    # 函式內容
    return value

【參數類型】
1. 位置參數：def f(a, b)
2. 預設參數：def f(a, b=10)
3. 可變位置參數：def f(*args)
4. 可變關鍵字參數：def f(**kwargs)
5. 僅限關鍵字參數：def f(*, a, b)

【返回值】
return value        返回單一值
return a, b         返回多個值（元組）
無 return          返回 None

【文件字串】
def f():
    '''這是函式說明'''
    pass

f.__doc__  # 取得文件字串

【Lambda 表達式】
lambda x: x ** 2
相當於
def f(x):
    return x ** 2
"""
