"""
物件導向程式設計進階 - 進階練習題目
====================================

【前置知識】
- 第 18 課：物件導向入門
- 第 19 課：物件導向進階（繼承、多型、封裝）
"""

# ============================================================
# 練習 1：基本繼承（基礎）
# ============================================================
"""
【題目說明】
定義一個 Animal 基類和子類：
- Animal：name, age, speak()
- Dog(Animal)：breed, speak() 返回 "汪汪"
- Cat(Animal)：color, speak() 返回 "喵喵"

【預期輸出】
dog = Dog("小黑", 3, "柴犬")
dog.speak() → "汪汪"

cat = Cat("小花", 2, "橘色")
cat.speak() → "喵喵"
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 2：方法覆寫（基礎）
# ============================================================
"""
【題目說明】
定義 Shape 基類和子類，實作面積和周長計算：
- Shape：name, area(), perimeter()
- Rectangle(Shape)：width, height
- Circle(Shape)：radius
- Triangle(Shape)：a, b, c（三邊長）

【預期輸出】
rect = Rectangle(4, 5)
rect.area() → 20
rect.perimeter() → 18

circle = Circle(3)
circle.area() → 28.27
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 3：多層繼承和 super()（進階）
# ============================================================
"""
【題目說明】
定義員工系統的繼承結構：
- Employee：name, salary, work()
- Manager(Employee)：department, manage()
- Developer(Employee)：language, code()
- TechLead(Manager, Developer)：team_size

【預期輸出】
lead = TechLead("Alice", 80000, "Engineering", "Python", 5)
lead.work() → "Alice 正在工作"
lead.manage() → "Alice 正在管理 Engineering 部門"
lead.code() → "Alice 正在用 Python 寫程式"
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 4：抽象類別和多型（挑戰）
# ============================================================
"""
【題目說明】
使用抽象類別定義支付系統：
- PaymentMethod（抽象類別）：pay(amount), refund(amount)
- CreditCard：card_number, pay(), refund()
- PayPal：email, pay(), refund()
- BankTransfer：account, pay(), refund()

定義 PaymentProcessor 來處理不同的支付方式

【預期輸出】
credit_card = CreditCard("1234-5678-9012-3456")
paypal = PayPal("user@example.com")

processor = PaymentProcessor()
processor.process_payment(credit_card, 100)
→ "信用卡 *3456 支付 100 元成功"
"""

# 請在下方撰寫你的程式碼


