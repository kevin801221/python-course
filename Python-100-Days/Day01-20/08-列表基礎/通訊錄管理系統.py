"""
通訊錄管理系統 - Contact Manager
================================
進階應用：展示 Python 列表的實際應用

功能：
1. 聯絡人 CRUD 操作
2. 分組管理
3. 搜尋功能
4. 匯入匯出
"""

import json
from datetime import datetime


class Contact:
    """聯絡人類別"""

    def __init__(self, name, phone, email="", group="一般"):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group
        self.created_at = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return vars(self)

    def display(self):
        return f"👤 {self.name} | 📱 {self.phone} | 📧 {self.email or '-'} | 🏷️ {self.group}"


class ContactManager:
    """通訊錄管理器"""

    GROUPS = ["一般", "家人", "朋友", "同事", "客戶"]

    def __init__(self):
        # 使用列表儲存所有聯絡人
        self.contacts = []

    def add(self, name, phone, email="", group="一般"):
        """新增聯絡人 - 使用 list.append()"""
        contact = Contact(name, phone, email, group)
        self.contacts.append(contact)
        return contact

    def delete(self, index):
        """刪除聯絡人 - 使用 list.pop()"""
        if 0 <= index < len(self.contacts):
            return self.contacts.pop(index)
        return None

    def update(self, index, **kwargs):
        """更新聯絡人 - 使用索引存取"""
        if 0 <= index < len(self.contacts):
            contact = self.contacts[index]
            for key, value in kwargs.items():
                if hasattr(contact, key) and value:
                    setattr(contact, key, value)
            return contact
        return None

    def search(self, keyword):
        """搜尋 - 使用列表推導式"""
        keyword = keyword.lower()
        return [c for c in self.contacts
                if keyword in c.name.lower()
                or keyword in c.phone
                or keyword in c.email.lower()]

    def filter_by_group(self, group):
        """篩選分組 - 使用 filter()"""
        return list(filter(lambda c: c.group == group, self.contacts))

    def sort_by_name(self):
        """排序 - 使用 list.sort()"""
        self.contacts.sort(key=lambda c: c.name)

    def get_all(self):
        """取得所有 - 使用 list.copy()"""
        return self.contacts.copy()

    def count(self):
        """計數 - 使用 len()"""
        return len(self.contacts)

    def get_groups_count(self):
        """統計各分組數量"""
        counts = {}
        for contact in self.contacts:
            counts[contact.group] = counts.get(contact.group, 0) + 1
        return counts

    def export_json(self, filename="contacts.json"):
        """匯出 JSON"""
        data = [c.to_dict() for c in self.contacts]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename

    def import_json(self, filename="contacts.json"):
        """匯入 JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                self.add(item['name'], item['phone'],
                        item.get('email', ''), item.get('group', '一般'))
            return len(data)
        except FileNotFoundError:
            return 0

    def add_sample_data(self):
        """新增範例資料"""
        samples = [
            ("王小明", "0912-345-678", "ming@email.com", "朋友"),
            ("李大華", "0923-456-789", "dahua@email.com", "同事"),
            ("張美美", "0934-567-890", "mei@email.com", "家人"),
            ("陳建中", "0945-678-901", "jian@email.com", "客戶"),
            ("林志玲", "0956-789-012", "ling@email.com", "朋友"),
        ]
        for name, phone, email, group in samples:
            self.add(name, phone, email, group)


def display_contacts(contacts, title="聯絡人列表"):
    """顯示聯絡人列表"""
    print(f"\n{'='*60}")
    print(f"  {title} (共 {len(contacts)} 人)")
    print('='*60)

    if not contacts:
        print("  (空)")
    else:
        for i, contact in enumerate(contacts, 1):
            print(f"  {i}. {contact.display()}")

    print('='*60)


def main():
    manager = ContactManager()

    print("""
╔══════════════════════════════════════════════════════╗
║            通訊錄管理系統 v1.0                         ║
║           展示 Python 列表的應用                       ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print(f"""
📇 通訊錄 | 共 {manager.count()} 位聯絡人

【選單】
  1. 查看全部    2. 新增聯絡人   3. 搜尋
  4. 編輯        5. 刪除         6. 依分組查看
  7. 排序        8. 匯出/匯入    9. 載入範例
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            save = input("是否儲存資料? (y/n): ").lower()
            if save == 'y':
                manager.export_json()
                print("✅ 已儲存到 contacts.json")
            print("\n再見！👋")
            break

        elif choice == '1':
            display_contacts(manager.get_all())

        elif choice == '2':
            name = input("姓名: ").strip()
            if not name:
                print("❌ 姓名不能為空！")
                continue

            phone = input("電話: ").strip()
            email = input("Email (可選): ").strip()

            print(f"分組: {', '.join(f'{i+1}.{g}' for i, g in enumerate(manager.GROUPS))}")
            g = input("選擇分組 (預設1): ").strip()
            try:
                group = manager.GROUPS[int(g) - 1]
            except:
                group = "一般"

            contact = manager.add(name, phone, email, group)
            print(f"✅ 已新增: {contact.display()}")

        elif choice == '3':
            keyword = input("搜尋關鍵字: ").strip()
            results = manager.search(keyword)
            display_contacts(results, f"搜尋結果: '{keyword}'")

        elif choice == '4':
            display_contacts(manager.get_all())
            try:
                idx = int(input("選擇要編輯的編號: ")) - 1
                print("留空表示不修改")
                name = input("新姓名: ").strip()
                phone = input("新電話: ").strip()
                email = input("新Email: ").strip()

                contact = manager.update(idx, name=name, phone=phone, email=email)
                if contact:
                    print(f"✅ 已更新: {contact.display()}")
                else:
                    print("❌ 無效的編號！")
            except ValueError:
                print("❌ 請輸入數字！")

        elif choice == '5':
            display_contacts(manager.get_all())
            try:
                idx = int(input("選擇要刪除的編號: ")) - 1
                contact = manager.delete(idx)
                if contact:
                    print(f"✅ 已刪除: {contact.name}")
                else:
                    print("❌ 無效的編號！")
            except ValueError:
                print("❌ 請輸入數字！")

        elif choice == '6':
            print(f"分組: {', '.join(f'{i+1}.{g}' for i, g in enumerate(manager.GROUPS))}")
            g = input("選擇分組: ").strip()
            try:
                group = manager.GROUPS[int(g) - 1]
                results = manager.filter_by_group(group)
                display_contacts(results, f"{group} 分組")
            except:
                print("❌ 無效的選擇！")

        elif choice == '7':
            manager.sort_by_name()
            print("✅ 已按姓名排序！")
            display_contacts(manager.get_all())

        elif choice == '8':
            print("1. 匯出  2. 匯入")
            sub = input("選擇: ").strip()
            if sub == '1':
                filename = manager.export_json()
                print(f"✅ 已匯出到 {filename}")
            elif sub == '2':
                count = manager.import_json()
                print(f"✅ 已匯入 {count} 筆資料")

        elif choice == '9':
            manager.add_sample_data()
            print("✅ 已載入範例資料！")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
