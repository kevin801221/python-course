"""
寵物商店系統 - Pet Shop System
===============================
進階應用：展示 Python 物件導向程式設計入門

功能：
1. 類別與物件基礎
2. 建構子與屬性
3. 實例方法與類別方法
4. 物件互動
"""

from datetime import datetime, date
from typing import List, Optional


# ========================================
# 1. 基本類別定義
# ========================================

class Pet:
    """
    寵物類別 - 展示類別的基本結構

    屬性：
        name: 名字
        species: 物種
        age: 年齡
        price: 價格
    """

    # 類別屬性（所有實例共享）
    total_pets = 0

    def __init__(self, name: str, species: str, age: int, price: float):
        """
        建構子 - 初始化寵物

        Args:
            name: 寵物名字
            species: 物種
            age: 年齡（月）
            price: 價格
        """
        # 實例屬性
        self.name = name
        self.species = species
        self.age = age
        self.price = price
        self.is_sold = False
        self.owner = None
        self.created_at = datetime.now()

        # 更新類別計數器
        Pet.total_pets += 1
        self.id = Pet.total_pets

    def __str__(self) -> str:
        """字串表示"""
        status = "已售出" if self.is_sold else "待售"
        return f"[{self.id}] {self.name} ({self.species}) - {self.age}個月 - ${self.price:,.0f} [{status}]"

    def __repr__(self) -> str:
        """正式表示"""
        return f"Pet(name='{self.name}', species='{self.species}', age={self.age}, price={self.price})"

    # 實例方法
    def get_info(self) -> dict:
        """取得寵物資訊"""
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'age_years': self.age / 12,
            'price': self.price,
            'is_sold': self.is_sold,
            'owner': self.owner,
        }

    def make_sound(self) -> str:
        """發出聲音"""
        sounds = {
            '狗': '汪汪！',
            '貓': '喵喵～',
            '鳥': '啾啾！',
            '兔子': '（安靜地抽動鼻子）',
            '倉鼠': '吱吱！',
            '魚': '（吐泡泡）',
        }
        return sounds.get(self.species, '...')

    def age_in_years(self) -> float:
        """轉換年齡為年"""
        return self.age / 12

    def apply_discount(self, percent: float):
        """套用折扣"""
        if 0 < percent <= 100:
            self.price = self.price * (1 - percent / 100)

    # 類別方法
    @classmethod
    def get_total_pets(cls) -> int:
        """取得總寵物數"""
        return cls.total_pets

    @classmethod
    def from_dict(cls, data: dict) -> 'Pet':
        """從字典建立寵物（工廠方法）"""
        return cls(
            name=data['name'],
            species=data['species'],
            age=data['age'],
            price=data['price']
        )

    # 靜態方法
    @staticmethod
    def is_valid_age(age: int) -> bool:
        """驗證年齡"""
        return 0 <= age <= 300  # 月


# ========================================
# 2. 客戶類別
# ========================================

class Customer:
    """客戶類別"""

    def __init__(self, name: str, phone: str = "", email: str = ""):
        self.name = name
        self.phone = phone
        self.email = email
        self.pets: List[Pet] = []
        self.purchase_history = []
        self.registered_at = datetime.now()

    def __str__(self) -> str:
        return f"客戶: {self.name} (擁有 {len(self.pets)} 隻寵物)"

    def buy_pet(self, pet: Pet) -> bool:
        """購買寵物"""
        if pet.is_sold:
            return False

        pet.is_sold = True
        pet.owner = self.name
        self.pets.append(pet)
        self.purchase_history.append({
            'pet': pet,
            'date': datetime.now(),
            'price': pet.price,
        })
        return True

    def get_total_spent(self) -> float:
        """計算總消費"""
        return sum(p['price'] for p in self.purchase_history)

    def list_pets(self) -> List[str]:
        """列出擁有的寵物"""
        return [pet.name for pet in self.pets]


# ========================================
# 3. 寵物商店類別
# ========================================

