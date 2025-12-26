"""
函式進階 - 進階練習解答
========================
"""

import time
import functools
import warnings

# ============================================================
# 練習 1：閉包基礎（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：閉包基礎】")
print("=" * 40)


def counter():
    """計數器閉包"""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


def multiplier(n):
    """乘法器閉包"""
    def multiply(x):
        return x * n
    return multiply


def power_of(exp):
    """次方計算閉包"""
    def power(base):
        return base ** exp
    return power


# 測試
c = counter()
print(f"c() → {c()}")
print(f"c() → {c()}")
print(f"c() → {c()}")

double = multiplier(2)
print(f"\ndouble(5) → {double(5)}")

square = power_of(2)
print(f"square(5) → {square(5)}")


# ============================================================
# 練習 2：基礎裝飾器（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：基礎裝飾器】")
print("=" * 40)


def timer(func):
    """計時裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 執行時間：{end - start:.4f} 秒")
        return result
    return wrapper


def logger(func):
    """日誌裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"呼叫 {func.__name__}，參數：{args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回：{result}")
        return result
    return wrapper


def repeat(n):
    """重複執行裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@timer
def slow_function():
    time.sleep(0.1)
    return "完成"


@logger
def add(a, b):
    return a + b


@repeat(3)
def greet(name):
    return f"Hello, {name}!"


print("測試 @timer:")
slow_function()

print("\n測試 @logger:")
add(3, 5)

print("\n測試 @repeat(3):")
print(greet("Alice"))


# ============================================================
# 練習 3：帶參數的裝飾器（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：帶參數的裝飾器】")
print("=" * 40)


def validate_type(*types):
    """類型驗證裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"預期 {expected_type}，但得到 {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache(func):
    """快取裝飾器"""
    cached = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper


def retry(times=3, delay=0.1):
    """重試裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"第 {i + 1} 次嘗試失敗：{e}")
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


@validate_type(int, int)
def safe_add(a, b):
    return a + b


print("測試 @validate_type:")
print(f"safe_add(1, 2) → {safe_add(1, 2)}")

try:
    safe_add("1", 2)
except TypeError as e:
    print(f"safe_add('1', 2) → TypeError: {e}")


@cache
def expensive_calculation(n):
    print(f"計算 {n}...")
    time.sleep(0.1)
    return n * n


print("\n測試 @cache:")
print(f"expensive_calculation(5) → {expensive_calculation(5)}")
print(f"expensive_calculation(5) → {expensive_calculation(5)} (從快取)")


# ============================================================
# 練習 4：實用裝飾器（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：實用裝飾器】")
print("=" * 40)


def singleton(cls):
    """單例模式裝飾器"""
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def memoize(func):
    """記憶化裝飾器（支援遞迴）"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def deprecated(message="此函式已棄用"):
    """棄用警告裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(f"{func.__name__}: {message}", DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@singleton
class Database:
    def __init__(self):
        self.id = id(self)
        print(f"建立 Database 實例：{self.id}")


print("測試 @singleton:")
db1 = Database()
db2 = Database()
print(f"db1 is db2 → {db1 is db2}")


@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("\n測試 @memoize:")
start = time.time()
result = fibonacci(35)
end = time.time()
print(f"fibonacci(35) → {result}，耗時：{end - start:.4f} 秒")


# ============================================================
# 【裝飾器語法整理】
# ============================================================
"""
【基本裝飾器】
def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 前處理
        result = func(*args, **kwargs)
        # 後處理
        return result
    return wrapper

【帶參數的裝飾器】
def decorator_with_args(arg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

【類別裝飾器】
class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

【常用裝飾器】
@property          屬性裝飾器
@staticmethod      靜態方法
@classmethod       類別方法
@functools.wraps   保留原函式資訊
@functools.lru_cache  內建快取
"""
