"""
物件導向程式設計應用 - 進階練習題目
====================================

【前置知識】
- 第 18-19 課：物件導向基礎和進階
- 第 20 課：物件導向應用
"""

# ============================================================
# 練習 1：設計模式 - 單例模式（基礎）
# ============================================================
"""
【題目說明】
實作單例模式的 Logger 類別：
- 確保只有一個實例
- 可以記錄不同級別的日誌：info, warning, error

【預期輸出】
logger1 = Logger.get_instance()
logger2 = Logger.get_instance()
logger1 is logger2 → True

logger1.info("系統啟動")
logger1.warning("記憶體使用率高")
logger1.error("連線失敗")
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 2：設計模式 - 工廠模式（基礎）
# ============================================================
"""
【題目說明】
使用工廠模式建立不同類型的通知：
- Notification（基類）
- EmailNotification
- SMSNotification
- PushNotification
- NotificationFactory

【預期輸出】
factory = NotificationFactory()
email = factory.create("email")
email.send("Hello") → "發送 Email: Hello"

sms = factory.create("sms")
sms.send("Hello") → "發送簡訊: Hello"
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 3：完整的銀行系統（進階）
# ============================================================
"""
【題目說明】
設計一個完整的銀行系統：
- Account（帳戶基類）
- SavingsAccount（儲蓄帳戶）- 有利息
- CheckingAccount（支票帳戶）- 有透支額度
- Bank（銀行）- 管理所有帳戶

功能：
- 開戶、銷戶
- 存款、提款、轉帳
- 計算利息
- 查詢帳戶

【預期輸出】
bank = Bank("台灣銀行")
savings = bank.open_account("savings", "Alice", 10000)
checking = bank.open_account("checking", "Bob", 5000)

savings.deposit(5000)
savings.calculate_interest()  # 計算利息
bank.transfer(savings, checking, 3000)  # 轉帳
"""

# 請在下方撰寫你的程式碼




# ============================================================
# 練習 4：設計遊戲系統（挑戰）
# ============================================================
"""
【題目說明】
設計一個 RPG 遊戲系統：
- Character（角色基類）
- Warrior, Mage, Archer（職業）
- Item, Weapon, Armor（物品）
- Inventory（背包）
- Battle（戰鬥系統）

功能：
- 角色創建和升級
- 裝備系統
- 戰鬥系統
- 技能系統

【預期輸出】
warrior = Warrior("勇者")
mage = Mage("法師")

sword = Weapon("長劍", attack=10)
warrior.equip(sword)

battle = Battle(warrior, mage)
battle.start()
"""

# 請在下方撰寫你的程式碼


