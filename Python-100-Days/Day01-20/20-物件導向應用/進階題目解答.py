"""
物件導向程式設計應用 - 進階練習解答
====================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
import random

# ============================================================
# 練習 1：設計模式 - 單例模式（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：單例模式 - Logger】")
print("=" * 40)


class Logger:
    """單例模式的日誌記錄器"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def _log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)

    def info(self, message):
        self._log("INFO", message)

    def warning(self, message):
        self._log("WARNING", message)

    def error(self, message):
        self._log("ERROR", message)


logger1 = Logger.get_instance()
logger2 = Logger.get_instance()
print(f"logger1 is logger2 → {logger1 is logger2}")

logger1.info("系統啟動")
logger1.warning("記憶體使用率高")
logger1.error("連線失敗")


# ============================================================
# 練習 2：設計模式 - 工廠模式（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：工廠模式 - 通知系統】")
print("=" * 40)


class Notification(ABC):
    """通知基類"""

    @abstractmethod
    def send(self, message):
        pass


class EmailNotification(Notification):
    def send(self, message):
        return f"發送 Email: {message}"


class SMSNotification(Notification):
    def send(self, message):
        return f"發送簡訊: {message}"


class PushNotification(Notification):
    def send(self, message):
        return f"發送推播: {message}"


class NotificationFactory:
    """通知工廠"""

    @staticmethod
    def create(notification_type):
        types = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification
        }
        if notification_type.lower() in types:
            return types[notification_type.lower()]()
        raise ValueError(f"未知的通知類型: {notification_type}")


factory = NotificationFactory()
email = factory.create("email")
sms = factory.create("sms")
push = factory.create("push")

print(email.send("Hello from Email"))
print(sms.send("Hello from SMS"))
print(push.send("Hello from Push"))


# ============================================================
# 練習 3：完整的銀行系統（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：銀行系統】")
print("=" * 40)


class Account(ABC):
    """帳戶基類"""
    _next_id = 1000

    def __init__(self, owner, balance=0):
        self.account_id = Account._next_id
        Account._next_id += 1
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._record_transaction("存款", amount)
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self._can_withdraw(amount):
            self.balance -= amount
            self._record_transaction("提款", -amount)
            return True
        return False

    @abstractmethod
    def _can_withdraw(self, amount):
        pass

    def _record_transaction(self, type_, amount):
        self.transactions.append({
            "time": datetime.now(),
            "type": type_,
            "amount": amount,
            "balance": self.balance
        })

    def get_balance(self):
        return self.balance


