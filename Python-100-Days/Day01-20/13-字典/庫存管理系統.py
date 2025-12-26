"""
庫存管理系統 - Inventory Management System
==========================================
進階應用：展示 Python 字典的各種應用

功能：
1. 商品 CRUD 操作
2. 庫存追蹤
3. 銷售記錄
4. 報表生成
"""

from datetime import datetime
from collections import defaultdict
import json


class InventoryManager:
    """庫存管理器"""

    def __init__(self):
        # 商品字典: {商品ID: {商品資訊}}
        self.products = {}

        # 庫存字典: {商品ID: 數量}
        self.stock = defaultdict(int)

        # 銷售記錄: [{銷售資訊}, ...]
        self.sales = []

        # 進貨記錄
        self.purchases = []

        # 自動編號
        self._next_id = 1

    def add_product(self, name: str, price: float, category: str = "一般") -> dict:
        """新增商品"""
        product_id = f"P{self._next_id:04d}"
        self._next_id += 1

        self.products[product_id] = {
            'id': product_id,
            'name': name,
            'price': price,
            'category': category,
            'created_at': datetime.now().isoformat(),
        }
        return self.products[product_id]

    def update_product(self, product_id: str, **kwargs) -> dict:
        """更新商品資訊"""
        if product_id in self.products:
            for key, value in kwargs.items():
                if key in self.products[product_id] and key != 'id':
                    self.products[product_id][key] = value
            return self.products[product_id]
        return None

    def delete_product(self, product_id: str) -> bool:
        """刪除商品"""
        if product_id in self.products:
            del self.products[product_id]
            if product_id in self.stock:
                del self.stock[product_id]
            return True
        return False

    def get_product(self, product_id: str) -> dict:
        """取得商品"""
        return self.products.get(product_id)

    def search_products(self, keyword: str) -> list:
        """搜尋商品"""
        keyword = keyword.lower()
        results = []
        for product in self.products.values():
            if keyword in product['name'].lower() or keyword in product['category'].lower():
                results.append(product)
        return results

    def add_stock(self, product_id: str, quantity: int, unit_cost: float = 0):
        """進貨"""
        if product_id not in self.products:
            return False

        self.stock[product_id] += quantity
        self.purchases.append({
            'product_id': product_id,
            'quantity': quantity,
            'unit_cost': unit_cost,
            'total_cost': unit_cost * quantity,
            'date': datetime.now().isoformat(),
        })
        return True

    def sell(self, product_id: str, quantity: int) -> dict:
        """銷售"""
        if product_id not in self.products:
            return {'success': False, 'message': '商品不存在'}

        if self.stock[product_id] < quantity:
            return {'success': False, 'message': f'庫存不足 (目前: {self.stock[product_id]})'}

        product = self.products[product_id]
        total = product['price'] * quantity
        self.stock[product_id] -= quantity

        sale = {
            'product_id': product_id,
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total': total,
            'date': datetime.now().isoformat(),
        }
        self.sales.append(sale)

        return {'success': True, 'sale': sale}

    def get_stock(self, product_id: str) -> int:
        """取得庫存量"""
        return self.stock.get(product_id, 0)

    def get_low_stock(self, threshold: int = 5) -> list:
        """低庫存警告"""
        low_stock = []
        for product_id, quantity in self.stock.items():
            if quantity <= threshold:
                product = self.products.get(product_id)
                if product:
                    low_stock.append({
                        'product': product,
                        'stock': quantity,
                    })
        return low_stock

    def get_sales_report(self) -> dict:
        """銷售報表"""
        report = {
            'total_sales': 0,
            'total_items': 0,
            'by_product': defaultdict(lambda: {'quantity': 0, 'revenue': 0}),
            'by_category': defaultdict(lambda: {'quantity': 0, 'revenue': 0}),
        }

        for sale in self.sales:
            report['total_sales'] += sale['total']
            report['total_items'] += sale['quantity']

            product = self.products.get(sale['product_id'])
            if product:
                report['by_product'][sale['product_name']]['quantity'] += sale['quantity']
                report['by_product'][sale['product_name']]['revenue'] += sale['total']

                report['by_category'][product['category']]['quantity'] += sale['quantity']
                report['by_category'][product['category']]['revenue'] += sale['total']

        return report

    def get_inventory_value(self) -> float:
        """計算庫存總價值"""
        total = 0
        for product_id, quantity in self.stock.items():
            product = self.products.get(product_id)
            if product:
                total += product['price'] * quantity
        return total

    def export_data(self, filename: str = "inventory.json"):
        """匯出資料"""
        data = {
            'products': self.products,
            'stock': dict(self.stock),
            'sales': self.sales,
            'purchases': self.purchases,
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename

    def add_sample_data(self):
        """新增範例資料"""
        samples = [
            ("蘋果 iPhone 15", 29900, "手機"),
            ("三星 Galaxy S24", 26900, "手機"),
            ("Sony 藍牙耳機", 4990, "配件"),
            ("Apple Watch", 12900, "穿戴"),
            ("iPad Pro", 35900, "平板"),
            ("MacBook Air", 39900, "筆電"),
            ("充電線", 299, "配件"),
            ("保護殼", 499, "配件"),
        ]

        for name, price, category in samples:
            product = self.add_product(name, price, category)
            self.add_stock(product['id'], 10 + (hash(name) % 20), price * 0.7)


def display_products(manager, products=None):
    """顯示商品列表"""
    if products is None:
        products = list(manager.products.values())

    print("\n" + "=" * 70)
    print(f"{'ID':^8} {'名稱':^20} {'價格':^10} {'分類':^8} {'庫存':^6}")
    print("-" * 70)

    for product in products:
        stock = manager.get_stock(product['id'])
        stock_warning = "⚠️" if stock <= 5 else ""
        print(f"{product['id']:^8} {product['name']:^20} ${product['price']:>8,.0f} {product['category']:^8} {stock:^4}{stock_warning}")

    print("=" * 70)


def main():
    manager = InventoryManager()

    print("""
╔══════════════════════════════════════════════════════╗
║             庫存管理系統 v1.0                          ║
║           展示 Python 字典的應用                       ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print(f"""
📦 庫存管理 | 商品: {len(manager.products)} | 庫存價值: ${manager.get_inventory_value():,.0f}

【選單】
  1. 商品列表    2. 新增商品    3. 搜尋商品
  4. 進貨        5. 銷售        6. 銷售報表
  7. 低庫存警告  8. 載入範例    0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            export = input("是否匯出資料? (y/n): ").lower()
            if export == 'y':
                manager.export_data()
                print("✅ 已匯出到 inventory.json")
            print("\n再見！")
            break

        elif choice == '1':
            display_products(manager)

        elif choice == '2':
            name = input("商品名稱: ").strip()
            if not name:
                print("❌ 名稱不能為空！")
                continue

            try:
                price = float(input("價格: "))
                category = input("分類 (預設: 一般): ").strip() or "一般"

                product = manager.add_product(name, price, category)
                print(f"✅ 已新增: {product['id']} - {product['name']}")

                add_stock = input("是否立即進貨? (y/n): ").lower()
                if add_stock == 'y':
                    qty = int(input("進貨數量: "))
                    manager.add_stock(product['id'], qty)
                    print(f"✅ 已進貨 {qty} 個")

            except ValueError:
                print("❌ 請輸入有效的數字！")

        elif choice == '3':
            keyword = input("搜尋關鍵字: ").strip()
            results = manager.search_products(keyword)
            display_products(manager, results)

        elif choice == '4':
            display_products(manager)
            product_id = input("商品 ID: ").strip().upper()

            product = manager.get_product(product_id)
            if not product:
                print("❌ 商品不存在！")
                continue

            try:
                qty = int(input("進貨數量: "))
                cost = float(input("單位成本 (可選): ") or 0)

                if manager.add_stock(product_id, qty, cost):
                    print(f"✅ {product['name']} 進貨 {qty} 個")
                    print(f"   目前庫存: {manager.get_stock(product_id)}")
            except ValueError:
                print("❌ 請輸入有效的數字！")

        elif choice == '5':
            display_products(manager)
            product_id = input("商品 ID: ").strip().upper()

            product = manager.get_product(product_id)
            if not product:
                print("❌ 商品不存在！")
                continue

            print(f"商品: {product['name']} (庫存: {manager.get_stock(product_id)})")

            try:
                qty = int(input("銷售數量: "))
                result = manager.sell(product_id, qty)

                if result['success']:
                    sale = result['sale']
                    print(f"\n✅ 銷售成功！")
                    print(f"   商品: {sale['product_name']}")
                    print(f"   數量: {sale['quantity']}")
                    print(f"   金額: ${sale['total']:,.0f}")
                else:
                    print(f"❌ {result['message']}")
            except ValueError:
                print("❌ 請輸入有效的數字！")

        elif choice == '6':
            report = manager.get_sales_report()

            print("\n" + "=" * 60)
            print("                    銷售報表")
            print("=" * 60)

            print(f"\n💰 總銷售額: ${report['total_sales']:,.0f}")
            print(f"📦 總銷售量: {report['total_items']} 件")

            print("\n📊 依商品統計:")
            print("-" * 40)
            for name, data in report['by_product'].items():
                print(f"  {name}: {data['quantity']}件, ${data['revenue']:,.0f}")

            print("\n📁 依分類統計:")
            print("-" * 40)
            for category, data in report['by_category'].items():
                print(f"  {category}: {data['quantity']}件, ${data['revenue']:,.0f}")

        elif choice == '7':
            low_stock = manager.get_low_stock(5)

            print("\n⚠️ 低庫存警告 (≤5)")
            print("=" * 40)

            if not low_stock:
                print("  所有商品庫存充足！")
            else:
                for item in low_stock:
                    product = item['product']
                    print(f"  ⚠️ {product['name']}: 剩餘 {item['stock']} 個")

        elif choice == '8':
            manager.add_sample_data()
            print("✅ 已載入範例資料！")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
