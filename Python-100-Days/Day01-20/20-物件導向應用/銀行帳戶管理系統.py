"""
銀行帳戶管理系統 - Bank Account Management System
==================================================
進階應用：展示 Python 物件導向完整應用

功能：
1. 封裝 (Encapsulation)
2. 繼承 (Inheritance)
3. 多型 (Polymorphism)
4. 組合 (Composition)
5. 設計模式應用
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from decimal import Decimal, ROUND_HALF_UP
import json
import hashlib


# ========================================
# 1. 基礎類別與封裝
# ========================================

class Money:
    """金額類別 - 封裝金額處理邏輯"""

    def __init__(self, amount: float, currency: str = "TWD"):
        self._amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self._currency = currency

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    def __str__(self) -> str:
        return f"{self._currency} ${self._amount:,.2f}"

    def __repr__(self) -> str:
        return f"Money({self._amount}, '{self._currency}')"

    def __add__(self, other: 'Money') -> 'Money':
        if self._currency != other._currency:
            raise ValueError("貨幣類型不同")
        return Money(float(self._amount + other._amount), self._currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self._currency != other._currency:
            raise ValueError("貨幣類型不同")
        return Money(float(self._amount - other._amount), self._currency)

    def __ge__(self, other: 'Money') -> bool:
        return self._amount >= other._amount

    def __le__(self, other: 'Money') -> bool:
        return self._amount <= other._amount


class Transaction:
    """交易記錄類別"""

    _counter = 0

    def __init__(self, trans_type: str, amount: Money, description: str = ""):
        Transaction._counter += 1
        self._id = f"TXN{Transaction._counter:06d}"
        self._type = trans_type
        self._amount = amount
        self._description = description
        self._timestamp = datetime.now()
        self._status = "completed"

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def amount(self) -> Money:
        return self._amount

    def __str__(self) -> str:
        time_str = self._timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{self._id}] {time_str} | {self._type:8} | {self._amount} | {self._description}"


# ========================================
# 2. 帳戶抽象類別與繼承
# ========================================

class Account(ABC):
    """帳戶抽象基礎類別"""

    _account_counter = 1000

    def __init__(self, holder_name: str, initial_balance: float = 0):
        Account._account_counter += 1
        self._account_number = f"ACC{Account._account_counter:06d}"
        self._holder_name = holder_name
        self._balance = Money(initial_balance)
        self._transactions: List[Transaction] = []
        self._created_at = datetime.now()
        self._is_active = True
        self._pin_hash = None

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def holder_name(self) -> str:
        return self._holder_name

    @property
    def balance(self) -> Money:
        return self._balance

    @property
    def is_active(self) -> bool:
        return self._is_active

    def set_pin(self, pin: str):
        """設定 PIN 碼"""
        self._pin_hash = hashlib.sha256(pin.encode()).hexdigest()

    def verify_pin(self, pin: str) -> bool:
        """驗證 PIN 碼"""
        if self._pin_hash is None:
            return True
        return hashlib.sha256(pin.encode()).hexdigest() == self._pin_hash

    def deposit(self, amount: float, description: str = "存款") -> dict:
        """存款"""
        if not self._is_active:
            return {'success': False, 'message': '帳戶已停用'}

        if amount <= 0:
            return {'success': False, 'message': '金額必須大於 0'}

        money = Money(amount)
        self._balance = self._balance + money

        transaction = Transaction("存款", money, description)
        self._transactions.append(transaction)

        return {
            'success': True,
            'message': f'成功存入 {money}',
            'transaction': transaction,
            'balance': self._balance
        }

    def withdraw(self, amount: float, description: str = "提款") -> dict:
        """提款"""
        if not self._is_active:
            return {'success': False, 'message': '帳戶已停用'}

        if amount <= 0:
            return {'success': False, 'message': '金額必須大於 0'}

        money = Money(amount)

        if not self._can_withdraw(money):
            return {'success': False, 'message': '餘額不足'}

        self._balance = self._balance - money

        transaction = Transaction("提款", money, description)
        self._transactions.append(transaction)

        return {
            'success': True,
            'message': f'成功提取 {money}',
            'transaction': transaction,
            'balance': self._balance
        }

    @abstractmethod
    def _can_withdraw(self, amount: Money) -> bool:
        """檢查是否可提款（子類實作）"""
        pass

    @abstractmethod
    def get_account_type(self) -> str:
        """取得帳戶類型（子類實作）"""
        pass

    @abstractmethod
    def calculate_interest(self) -> Money:
        """計算利息（子類實作）"""
        pass

    def get_transactions(self, n: int = 10) -> List[Transaction]:
        """取得最近 n 筆交易"""
        return self._transactions[-n:]

    def get_statement(self) -> str:
        """取得對帳單"""
        lines = [
            f"{'='*60}",
            f"  {self.get_account_type()} 對帳單",
            f"  帳號: {self._account_number}",
            f"  戶名: {self._holder_name}",
            f"  餘額: {self._balance}",
            f"{'='*60}",
            "  最近交易:",
        ]

        for t in self._transactions[-10:]:
            lines.append(f"  {t}")

        lines.append(f"{'='*60}")
        return '\n'.join(lines)

    def deactivate(self):
        """停用帳戶"""
        self._is_active = False

    def activate(self):
        """啟用帳戶"""
        self._is_active = True


class SavingsAccount(Account):
    """儲蓄帳戶"""

    INTEREST_RATE = 0.02  # 2% 年利率

    def __init__(self, holder_name: str, initial_balance: float = 0):
        super().__init__(holder_name, initial_balance)

    def get_account_type(self) -> str:
        return "💰 儲蓄帳戶"

    def _can_withdraw(self, amount: Money) -> bool:
        return self._balance >= amount

    def calculate_interest(self) -> Money:
        """計算年利息"""
        interest = float(self._balance.amount) * self.INTEREST_RATE
        return Money(interest)

    def apply_interest(self) -> dict:
        """套用利息"""
        interest = self.calculate_interest()
        self._balance = self._balance + interest

        transaction = Transaction("利息", interest, f"年利率 {self.INTEREST_RATE*100}%")
        self._transactions.append(transaction)

        return {
            'success': True,
            'interest': interest,
            'balance': self._balance
        }


class CheckingAccount(Account):
    """支票帳戶（含透支額度）"""

    def __init__(self, holder_name: str, initial_balance: float = 0, overdraft_limit: float = 10000):
        super().__init__(holder_name, initial_balance)
        self._overdraft_limit = Money(overdraft_limit)

    def get_account_type(self) -> str:
        return "📝 支票帳戶"

    def _can_withdraw(self, amount: Money) -> bool:
        # 可透支到限額
        available = Money(float(self._balance.amount) + float(self._overdraft_limit.amount))
        return available >= amount

    def calculate_interest(self) -> Money:
        """支票帳戶不計息"""
        return Money(0)

    @property
    def overdraft_limit(self) -> Money:
        return self._overdraft_limit


class FixedDepositAccount(Account):
    """定期存款帳戶"""

    INTEREST_RATE = 0.05  # 5% 年利率

    def __init__(self, holder_name: str, initial_balance: float, term_months: int = 12):
        super().__init__(holder_name, initial_balance)
        self._term_months = term_months
        self._maturity_date = datetime.now()  # 簡化：實際應計算到期日

    def get_account_type(self) -> str:
        return "🔒 定期存款"

    def _can_withdraw(self, amount: Money) -> bool:
        # 定存不能提前解約（簡化處理）
        return False

    def calculate_interest(self) -> Money:
        """計算到期利息"""
        months_rate = self.INTEREST_RATE * (self._term_months / 12)
        interest = float(self._balance.amount) * months_rate
        return Money(interest)

    def withdraw(self, amount: float, description: str = "提款") -> dict:
        return {'success': False, 'message': '定期存款不能提前解約'}


# ========================================
# 3. 客戶類別（組合）
# ========================================

class Customer:
    """客戶類別 - 使用組合管理帳戶"""

    _customer_counter = 0

    def __init__(self, name: str, phone: str = "", email: str = ""):
        Customer._customer_counter += 1
        self._id = f"CUS{Customer._customer_counter:06d}"
        self._name = name
        self._phone = phone
        self._email = email
        self._accounts: List[Account] = []
        self._registered_at = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def add_account(self, account: Account):
        """新增帳戶"""
        self._accounts.append(account)

    def get_accounts(self) -> List[Account]:
        """取得所有帳戶"""
        return self._accounts

    def get_total_balance(self) -> Money:
        """取得總資產"""
        total = Money(0)
        for account in self._accounts:
            total = total + account.balance
        return total

    def __str__(self) -> str:
        return f"客戶 {self._name} ({self._id}) - {len(self._accounts)} 個帳戶"


# ========================================
# 4. 銀行類別（門面模式）
# ========================================

class Bank:
    """銀行類別 - 管理所有客戶和帳戶"""

    def __init__(self, name: str):
        self._name = name
        self._customers: List[Customer] = []
        self._all_accounts: dict = {}  # account_number -> account

    @property
    def name(self) -> str:
        return self._name

    def register_customer(self, name: str, phone: str = "", email: str = "") -> Customer:
        """註冊新客戶"""
        customer = Customer(name, phone, email)
        self._customers.append(customer)
        return customer

    def open_savings_account(self, customer: Customer, initial_balance: float = 0) -> SavingsAccount:
        """開立儲蓄帳戶"""
        account = SavingsAccount(customer.name, initial_balance)
        customer.add_account(account)
        self._all_accounts[account.account_number] = account
        return account

    def open_checking_account(self, customer: Customer, initial_balance: float = 0,
                              overdraft_limit: float = 10000) -> CheckingAccount:
        """開立支票帳戶"""
        account = CheckingAccount(customer.name, initial_balance, overdraft_limit)
        customer.add_account(account)
        self._all_accounts[account.account_number] = account
        return account

    def open_fixed_deposit(self, customer: Customer, amount: float,
                          term_months: int = 12) -> FixedDepositAccount:
        """開立定期存款"""
        account = FixedDepositAccount(customer.name, amount, term_months)
        customer.add_account(account)
        self._all_accounts[account.account_number] = account
        return account

    def find_account(self, account_number: str) -> Optional[Account]:
        """尋找帳戶"""
        return self._all_accounts.get(account_number)

    def transfer(self, from_account: Account, to_account: Account, amount: float) -> dict:
        """轉帳"""
        # 從來源帳戶提款
        withdraw_result = from_account.withdraw(amount, f"轉帳至 {to_account.account_number}")
        if not withdraw_result['success']:
            return withdraw_result

        # 存入目標帳戶
        deposit_result = to_account.deposit(amount, f"來自 {from_account.account_number} 的轉帳")

        return {
            'success': True,
            'message': f'成功轉帳 TWD ${amount:,.2f}',
            'from_balance': from_account.balance,
            'to_balance': to_account.balance
        }

    def get_statistics(self) -> dict:
        """取得銀行統計"""
        total_deposits = Money(0)
        for account in self._all_accounts.values():
            total_deposits = total_deposits + account.balance

        return {
            'customers': len(self._customers),
            'accounts': len(self._all_accounts),
            'total_deposits': total_deposits,
        }

    def get_all_customers(self) -> List[Customer]:
        """取得所有客戶"""
        return self._customers


# ========================================
# 主程式
# ========================================

def main():
    bank = Bank("Python 銀行")

    print("""
