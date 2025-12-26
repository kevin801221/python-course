"""
物件導向程式設計入門 - 進階練習解答
====================================
"""

# ============================================================
# 練習 1：定義基本類別（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：定義基本類別】")
print("=" * 40)


class Person:
    """人物類別"""

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def introduce(self):
        """自我介紹"""
        return f"我是 {self.name}，今年 {self.age} 歲"

    def is_adult(self):
        """判斷是否成年"""
        return self.age >= 18


p = Person("Alice", 25, "alice@example.com")
print(f"p.name → {p.name}")
print(f"p.introduce() → {p.introduce()}")
print(f"p.is_adult() → {p.is_adult()}")


# ============================================================
# 練習 2：定義銀行帳戶類別（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：銀行帳戶類別】")
print("=" * 40)


class BankAccount:
    """銀行帳戶類別"""

    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.balance += amount
            return f"存款成功，餘額：{self.balance}"
        return "存款金額必須大於 0"

    def withdraw(self, amount):
        """提款"""
        if amount > self.balance:
            return "餘額不足"
        if amount <= 0:
            return "提款金額必須大於 0"
        self.balance -= amount
        return f"提款成功，餘額：{self.balance}"

    def get_balance(self):
        """查詢餘額"""
        return self.balance


account = BankAccount("123456", "Alice", 1000)
print(f"初始餘額：{account.get_balance()}")
print(account.deposit(500))
print(account.withdraw(200))
print(account.withdraw(2000))


# ============================================================
# 練習 3：定義商品和購物車（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：商品和購物車】")
print("=" * 40)


class Product:
    """商品類別"""

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} - ${self.price} (庫存: {self.stock})"


class ShoppingCart:
    """購物車類別"""

    def __init__(self):
        self.items = {}  # {product_name: (product, quantity)}

    def add_item(self, product, quantity=1):
        """加入商品"""
        if quantity > product.stock:
            return f"庫存不足，只剩 {product.stock} 個"

        if product.name in self.items:
            self.items[product.name][1] += quantity
        else:
            self.items[product.name] = [product, quantity]

        return f"已加入 {product.name} x {quantity}"

    def remove_item(self, product_name):
        """移除商品"""
        if product_name in self.items:
            del self.items[product_name]
            return f"已移除 {product_name}"
        return "商品不在購物車中"

    def get_total(self):
        """計算總價"""
        total = 0
        for product, quantity in self.items.values():
            total += product.price * quantity
        return total

    def show_cart(self):
        """顯示購物車"""
        if not self.items:
            return "購物車是空的"

        lines = ["【購物車】"]
        for product, quantity in self.items.values():
            subtotal = product.price * quantity
            lines.append(f"  {product.name} x {quantity} = ${subtotal}")
        lines.append(f"  總計：${self.get_total()}")
        return "\n".join(lines)


# 測試
apple = Product("蘋果", 30, 100)
banana = Product("香蕉", 20, 50)

cart = ShoppingCart()
print(cart.add_item(apple, 3))
print(cart.add_item(banana, 2))
print(cart.show_cart())
print(f"總價：{cart.get_total()}")


# ============================================================
# 練習 4：定義學生成績系統（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：學生成績系統】")
print("=" * 40)


class Student:
    """學生類別"""

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.scores = {}

    def add_score(self, subject, score):
        """新增成績"""
        self.scores[subject] = score
        return f"已記錄 {subject}：{score}"

    def get_average(self):
        """計算平均"""
        if not self.scores:
            return 0
        return sum(self.scores.values()) / len(self.scores)

    def get_grade(self):
        """返回等第"""
        avg = self.get_average()
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.name}({self.student_id}) - 平均：{self.get_average():.1f}"


class Classroom:
    """班級類別"""

    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        """新增學生"""
        self.students.append(student)
        return f"已加入 {student.name}"

    def get_top_students(self, n=3):
        """返回前 n 名學生"""
        sorted_students = sorted(
            self.students,
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]

    def get_class_average(self):
        """班級平均"""
        if not self.students:
            return 0
        total = sum(s.get_average() for s in self.students)
        return total / len(self.students)


# 測試
alice = Student("Alice", "001")
alice.add_score("數學", 90)
alice.add_score("英文", 85)
alice.add_score("國文", 88)

bob = Student("Bob", "002")
bob.add_score("數學", 75)
bob.add_score("英文", 80)
bob.add_score("國文", 78)

carol = Student("Carol", "003")
carol.add_score("數學", 95)
carol.add_score("英文", 92)
carol.add_score("國文", 90)

classroom = Classroom("三年甲班")
classroom.add_student(alice)
classroom.add_student(bob)
classroom.add_student(carol)

print(f"Alice 平均：{alice.get_average():.1f}")
print(f"Alice 等第：{alice.get_grade()}")

print(f"\n班級平均：{classroom.get_class_average():.1f}")
print("\n前 2 名學生：")
for i, student in enumerate(classroom.get_top_students(2), 1):
    print(f"  {i}. {student}")


# ============================================================
# 【物件導向基礎整理】
# ============================================================
"""
【類別定義】
class ClassName:
    def __init__(self, args):  # 建構子
        self.attribute = value  # 實例屬性

    def method(self):  # 實例方法
        pass

【特殊方法】
__init__    建構子（初始化）
__str__     字串表示（print 時呼叫）
__repr__    程式表示（debug 用）
__eq__      相等比較
__lt__      小於比較

【存取控制】
self.public      公開屬性
self._protected  受保護（慣例）
self.__private   私有（名稱修飾）

【類別 vs 實例】
- 類別屬性：所有實例共享
- 實例屬性：每個實例獨立
"""