class PetShop:
    """寵物商店類別"""

    def __init__(self, name: str, address: str = ""):
        self.name = name
        self.address = address
        self.inventory: List[Pet] = []
        self.customers: List[Customer] = []
        self.sales_records = []

    def __str__(self) -> str:
        available = len([p for p in self.inventory if not p.is_sold])
        return f"🏪 {self.name} - 有 {available} 隻寵物待售"

    def add_pet(self, pet: Pet):
        """進貨寵物"""
        self.inventory.append(pet)

    def add_customer(self, customer: Customer):
        """新增客戶"""
        self.customers.append(customer)

    def get_available_pets(self) -> List[Pet]:
        """取得待售寵物"""
        return [p for p in self.inventory if not p.is_sold]

    def get_pets_by_species(self, species: str) -> List[Pet]:
        """依物種篩選"""
        return [p for p in self.get_available_pets() if p.species == species]

    def get_pets_by_price_range(self, min_price: float, max_price: float) -> List[Pet]:
        """依價格篩選"""
        return [p for p in self.get_available_pets() if min_price <= p.price <= max_price]

    def sell_pet(self, pet_id: int, customer: Customer) -> dict:
        """銷售寵物"""
        pet = self.find_pet_by_id(pet_id)

        if not pet:
            return {'success': False, 'message': '找不到該寵物'}

        if pet.is_sold:
            return {'success': False, 'message': '該寵物已售出'}

        # 進行銷售
        customer.buy_pet(pet)
        self.sales_records.append({
            'pet': pet,
            'customer': customer,
            'date': datetime.now(),
            'amount': pet.price,
        })

        return {'success': True, 'message': f'{customer.name} 購買了 {pet.name}'}

    def find_pet_by_id(self, pet_id: int) -> Optional[Pet]:
        """依 ID 尋找寵物"""
        for pet in self.inventory:
            if pet.id == pet_id:
                return pet
        return None

    def get_sales_summary(self) -> dict:
        """銷售摘要"""
        total_sales = sum(r['amount'] for r in self.sales_records)
        return {
            'total_sales': total_sales,
            'pets_sold': len(self.sales_records),
            'pets_available': len(self.get_available_pets()),
            'total_customers': len(self.customers),
        }

    def get_inventory_value(self) -> float:
        """庫存價值"""
        return sum(p.price for p in self.get_available_pets())

    def display_inventory(self):
        """顯示庫存"""
        print(f"\n{'='*60}")
        print(f"  {self.name} - 寵物庫存")
        print(f"{'='*60}")

        available = self.get_available_pets()
        if not available:
            print("  (目前沒有待售寵物)")
        else:
            for pet in available:
                sound = pet.make_sound()
                print(f"  {pet} {sound}")

        print(f"{'='*60}")
        print(f"  庫存價值: ${self.get_inventory_value():,.0f}")

    def add_sample_data(self):
        """新增範例資料"""
        pets_data = [
            ("小白", "狗", 6, 15000),
            ("咪咪", "貓", 4, 12000),
            ("阿黃", "狗", 12, 18000),
            ("花花", "貓", 3, 10000),
            ("彩虹", "鳥", 8, 3000),
            ("雪球", "兔子", 5, 2500),
            ("肥仔", "倉鼠", 2, 800),
            ("小金", "魚", 1, 500),
            ("黑皮", "狗", 24, 20000),
            ("虎斑", "貓", 10, 14000),
        ]

        for name, species, age, price in pets_data:
            self.add_pet(Pet(name, species, age, price))


# ========================================
# 主程式
# ========================================

