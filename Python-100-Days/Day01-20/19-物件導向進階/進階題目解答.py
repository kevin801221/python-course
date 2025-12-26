"""
物件導向程式設計進階 - 進階練習解答
====================================
"""

from abc import ABC, abstractmethod
import math

# ============================================================
# 練習 1：基本繼承（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：基本繼承】")
print("=" * 40)


class Animal:
    """動物基類"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return "..."

    def info(self):
        return f"{self.name}，{self.age} 歲"


class Dog(Animal):
    """狗類別"""

    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self):
        return "汪汪"

    def fetch(self):
        return f"{self.name} 去撿球了"


class Cat(Animal):
    """貓類別"""

    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speak(self):
        return "喵喵"

    def scratch(self):
        return f"{self.name} 在抓東西"


dog = Dog("小黑", 3, "柴犬")
cat = Cat("小花", 2, "橘色")

print(f"dog.info() → {dog.info()}")
print(f"dog.speak() → {dog.speak()}")
print(f"dog.fetch() → {dog.fetch()}")

print(f"\ncat.info() → {cat.info()}")
print(f"cat.speak() → {cat.speak()}")


# ============================================================
# 練習 2：方法覆寫（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：方法覆寫】")
print("=" * 40)


class Shape:
    """形狀基類"""

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.name}：面積={self.area():.2f}，周長={self.perimeter():.2f}"


class Rectangle(Shape):
    """矩形"""

    def __init__(self, width, height):
        super().__init__("矩形")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """圓形"""

    def __init__(self, radius):
        super().__init__("圓形")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Triangle(Shape):
    """三角形"""

    def __init__(self, a, b, c):
        super().__init__("三角形")
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        # 使用海龍公式
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


rect = Rectangle(4, 5)
circle = Circle(3)
triangle = Triangle(3, 4, 5)

print(rect)
print(circle)
print(triangle)


# ============================================================
# 練習 3：多層繼承和 super()（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：多層繼承】")
print("=" * 40)


class Employee:
    """員工基類"""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def work(self):
        return f"{self.name} 正在工作"

    def get_info(self):
        return f"{self.name}，薪資：{self.salary}"


class Manager(Employee):
    """經理"""

    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department

    def manage(self):
        return f"{self.name} 正在管理 {self.department} 部門"


class Developer(Employee):
    """開發者"""

    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def code(self):
        return f"{self.name} 正在用 {self.language} 寫程式"


class TechLead(Manager, Developer):
    """技術主管"""

    def __init__(self, name, salary, department, language, team_size):
        Manager.__init__(self, name, salary, department)
        Developer.__init__(self, name, salary, language)
        self.team_size = team_size

    def lead(self):
        return f"{self.name} 帶領 {self.team_size} 人的團隊"


lead = TechLead("Alice", 80000, "Engineering", "Python", 5)
print(f"lead.work() → {lead.work()}")
print(f"lead.manage() → {lead.manage()}")
print(f"lead.code() → {lead.code()}")
print(f"lead.lead() → {lead.lead()}")


# ============================================================
# 練習 4：抽象類別和多型（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：抽象類別和多型】")
print("=" * 40)


class PaymentMethod(ABC):
    """支付方式抽象類別"""

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

    @abstractmethod
    def get_description(self):
        pass


class CreditCard(PaymentMethod):
    """信用卡支付"""

    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        return f"信用卡 *{self.card_number[-4:]} 支付 {amount} 元成功"

    def refund(self, amount):
        return f"信用卡 *{self.card_number[-4:]} 退款 {amount} 元成功"

    def get_description(self):
        return f"信用卡 *{self.card_number[-4:]}"


class PayPal(PaymentMethod):
    """PayPal 支付"""

    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        return f"PayPal ({self.email}) 支付 {amount} 元成功"

    def refund(self, amount):
        return f"PayPal ({self.email}) 退款 {amount} 元成功"

    def get_description(self):
        return f"PayPal ({self.email})"


class BankTransfer(PaymentMethod):
    """銀行轉帳"""

    def __init__(self, account):
        self.account = account

    def pay(self, amount):
        return f"銀行帳戶 {self.account} 轉帳 {amount} 元成功"

    def refund(self, amount):
        return f"銀行帳戶 {self.account} 退款 {amount} 元成功"

    def get_description(self):
        return f"銀行帳戶 {self.account}"


class PaymentProcessor:
    """支付處理器"""

    def process_payment(self, payment_method: PaymentMethod, amount: float):
        """處理支付（多型示範）"""
        print(f"處理 {payment_method.get_description()} 的支付...")
        return payment_method.pay(amount)

    def process_refund(self, payment_method: PaymentMethod, amount: float):
        """處理退款"""
        return payment_method.refund(amount)


# 測試多型
credit_card = CreditCard("1234-5678-9012-3456")
paypal = PayPal("user@example.com")
bank = BankTransfer("123-456-789")

processor = PaymentProcessor()

print(processor.process_payment(credit_card, 100))
print(processor.process_payment(paypal, 200))
print(processor.process_payment(bank, 300))


# ============================================================
# 【物件導向進階整理】
# ============================================================
"""
【繼承】
class Child(Parent):
    def __init__(self, args):
        super().__init__(parent_args)
        self.child_attr = value

【多型】
- 不同類別實現相同的方法
- 可以用相同的方式呼叫不同類別的方法

【抽象類別】
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass

【方法解析順序 (MRO)】
- 多重繼承時的方法查找順序
- 使用 ClassName.__mro__ 查看

【組合 vs 繼承】
- 繼承：is-a 關係（狗是動物）
- 組合：has-a 關係（汽車有引擎）
"""
