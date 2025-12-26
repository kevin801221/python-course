"""
函式式程式設計工具 - Functional Programming Tools
==================================================
進階應用：展示 Python 函式式程式設計

功能：
1. Lambda 表達式
2. map, filter, reduce
3. 高階函式
4. 函式組合
"""

from functools import reduce, partial
from typing import Callable, List, Any, TypeVar
from operator import add, mul, sub
import itertools

T = TypeVar('T')


# ========================================
# 1. Lambda 表達式工具
# ========================================

# 基本 Lambda 範例
square = lambda x: x ** 2
cube = lambda x: x ** 3
double = lambda x: x * 2
is_even = lambda x: x % 2 == 0
is_positive = lambda x: x > 0
to_upper = lambda s: s.upper()
to_lower = lambda s: s.lower()


def lambda_calculator():
    """Lambda 計算機"""
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf'),
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b if b != 0 else 0,
    }
    return operations


# ========================================
# 2. Map, Filter, Reduce 進階應用
# ========================================

def transform_data(data: List, *transformations: Callable) -> List:
    """連續轉換資料"""
    result = data
    for transform in transformations:
        result = list(map(transform, result))
    return result


def filter_chain(data: List, *conditions: Callable) -> List:
    """連續過濾"""
    result = data
    for condition in conditions:
        result = list(filter(condition, result))
    return result


def multi_reduce(data: List, *reducers: tuple) -> dict:
    """多重歸約"""
    results = {}
    for name, reducer, initial in reducers:
        results[name] = reduce(reducer, data, initial)
    return results


def group_by(data: List, key_func: Callable) -> dict:
    """按鍵分組"""
    groups = {}
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups


def partition(data: List, predicate: Callable) -> tuple:
    """根據條件分割"""
    true_items = list(filter(predicate, data))
    false_items = list(filter(lambda x: not predicate(x), data))
    return true_items, false_items


# ========================================
# 3. 高階函式
# ========================================