def main():
    # 建立寵物商店
    shop = PetShop("快樂寵物店", "台北市中山區")

    print("""
╔══════════════════════════════════════════════════════╗
║              寵物商店系統 v1.0                         ║
║           展示 Python 物件導向入門                     ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print(f"""
{shop}

【選單】
  1. 查看庫存          2. 新增寵物
  3. 搜尋寵物          4. 購買寵物
  5. 客戶管理          6. 銷售報表
  7. 載入範例          0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            shop.display_inventory()

        elif choice == '2':
            print("\n➕ 新增寵物")
            print("=" * 40)

            name = input("名字: ").strip()
            if not name:
                print("❌ 名字不能為空！")
                continue

            print("物種選項: 狗, 貓, 鳥, 兔子, 倉鼠, 魚")
            species = input("物種: ").strip() or "狗"

            try:
                age = int(input("年齡（月）: "))
                price = float(input("價格: "))

                if not Pet.is_valid_age(age):
                    print("❌ 無效的年齡！")
                    continue

                pet = Pet(name, species, age, price)
                shop.add_pet(pet)
                print(f"\n✅ 已新增: {pet}")
                print(f"   {pet.name} 說: {pet.make_sound()}")

            except ValueError:
                print("❌ 請輸入有效的數字！")

        elif choice == '3':
            print("\n🔍 搜尋寵物")
            print("=" * 40)
            print("  1. 依物種搜尋")
            print("  2. 依價格範圍搜尋")

            search_type = input("選擇: ").strip()

            if search_type == '1':
                species = input("物種: ").strip()
                results = shop.get_pets_by_species(species)
            elif search_type == '2':
                try:
                    min_p = float(input("最低價格: "))
                    max_p = float(input("最高價格: "))
                    results = shop.get_pets_by_price_range(min_p, max_p)
                except ValueError:
                    print("❌ 請輸入有效的數字！")
                    continue
            else:
                continue

            print(f"\n找到 {len(results)} 隻寵物:")
            for pet in results:
                print(f"  {pet}")

        elif choice == '4':
            print("\n💰 購買寵物")
            print("=" * 40)

            available = shop.get_available_pets()
            if not available:
                print("❌ 目前沒有待售寵物！")
                continue

            print("待售寵物:")
            for pet in available:
                print(f"  {pet}")

            try:
                pet_id = int(input("\n輸入寵物 ID: "))
                customer_name = input("客戶名稱: ").strip() or "匿名客戶"

                # 找或建立客戶
                customer = None
                for c in shop.customers:
                    if c.name == customer_name:
                        customer = c
                        break

                if not customer:
                    customer = Customer(customer_name)
                    shop.add_customer(customer)

                result = shop.sell_pet(pet_id, customer)
                if result['success']:
                    print(f"\n✅ {result['message']}")
                    pet = shop.find_pet_by_id(pet_id)
                    print(f"   金額: ${pet.price:,.0f}")
                else:
                    print(f"\n❌ {result['message']}")

            except ValueError:
                print("❌ 請輸入有效的數字！")

        elif choice == '5':
            print("\n👥 客戶管理")
            print("=" * 40)

            if not shop.customers:
                print("(尚無客戶)")
            else:
                for i, customer in enumerate(shop.customers, 1):
                    print(f"\n{i}. {customer}")
                    print(f"   總消費: ${customer.get_total_spent():,.0f}")
                    if customer.pets:
                        print(f"   寵物: {', '.join(customer.list_pets())}")

        elif choice == '6':
            print("\n📊 銷售報表")
            print("=" * 40)

            summary = shop.get_sales_summary()
            print(f"  總銷售額: ${summary['total_sales']:,.0f}")
            print(f"  已售出: {summary['pets_sold']} 隻")
            print(f"  待售中: {summary['pets_available']} 隻")
            print(f"  總客戶: {summary['total_customers']} 位")
            print(f"  庫存價值: ${shop.get_inventory_value():,.0f}")

            if shop.sales_records:
                print("\n最近銷售:")
                for record in shop.sales_records[-5:]:
                    print(f"  - {record['pet'].name} → {record['customer'].name} (${record['amount']:,.0f})")

        elif choice == '7':
            shop.add_sample_data()
            print("✅ 已載入範例資料！")
            print(f"   建立了 {Pet.get_total_pets()} 隻寵物")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
