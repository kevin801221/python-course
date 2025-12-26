"""
裝飾器工具箱 - Decorator Toolkit
=================================
進階應用：展示 Python 裝飾器與閉包

功能：
1. 閉包 (Closure) 示範
2. 裝飾器 (Decorator) 設計
3. 帶參數的裝飾器
4. 實用裝飾器庫
"""

import time
import functools
from typing import Callable, Any
from datetime import datetime


# ========================================
# 1. 閉包 (Closure) 示範
# ========================================

def make_counter(start: int = 0) -> Callable:
    """
    計數器工廠 - 閉包示範

    閉包：內部函式記住外部函式的變數
    """
    count = start

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def make_multiplier(factor: int) -> Callable:
    """乘法器工廠"""
    def multiply(x):
        return x * factor
    return multiply


def make_power(exponent: int) -> Callable:
    """次方工廠"""
    def power(base):
        return base ** exponent
    return power


def make_accumulator(initial: float = 0) -> Callable:
    """累加器"""
    total = initial

    def add(value):
        nonlocal total
        total += value
        return total

    return add


def make_logger(prefix: str = "LOG") -> Callable:
    """日誌記錄器工廠"""
    logs = []

    def log(message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{prefix}][{timestamp}] {message}"
        logs.append(entry)
        print(entry)

    def get_logs():
        return logs.copy()

    log.get_logs = get_logs
    return log


# ========================================
# 2. 基本裝飾器
# ========================================

def timer(func: Callable) -> Callable:
    """計時裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ {func.__name__} 執行時間: {end - start:.4f} 秒")
        return result
    return wrapper


def debug(func: Callable) -> Callable:
    """除錯裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"🔍 呼叫 {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"🔍 {func.__name__} 返回: {result!r}")
        return result
    return wrapper


def log_call(func: Callable) -> Callable:
    """記錄呼叫裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 [{timestamp}] 呼叫 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def deprecated(func: Callable) -> Callable:
    """標記為過時"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"⚠️ 警告: {func.__name__} 已過時，請使用新版本！")
        return func(*args, **kwargs)
    return wrapper


def singleton(cls):
    """單例模式裝飾器（裝飾類別）"""
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# ========================================
# 3. 帶參數的裝飾器
# ========================================