def compose(*functions: Callable) -> Callable:
    """函式組合（從右到左）"""
    def inner(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return inner


def pipe(*functions: Callable) -> Callable:
    """函式管道（從左到右）"""
    def inner(x):
        result = x
        for f in functions:
            result = f(result)
        return result
    return inner


def curry(func: Callable, arity: int = None) -> Callable:
    """柯里化"""
    if arity is None:
        arity = func.__code__.co_argcount

    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        return lambda *more: curried(*(args + more))

    return curried


def flip(func: Callable) -> Callable:
    """翻轉參數順序"""
    return lambda a, b: func(b, a)


def memoize(func: Callable) -> Callable:
    """記憶化"""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def identity(x: T) -> T:
    """恆等函式"""
    return x


def constantly(value: T) -> Callable:
    """常數函式"""
    return lambda *args, **kwargs: value


def complement(predicate: Callable) -> Callable:
    """補集（否定）"""
    return lambda *args, **kwargs: not predicate(*args, **kwargs)


# ========================================
# 4. 實用工具函式
# ========================================

def take(n: int, iterable) -> List:
    """取前 n 個元素"""
    return list(itertools.islice(iterable, n))


def drop(n: int, iterable) -> List:
    """丟棄前 n 個元素"""
    return list(itertools.islice(iterable, n, None))


def take_while(predicate: Callable, iterable) -> List:
    """取滿足條件的元素（直到不滿足為止）"""
    return list(itertools.takewhile(predicate, iterable))


def drop_while(predicate: Callable, iterable) -> List:
    """丟棄滿足條件的元素"""
    return list(itertools.dropwhile(predicate, iterable))


def flatten(nested: List) -> List:
    """扁平化巢狀列表"""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def zip_with(func: Callable, *iterables) -> List:
    """用函式合併多個列表"""
    return [func(*items) for items in zip(*iterables)]


def unique(iterable) -> List:
    """去重（保持順序）"""
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def frequencies(iterable) -> dict:
    """計算頻率"""
    freq = {}
    for item in iterable:
        freq[item] = freq.get(item, 0) + 1
    return freq


# ========================================
# 5. 資料處理管道
# ========================================

class Pipeline:
    """函式式資料處理管道"""

    def __init__(self, data):
        self.data = list(data)

    def map(self, func: Callable) -> 'Pipeline':
        """映射"""
        return Pipeline(map(func, self.data))

    def filter(self, predicate: Callable) -> 'Pipeline':
        """過濾"""
        return Pipeline(filter(predicate, self.data))

    def reduce(self, func: Callable, initial=None):
        """歸約"""
        if initial is None:
            return reduce(func, self.data)
        return reduce(func, self.data, initial)

    def sort(self, key: Callable = None, reverse: bool = False) -> 'Pipeline':
        """排序"""
        return Pipeline(sorted(self.data, key=key, reverse=reverse))

    def take(self, n: int) -> 'Pipeline':
        """取前 n 個"""
        return Pipeline(self.data[:n])

    def skip(self, n: int) -> 'Pipeline':
        """跳過前 n 個"""
        return Pipeline(self.data[n:])

    def unique(self) -> 'Pipeline':
        """去重"""
        return Pipeline(unique(self.data))

    def group_by(self, key_func: Callable) -> dict:
        """分組"""
        return group_by(self.data, key_func)

    def partition(self, predicate: Callable) -> tuple:
        """分割"""
        return partition(self.data, predicate)

    def to_list(self) -> List:
        """轉換為列表"""
        return self.data

    def __repr__(self):
        return f"Pipeline({self.data})"


# ========================================
# 主程式
# ========================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║           函式式程式設計工具 v1.0                      ║
║           展示 Python 高階函式                        ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print("""
【選單】
  1. Lambda 表達式     2. Map/Filter/Reduce
  3. 函式組合          4. 資料處理管道
  5. 實用工具          0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n⚡ Lambda 表達式")
            print("=" * 50)

            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            print(f"原始數列: {numbers}")

            print(f"\n平方: {list(map(square, numbers))}")
            print(f"立方: {list(map(cube, numbers))}")
            print(f"兩倍: {list(map(double, numbers))}")
            print(f"偶數: {list(filter(is_even, numbers))}")
            print(f"奇數: {list(filter(complement(is_even), numbers))}")

            # Lambda 計算機
            print("\n【Lambda 計算機】")
            calc = lambda_calculator()
            a, b = 10, 3
            for op, func in calc.items():
                print(f"  {a} {op} {b} = {func(a, b)}")

            # 排序
            print("\n【Lambda 排序】")
            words = ["apple", "Banana", "cherry", "Date"]
            print(f"原始: {words}")
            print(f"按長度: {sorted(words, key=lambda s: len(s))}")
            print(f"忽略大小寫: {sorted(words, key=lambda s: s.lower())}")

        elif choice == '2':
            print("\n🔄 Map / Filter / Reduce")
            print("=" * 50)

            numbers = list(range(1, 11))
            print(f"數列: {numbers}")

            # Map
            print("\n【Map 映射】")
            print(f"平方: {list(map(lambda x: x**2, numbers))}")
            print(f"加100: {list(map(lambda x: x+100, numbers))}")

            # Filter
            print("\n【Filter 過濾】")
            print(f"偶數: {list(filter(lambda x: x%2==0, numbers))}")
            print(f">5: {list(filter(lambda x: x>5, numbers))}")

            # Reduce
            print("\n【Reduce 歸約】")
            print(f"總和: {reduce(add, numbers)}")
            print(f"乘積: {reduce(mul, numbers)}")
            print(f"最大: {reduce(max, numbers)}")

            # 進階組合
            print("\n【組合使用】")
            result = reduce(add, map(square, filter(is_even, numbers)))
            print(f"偶數的平方和: {result}")

            # 多重歸約
            print("\n【多重歸約】")
            results = multi_reduce(
                numbers,
                ('sum', add, 0),
                ('product', mul, 1),
                ('max', max, float('-inf')),
            )
            for name, value in results.items():
                print(f"  {name}: {value}")

        elif choice == '3':
            print("\n🔗 函式組合")
            print("=" * 50)

            # compose vs pipe
            print("【Compose（從右到左）】")
            add_one = lambda x: x + 1
            times_two = lambda x: x * 2

            composed = compose(add_one, times_two)  # (x*2) + 1
            print(f"compose(add_one, times_two)(5) = {composed(5)}")
            print(f"解釋: (5 * 2) + 1 = 11")

            print("\n【Pipe（從左到右）】")
            piped = pipe(times_two, add_one)  # (x*2) + 1
            print(f"pipe(times_two, add_one)(5) = {piped(5)}")
            print(f"解釋: (5 * 2) + 1 = 11")

            # 柯里化
            print("\n【柯里化 (Curry)】")
            @curry
            def add_three(a, b, c):
                return a + b + c

            print(f"add_three(1, 2, 3) = {add_three(1, 2, 3)}")
            print(f"add_three(1)(2)(3) = {add_three(1)(2)(3)}")
            print(f"add_three(1, 2)(3) = {add_three(1, 2)(3)}")

            add_10 = add_three(10)
            print(f"add_10(5, 3) = {add_10(5, 3)}")

            # Partial
            print("\n【Partial（部分應用）】")
            power_of_2 = partial(pow, 2)
            print(f"2^1, 2^2, 2^3, 2^4 = {[power_of_2(i) for i in range(1, 5)]}")

            # Flip
            print("\n【Flip（翻轉參數）】")
            def divide(a, b):
                return a / b
            flipped_divide = flip(divide)
            print(f"divide(10, 2) = {divide(10, 2)}")
            print(f"flip(divide)(10, 2) = {flipped_divide(10, 2)}")

        elif choice == '4':
            print("\n📊 資料處理管道")
            print("=" * 50)

            # 員工資料
            employees = [
                {'name': '王小明', 'dept': '工程', 'salary': 50000},
                {'name': '李大華', 'dept': '業務', 'salary': 45000},
                {'name': '張美麗', 'dept': '工程', 'salary': 55000},
                {'name': '陳建國', 'dept': '業務', 'salary': 60000},
                {'name': '林志偉', 'dept': '工程', 'salary': 48000},
                {'name': '黃雅婷', 'dept': '人資', 'salary': 42000},
            ]

            print("原始資料:")
            for e in employees:
                print(f"  {e}")

            # 使用 Pipeline
            print("\n【Pipeline 處理】")

            # 工程部門薪資
            eng_salaries = (
                Pipeline(employees)
                .filter(lambda e: e['dept'] == '工程')
                .map(lambda e: e['salary'])
                .to_list()
            )
            print(f"工程部門薪資: {eng_salaries}")
            print(f"工程部門平均: {sum(eng_salaries) / len(eng_salaries):.0f}")

            # 高薪員工
            high_salary = (
                Pipeline(employees)
                .filter(lambda e: e['salary'] >= 50000)
                .map(lambda e: e['name'])
                .to_list()
            )
            print(f"高薪員工: {high_salary}")

            # 按部門分組
            print("\n【按部門分組】")
            by_dept = Pipeline(employees).group_by(lambda e: e['dept'])
            for dept, members in by_dept.items():
                names = [m['name'] for m in members]
                print(f"  {dept}: {names}")

            # 分割高低薪
            print("\n【分割高低薪】")
            high, low = Pipeline(employees).partition(lambda e: e['salary'] >= 50000)
            print(f"高薪 (>=50000): {[e['name'] for e in high]}")
            print(f"低薪 (<50000): {[e['name'] for e in low]}")

        elif choice == '5':
            print("\n🛠️ 實用工具")
            print("=" * 50)

            numbers = list(range(1, 21))
            print(f"數列: {numbers}")

            print(f"\n前5個: {take(5, numbers)}")
            print(f"跳過5個: {drop(5, numbers)}")
            print(f"取<10: {take_while(lambda x: x < 10, numbers)}")
            print(f"丟<10: {drop_while(lambda x: x < 10, numbers)}")

            # 扁平化
            print("\n【扁平化】")
            nested = [1, [2, 3, [4, 5]], [6, [7, 8, [9]]]]
            print(f"巢狀: {nested}")
            print(f"扁平: {flatten(nested)}")

            # zip_with
            print("\n【zip_with】")
            a = [1, 2, 3]
            b = [10, 20, 30]
            print(f"a: {a}, b: {b}")
            print(f"相加: {zip_with(add, a, b)}")
            print(f"相乘: {zip_with(mul, a, b)}")

            # 去重
            print("\n【去重】")
            data = [1, 2, 2, 3, 1, 4, 2, 5]
            print(f"原始: {data}")
            print(f"去重: {unique(data)}")

            # 頻率
            print("\n【頻率統計】")
            text = "abracadabra"
            freq = frequencies(text)
            print(f"字串: {text}")
            print(f"頻率: {freq}")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
