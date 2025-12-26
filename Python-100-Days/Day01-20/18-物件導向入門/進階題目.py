"""
物件導向程式設計入門 - 進階練習題目
====================================

【前置知識】
- 第 14-17 課：函式
- 第 18 課：物件導向入門（類別、物件、屬性、方法）
"""

# ============================================================
# 練習 1：定義基本類別（基礎）
# ============================================================
"""
【題目說明】
定義一個 Person 類別：
- 屬性：name, age, email
- 方法：introduce() 返回自我介紹
- 方法：is_adult() 判斷是否成年

【預期輸出】
p = Person("Alice", 25, "alice@example.com")
p.introduce() → "我是 Alice，今年 25 歲"
p.is_adult() → True
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 2：定義銀行帳戶類別（基礎）
# ============================================================
"""
【題目說明】
定義一個 BankAccount 類別：
- 屬性：account_number, owner, balance
- 方法：deposit(amount) 存款
- 方法：withdraw(amount) 提款（餘額不足要拒絕）
- 方法：get_balance() 查詢餘額

【預期輸出】
account = BankAccount("123456", "Alice", 1000)
account.deposit(500) → "存款成功，餘額：1500"
account.withdraw(200) → "提款成功，餘額：1300"
account.withdraw(2000) → "餘額不足"
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 3：定義商品和購物車（進階）
# ============================================================
"""
【題目說明】
定義 Product 類別：
- 屬性：name, price, stock

定義 ShoppingCart 類別：
- 方法：add_item(product, quantity) 加入商品
- 方法：remove_item(product_name) 移除商品
- 方法：get_total() 計算總價
- 方法：checkout() 結帳

【預期輸出】
apple = Product("蘋果", 30, 100)
cart = ShoppingCart()
cart.add_item(apple, 3)
cart.get_total() → 90
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 4：定義學生成績系統（挑戰）
# ============================================================
"""
【題目說明】
定義 Student 類別：
- 屬性：name, student_id, scores（字典，科目:分數）
- 方法：add_score(subject, score) 新增成績
- 方法：get_average() 計算平均
- 方法：get_grade() 返回等第

定義 Classroom 類別：
- 方法：add_student(student) 新增學生
- 方法：get_top_students(n) 返回前 n 名學生
- 方法：get_class_average() 班級平均

【預期輸出】
alice = Student("Alice", "001")
alice.add_score("數學", 90)
alice.add_score("英文", 85)
alice.get_average() → 87.5
"""

# 請在下方撰寫你的程式碼