def repeat(times: int = 2):
    """重複執行裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                print(f"🔄 第 {i+1}/{times} 次執行")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0):
    """重試裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"❌ 第 {attempt+1} 次失敗: {e}")
                    if attempt < max_attempts - 1:
                        print(f"⏳ {delay} 秒後重試...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def cache(max_size: int = 128):
    """快取裝飾器"""
    def decorator(func):
        cache_dict = {}
        call_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in cache_dict:
                print(f"💾 快取命中: {args}")
                return cache_dict[args]

            result = func(*args)
            cache_dict[args] = result
            call_order.append(args)

            # LRU 清理
            while len(cache_dict) > max_size:
                oldest = call_order.pop(0)
                del cache_dict[oldest]

            return result

        wrapper.cache_info = lambda: f"快取大小: {len(cache_dict)}/{max_size}"
        wrapper.cache_clear = lambda: cache_dict.clear()
        return wrapper

    return decorator


def validate_args(*validators):
    """參數驗證裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i, (arg, validator) in enumerate(zip(args, validators)):
                if not validator(arg):
                    raise ValueError(f"參數 {i} 驗證失敗: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(calls: int, period: float):
    """限流裝飾器"""
    timestamps = []

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理過期記錄
            while timestamps and timestamps[0] < now - period:
                timestamps.pop(0)

            if len(timestamps) >= calls:
                wait = period - (now - timestamps[0])
                print(f"🚫 限流中，請等待 {wait:.1f} 秒")
                return None

            timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ========================================
# 4. 實用範例
# ========================================

@timer
def slow_function():
    """模擬慢函式"""
    time.sleep(0.1)
    return "完成"


@debug
def add(a, b):
    """加法"""
    return a + b


@repeat(times=3)
def greet(name):
    """打招呼"""
    print(f"Hello, {name}!")


@cache(max_size=100)
def fibonacci(n):
    """費波那契（帶快取）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@validate_args(lambda x: x > 0, lambda y: y > 0)
def divide(x, y):
    """安全除法"""
    return x / y


# ========================================
# 主程式
# ========================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║             裝飾器工具箱 v1.0                          ║
║           展示 Python 裝飾器與閉包                     ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print("""
【選單】
  1. 閉包示範         2. 基本裝飾器
  3. 帶參數裝飾器     4. 效能快取
  5. 實用範例         0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n🔒 閉包 (Closure) 示範")
            print("=" * 50)

            # 計數器
            print("\n【計數器工廠】")
            counter1 = make_counter(0)
            counter2 = make_counter(100)

            print(f"計數器1: {counter1()}, {counter1()}, {counter1()}")
            print(f"計數器2: {counter2()}, {counter2()}, {counter2()}")

            # 乘法器
            print("\n【乘法器工廠】")
            double = make_multiplier(2)
            triple = make_multiplier(3)

            print(f"double(5) = {double(5)}")
            print(f"triple(5) = {triple(5)}")

            # 次方
            print("\n【次方工廠】")
            square = make_power(2)
            cube = make_power(3)

            print(f"square(4) = {square(4)}")
            print(f"cube(4) = {cube(4)}")

            # 累加器
            print("\n【累加器】")
            acc = make_accumulator(0)
            print(f"累加: {acc(10)}, {acc(20)}, {acc(30)}")

        elif choice == '2':
            print("\n🎀 基本裝飾器")
            print("=" * 50)

            print("\n【計時裝飾器 @timer】")
            slow_function()

            print("\n【除錯裝飾器 @debug】")
            add(3, 5)
            add(10, b=20)

            print("\n【過時標記 @deprecated】")
            @deprecated
            def old_function():
                return "舊功能"
            old_function()

        elif choice == '3':
            print("\n🎯 帶參數的裝飾器")
            print("=" * 50)

            print("\n【重複執行 @repeat(times=3)】")
            greet("Python")

            print("\n【參數驗證 @validate_args】")
            try:
                print(f"divide(10, 2) = {divide(10, 2)}")
                print("嘗試 divide(-1, 2)...")
                divide(-1, 2)
            except ValueError as e:
                print(f"❌ 錯誤: {e}")

            print("\n【重試裝飾器 @retry】")
            @retry(max_attempts=3, delay=0.5)
            def unstable_function():
                import random
                if random.random() < 0.7:
                    raise Exception("隨機失敗")
                return "成功！"

            try:
                result = unstable_function()
                print(f"✅ 結果: {result}")
            except:
                print("❌ 所有重試都失敗")

        elif choice == '4':
            print("\n💾 效能快取")
            print("=" * 50)

            # 清除之前的快取
            fibonacci.cache_clear()

            print("計算 fibonacci(30)...")
            start = time.perf_counter()
            result = fibonacci(30)
            elapsed = time.perf_counter() - start
            print(f"結果: {result}")
            print(f"時間: {elapsed:.4f} 秒")
            print(fibonacci.cache_info())

            print("\n再次計算 fibonacci(30)（使用快取）...")
            start = time.perf_counter()
            result = fibonacci(30)
            elapsed = time.perf_counter() - start
            print(f"結果: {result}")
            print(f"時間: {elapsed:.6f} 秒")

            print("\n計算 fibonacci(35)（部分使用快取）...")
            start = time.perf_counter()
            result = fibonacci(35)
            elapsed = time.perf_counter() - start
            print(f"結果: {result}")
            print(f"時間: {elapsed:.4f} 秒")
            print(fibonacci.cache_info())

        elif choice == '5':
            print("\n🛠️ 實用範例")
            print("=" * 50)

            # 日誌記錄器
            print("\n【日誌記錄器（閉包）】")
            app_log = make_logger("APP")
            db_log = make_logger("DB")

            app_log("應用程式啟動")
            db_log("連接資料庫")
            app_log("初始化完成")

            print(f"\n應用程式日誌數: {len(app_log.get_logs())}")

            # 限流
            print("\n【限流裝飾器】")
            @rate_limit(calls=3, period=5.0)
            def api_call():
                print("✅ API 呼叫成功")
                return True

            for i in range(5):
                print(f"\n第 {i+1} 次呼叫:")
                api_call()

            # 單例模式
            print("\n【單例模式裝飾器】")
            @singleton
            class Database:
                def __init__(self):
                    self.id = id(self)
                    print(f"Database 建立: {self.id}")

            db1 = Database()
            db2 = Database()
            print(f"db1.id: {db1.id}")
            print(f"db2.id: {db2.id}")
            print(f"db1 is db2: {db1 is db2}")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