class SavingsAccount(Account):
    """儲蓄帳戶"""

    def __init__(self, owner, balance=0, interest_rate=0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def _can_withdraw(self, amount):
        return self.balance >= amount

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._record_transaction("利息", interest)
        return interest


class CheckingAccount(Account):
    """支票帳戶"""

    def __init__(self, owner, balance=0, overdraft_limit=1000):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def _can_withdraw(self, amount):
        return self.balance + self.overdraft_limit >= amount


class Bank:
    """銀行"""

    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def open_account(self, account_type, owner, initial_deposit=0):
        if account_type == "savings":
            account = SavingsAccount(owner, initial_deposit)
        elif account_type == "checking":
            account = CheckingAccount(owner, initial_deposit)
        else:
            raise ValueError(f"未知的帳戶類型: {account_type}")

        self.accounts[account.account_id] = account
        print(f"開戶成功！帳號：{account.account_id}，持有人：{owner}")
        return account

    def transfer(self, from_account, to_account, amount):
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            print(f"轉帳成功：{from_account.owner} → {to_account.owner}，金額：{amount}")
            return True
        print("轉帳失敗：餘額不足")
        return False


# 測試
bank = Bank("台灣銀行")
savings = bank.open_account("savings", "Alice", 10000)
checking = bank.open_account("checking", "Bob", 5000)

print(f"\nAlice 餘額：{savings.get_balance()}")
savings.deposit(5000)
print(f"存款後餘額：{savings.get_balance()}")

interest = savings.calculate_interest()
print(f"利息：{interest:.2f}，餘額：{savings.get_balance():.2f}")

bank.transfer(savings, checking, 3000)
print(f"Alice 餘額：{savings.get_balance():.2f}")
print(f"Bob 餘額：{checking.get_balance():.2f}")


# ============================================================
# 練習 4：設計遊戲系統（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：RPG 遊戲系統】")
print("=" * 40)


class Item:
    """物品基類"""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description


class Weapon(Item):
    """武器"""

    def __init__(self, name, attack=0):
        super().__init__(name)
        self.attack = attack


class Armor(Item):
    """護甲"""

    def __init__(self, name, defense=0):
        super().__init__(name)
        self.defense = defense


class Character:
    """角色基類"""

    def __init__(self, name, hp=100, attack=10, defense=5):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.level = 1
        self.exp = 0
        self.weapon = None
        self.armor = None

    @property
    def attack(self):
        bonus = self.weapon.attack if self.weapon else 0
        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = self.armor.defense if self.armor else 0
        return self.base_defense + bonus

    def equip(self, item):
        if isinstance(item, Weapon):
            self.weapon = item
            print(f"{self.name} 裝備了 {item.name}")
        elif isinstance(item, Armor):
            self.armor = item
            print(f"{self.name} 穿上了 {item.name}")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        print(f"{self.name} 受到 {actual_damage} 點傷害，剩餘 HP: {max(0, self.hp)}")
        return self.hp <= 0

    def attack_target(self, target):
        damage = self.attack + random.randint(-2, 2)
        print(f"{self.name} 攻擊 {target.name}，造成 {damage} 點傷害")
        return target.take_damage(damage)

    def is_alive(self):
        return self.hp > 0


class Warrior(Character):
    """戰士"""

    def __init__(self, name):
        super().__init__(name, hp=150, attack=15, defense=10)
        self.job = "戰士"

    def skill_heavy_strike(self, target):
        damage = self.attack * 2
        print(f"{self.name} 使用【重擊】！")
        return target.take_damage(damage)


class Mage(Character):
    """法師"""

    def __init__(self, name):
        super().__init__(name, hp=80, attack=20, defense=3)
        self.job = "法師"
        self.mp = 50

    def skill_fireball(self, target):
        if self.mp >= 10:
            self.mp -= 10
            damage = self.attack * 1.5
            print(f"{self.name} 使用【火球術】！（MP: {self.mp}）")
            return target.take_damage(int(damage))
        print(f"{self.name} MP 不足！")
        return False


class Battle:
    """戰鬥系統"""

    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2

    def start(self):
        print(f"\n⚔️ 戰鬥開始：{self.char1.name} vs {self.char2.name}")
        print("=" * 40)

        turn = 1
        while self.char1.is_alive() and self.char2.is_alive():
            print(f"\n--- 第 {turn} 回合 ---")

            # char1 攻擊
            if random.random() < 0.3 and hasattr(self.char1, 'skill_heavy_strike'):
                self.char1.skill_heavy_strike(self.char2)
            else:
                self.char1.attack_target(self.char2)

            if not self.char2.is_alive():
                break

            # char2 攻擊
            if random.random() < 0.3 and hasattr(self.char2, 'skill_fireball'):
                self.char2.skill_fireball(self.char1)
            else:
                self.char2.attack_target(self.char1)

            turn += 1

        print("\n" + "=" * 40)
        winner = self.char1 if self.char1.is_alive() else self.char2
        print(f"🏆 {winner.name} 獲勝！")


# 測試
warrior = Warrior("勇者")
mage = Mage("法師")

sword = Weapon("長劍", attack=10)
staff = Weapon("法杖", attack=5)

warrior.equip(sword)
mage.equip(staff)

battle = Battle(warrior, mage)
battle.start()


# ============================================================
# 【設計模式整理】
# ============================================================
"""
【單例模式 Singleton】
- 確保類別只有一個實例
- 用於：設定管理、日誌記錄、資料庫連線

【工廠模式 Factory】
- 將物件創建邏輯封裝起來
- 用於：根據條件創建不同類型的物件

【策略模式 Strategy】
- 定義一系列演算法，讓它們可以互換
- 用於：支付方式、排序演算法

【觀察者模式 Observer】
- 定義物件間的一對多依賴
- 用於：事件系統、訂閱通知

【裝飾者模式 Decorator】
- 動態地給物件添加功能
- 用於：在不修改原始類別的情況下擴展功能
"""
