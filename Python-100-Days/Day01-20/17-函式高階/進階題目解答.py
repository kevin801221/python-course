"""
函式高階應用 - 進階練習解答
============================
"""

from functools import reduce

# ============================================================
# 練習 1：Lambda 表達式（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：Lambda 表達式】")
print("=" * 40)

# 計算平方
square = lambda x: x ** 2
print(f"square(5) → {square(5)}")

# 判斷偶數
is_even = lambda x: x % 2 == 0
print(f"is_even(4) → {is_even(4)}")
print(f"is_even(5) → {is_even(5)}")

# 兩數相加
add = lambda a, b: a + b
print(f"add(3, 5) → {add(3, 5)}")

# 取字串長度
length = lambda s: len(s)
print(f"length('Hello') → {length('Hello')}")


# ============================================================
# 練習 2：map 和 filter（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：map 和 filter】")
print("=" * 40)

numbers = [1, 5, 8, 12, 15, 3]
print(f"numbers = {numbers}")

# 乘以 2
doubled = list(map(lambda x: x * 2, numbers))
print(f"map(x * 2) → {doubled}")

# 篩選大於 10
greater_than_10 = list(filter(lambda x: x > 10, numbers))
print(f"filter(x > 10) → {greater_than_10}")

# 字串轉大寫
words = ["hello", "world", "python"]
upper_words = list(map(str.upper, words))
print(f"\nwords = {words}")
print(f"map(upper) → {upper_words}")

# 篩選長度大於 3
long_words = list(filter(lambda s: len(s) > 3, words))
print(f"filter(len > 3) → {long_words}")


# ============================================================
# 練習 3：reduce 應用（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：reduce 應用】")
print("=" * 40)

numbers = [1, 2, 3, 4, 5]
print(f"numbers = {numbers}")

# 計算乘積
product = reduce(lambda x, y: x * y, numbers)
print(f"reduce(乘積) → {product}")

# 找最大值
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(f"reduce(最大值) → {maximum}")

# 連接字串
words = ["Hello", "World", "Python"]
concatenated = reduce(lambda x, y: x + " " + y, words)
print(f"\nreduce(連接) → {concatenated}")

# 計算階乘
n = 5
factorial = reduce(lambda x, y: x * y, range(1, n + 1))
print(f"reduce(階乘 5!) → {factorial}")


# ============================================================
# 練習 4：組合使用（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 4：組合使用】")
print("=" * 40)

# 學生成績
students = [('Alice', 85), ('Bob', 58), ('Carol', 92), ('David', 45)]
print(f"students = {students}")

# 篩選及格者，計算平均
passed = list(filter(lambda s: s[1] >= 60, students))
if passed:
    avg = reduce(lambda acc, s: acc + s[1], passed, 0) / len(passed)
    print(f"及格者：{[s[0] for s in passed]}")
    print(f"及格者平均：{avg:.1f}")

# 商品列表
products = [
    ('蘋果', 30, '水果'),
    ('牛奶', 50, '飲料'),
    ('香蕉', 20, '水果'),
    ('橘子', 25, '水果')
]
print(f"\nproducts = {products}")

# 篩選水果，計算總價
fruits = list(filter(lambda p: p[2] == '水果', products))
fruit_total = reduce(lambda acc, p: acc + p[1], fruits, 0)
print(f"水果商品：{[p[0] for p in fruits]}")
print(f"水果總價：{fruit_total}")

# 文字處理
texts = ["Hi", "Hello", "World", "Python", "AI"]
print(f"\ntexts = {texts}")

# 篩選長度 > 3，轉大寫，用逗號連接
result = reduce(
    lambda acc, s: acc + ", " + s if acc else s,
    map(str.upper, filter(lambda s: len(s) > 3, texts)),
    ""
)
print(f"處理結果：{result}")


# ============================================================
# 練習 5：函式式程式設計（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 5：函式式程式設計】")
print("=" * 40)


def compose(f, g):
    """組合兩個函式：f(g(x))"""
    return lambda x: f(g(x))


def pipe(*funcs):
    """管道：依序執行多個函式"""
    def piped(x):
        result = x
        for func in funcs:
            result = func(result)
        return result
    return piped


def curry(func):
    """柯里化：將多參數函式轉為單參數函式鏈"""
    import inspect
    sig = inspect.signature(func)
    num_params = len(sig.parameters)

    def curried(*args):
        if len(args) >= num_params:
            return func(*args[:num_params])
        return lambda *more: curried(*(args + more))

    return curried


# 測試 compose
add_one = lambda x: x + 1
double = lambda x: x * 2

composed = compose(add_one, double)
print(f"compose(add_one, double)(5) → {composed(5)}")  # add_one(double(5)) = 11

# 測試 pipe
piped = pipe(double, add_one, double)
print(f"pipe(double, add_one, double)(5) → {piped(5)}")  # double(add_one(double(5))) = 22

# 測試 curry
@curry
def add_three(a, b, c):
    return a + b + c


print(f"curry: add_three(1)(2)(3) → {add_three(1)(2)(3)}")
print(f"curry: add_three(1, 2)(3) → {add_three(1, 2)(3)}")


# ============================================================
# 【函式式程式設計整理】
# ============================================================
"""
【Lambda 表達式】
lambda 參數: 表達式
等同於：
def f(參數):
    return 表達式

【map 函式】
map(func, iterable)
- 對可迭代物件中的每個元素應用函式
- 返回迭代器

【filter 函式】
filter(func, iterable)
- 篩選符合條件的元素
- func 返回 True 的元素會被保留

【reduce 函式】
from functools import reduce
reduce(func, iterable, initial)
- 累積計算
- func(累積值, 當前元素)

【函式式程式設計原則】
1. 純函式：相同輸入永遠得到相同輸出
2. 不可變性：不修改原始資料
3. 函式作為一等公民：函式可以作為參數和返回值
"""