╔══════════════════════════════════════════════════════╗
║            銀行帳戶管理系統 v1.0                       ║
║           展示 Python 物件導向應用                     ║
╚══════════════════════════════════════════════════════╝
    """)

    current_customer = None
    current_account = None

    while True:
        stats = bank.get_statistics()
        print(f"""
🏦 {bank.name}
   客戶: {stats['customers']} | 帳戶: {stats['accounts']} | 總存款: {stats['total_deposits']}
   目前客戶: {current_customer.name if current_customer else '無'}
   目前帳戶: {current_account.account_number if current_account else '無'}

【選單】
  1. 註冊客戶      2. 開立帳戶      3. 選擇帳戶
  4. 存款          5. 提款          6. 轉帳
  7. 查詢餘額      8. 交易紀錄      9. 套用利息
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n感謝使用，再見！")
            break

        elif choice == '1':
            print("\n📝 註冊新客戶")
            print("=" * 40)

            name = input("姓名: ").strip()
            if not name:
                print("❌ 姓名不能為空！")
                continue

            phone = input("電話: ").strip()
            email = input("Email: ").strip()

            customer = bank.register_customer(name, phone, email)
            current_customer = customer
            print(f"\n✅ 註冊成功！")
            print(f"   客戶編號: {customer.id}")

        elif choice == '2':
            if not current_customer:
                print("❌ 請先註冊或選擇客戶！")
                continue

            print("\n🏧 開立帳戶")
            print("=" * 40)
            print("  1. 儲蓄帳戶 (利率 2%)")
            print("  2. 支票帳戶 (可透支)")
            print("  3. 定期存款 (利率 5%)")

            account_type = input("\n選擇帳戶類型: ").strip()

            if account_type == '1':
                initial = float(input("初始存款: ") or "0")
                account = bank.open_savings_account(current_customer, initial)
            elif account_type == '2':
                initial = float(input("初始存款: ") or "0")
                limit = float(input("透支額度 (預設 10000): ") or "10000")
                account = bank.open_checking_account(current_customer, initial, limit)
            elif account_type == '3':
                amount = float(input("存款金額: "))
                term = int(input("期限（月）: ") or "12")
                account = bank.open_fixed_deposit(current_customer, amount, term)
            else:
                print("❌ 無效的選擇！")
                continue

            current_account = account
            print(f"\n✅ 帳戶開立成功！")
            print(f"   {account.get_account_type()}")
            print(f"   帳號: {account.account_number}")
            print(f"   餘額: {account.balance}")

        elif choice == '3':
            customers = bank.get_all_customers()
            if not customers:
                print("❌ 尚無客戶！")
                continue

            print("\n👥 選擇客戶")
            print("=" * 40)
            for i, c in enumerate(customers, 1):
                print(f"  {i}. {c}")

            try:
                idx = int(input("\n選擇客戶: ")) - 1
                current_customer = customers[idx]

                accounts = current_customer.get_accounts()
                if accounts:
                    print(f"\n帳戶列表:")
                    for i, acc in enumerate(accounts, 1):
                        print(f"  {i}. {acc.account_number} | {acc.get_account_type()} | {acc.balance}")

                    acc_idx = int(input("\n選擇帳戶: ")) - 1
                    current_account = accounts[acc_idx]
                    print(f"✅ 已選擇 {current_account.account_number}")
                else:
                    print("該客戶尚無帳戶")
                    current_account = None

            except (ValueError, IndexError):
                print("❌ 無效的選擇！")

        elif choice == '4':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            print("\n💵 存款")
            print("=" * 40)
            try:
                amount = float(input("存款金額: "))
                result = current_account.deposit(amount)

                if result['success']:
                    print(f"\n✅ {result['message']}")
                    print(f"   新餘額: {result['balance']}")
                else:
                    print(f"\n❌ {result['message']}")
            except ValueError:
                print("❌ 請輸入有效金額！")

        elif choice == '5':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            print("\n💸 提款")
            print("=" * 40)
            print(f"目前餘額: {current_account.balance}")

            try:
                amount = float(input("提款金額: "))
                result = current_account.withdraw(amount)

                if result['success']:
                    print(f"\n✅ {result['message']}")
                    print(f"   新餘額: {result['balance']}")
                else:
                    print(f"\n❌ {result['message']}")
            except ValueError:
                print("❌ 請輸入有效金額！")

        elif choice == '6':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            print("\n💳 轉帳")
            print("=" * 40)

            to_account_num = input("轉入帳號: ").strip()
            to_account = bank.find_account(to_account_num)

            if not to_account:
                print("❌ 找不到該帳戶！")
                continue

            if to_account == current_account:
                print("❌ 不能轉帳給自己！")
                continue

            try:
                amount = float(input("轉帳金額: "))
                result = bank.transfer(current_account, to_account, amount)

                if result['success']:
                    print(f"\n✅ {result['message']}")
                    print(f"   您的餘額: {result['from_balance']}")
                else:
                    print(f"\n❌ {result['message']}")
            except ValueError:
                print("❌ 請輸入有效金額！")

        elif choice == '7':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            print("\n💰 帳戶資訊")
            print(current_account.get_statement())

            if isinstance(current_account, CheckingAccount):
                print(f"  透支額度: {current_account.overdraft_limit}")

        elif choice == '8':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            print("\n📜 交易紀錄")
            print("=" * 60)

            transactions = current_account.get_transactions(20)
            if not transactions:
                print("  (無交易紀錄)")
            else:
                for t in transactions:
                    print(f"  {t}")

        elif choice == '9':
            if not current_account:
                print("❌ 請先選擇帳戶！")
                continue

            if isinstance(current_account, SavingsAccount):
                result = current_account.apply_interest()
                print(f"\n✅ 已套用利息: {result['interest']}")
                print(f"   新餘額: {result['balance']}")
            elif isinstance(current_account, FixedDepositAccount):
                interest = current_account.calculate_interest()
                print(f"\n📊 預計到期利息: {interest}")
            else:
                print("❌ 此帳戶類型不計息")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
