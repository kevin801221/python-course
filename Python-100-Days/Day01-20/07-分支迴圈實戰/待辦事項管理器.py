"""
待辦事項管理器 - Todo List Manager
===================================
進階應用：綜合運用分支和迴圈結構

功能：
1. 新增/刪除/編輯待辦事項
2. 優先級管理
3. 分類功能
4. 搜尋和篩選
5. 進度追蹤
"""

from datetime import datetime, timedelta
import json
import os


class TodoItem:
    """待辦事項類別"""

    PRIORITIES = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    CATEGORIES = ['工作', '學習', '生活', '其他']

    def __init__(self, title, priority='medium', category='其他', due_date=None):
        self.id = datetime.now().strftime('%Y%m%d%H%M%S%f')[:16]
        self.title = title
        self.priority = priority
        self.category = category
        self.completed = False
        self.created_at = datetime.now()
        self.due_date = due_date
        self.completed_at = None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'category': self.category,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data):
        item = cls(data['title'], data['priority'], data['category'])
        item.id = data['id']
        item.completed = data['completed']
        item.created_at = datetime.fromisoformat(data['created_at'])
        item.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        item.completed_at = datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        return item

    def display(self, show_id=False):
        status = '✅' if self.completed else '⬜'
        priority_icon = self.PRIORITIES.get(self.priority, '🟡')
        due = ""
        if self.due_date:
            days_left = (self.due_date - datetime.now()).days
            if days_left < 0:
                due = " ⚠️ 已過期!"
            elif days_left == 0:
                due = " 📅 今天到期"
            elif days_left <= 3:
                due = f" 📅 {days_left}天後到期"

        id_str = f"[{self.id[-4:]}] " if show_id else ""
        return f"{status} {priority_icon} {id_str}[{self.category}] {self.title}{due}"


class TodoManager:
    """待辦事項管理器"""

    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.todos = []
        self.load()

    def load(self):
        """載入資料"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(d) for d in data]
            except:
                self.todos = []

    def save(self):
        """儲存資料"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.todos], f, ensure_ascii=False, indent=2)

    def add(self, title, priority='medium', category='其他', due_days=None):
        """新增待辦事項"""
        due_date = datetime.now() + timedelta(days=due_days) if due_days else None
        item = TodoItem(title, priority, category, due_date)
        self.todos.append(item)
        self.save()
        return item

    def delete(self, item_id):
        """刪除待辦事項"""
        for i, todo in enumerate(self.todos):
            if todo.id.endswith(item_id) or todo.id == item_id:
                deleted = self.todos.pop(i)
                self.save()
                return deleted
        return None

    def toggle(self, item_id):
        """切換完成狀態"""
        for todo in self.todos:
            if todo.id.endswith(item_id) or todo.id == item_id:
                todo.completed = not todo.completed
                todo.completed_at = datetime.now() if todo.completed else None
                self.save()
                return todo
        return None

    def edit(self, item_id, new_title):
        """編輯待辦事項"""
        for todo in self.todos:
            if todo.id.endswith(item_id) or todo.id == item_id:
                todo.title = new_title
                self.save()
                return todo
        return None

    def filter_by_category(self, category):
        """依分類篩選"""
        return [t for t in self.todos if t.category == category]

    def filter_by_priority(self, priority):
        """依優先級篩選"""
        return [t for t in self.todos if t.priority == priority]

    def search(self, keyword):
        """搜尋"""
        return [t for t in self.todos if keyword.lower() in t.title.lower()]

    def get_pending(self):
        """取得未完成項目"""
        return [t for t in self.todos if not t.completed]

    def get_completed(self):
        """取得已完成項目"""
        return [t for t in self.todos if t.completed]

    def get_overdue(self):
        """取得過期項目"""
        now = datetime.now()
        return [t for t in self.todos if t.due_date and t.due_date < now and not t.completed]

    def get_stats(self):
        """取得統計"""
        total = len(self.todos)
        completed = len(self.get_completed())
        pending = len(self.get_pending())
        overdue = len(self.get_overdue())

        by_category = {}
        by_priority = {}
        for todo in self.todos:
            by_category[todo.category] = by_category.get(todo.category, 0) + 1
            by_priority[todo.priority] = by_priority.get(todo.priority, 0) + 1

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': completed / total * 100 if total > 0 else 0,
            'by_category': by_category,
            'by_priority': by_priority,
        }


def display_todos(todos, title="待辦事項"):
    """顯示待辦事項列表"""
    print(f"\n{'─' * 50}")
    print(f"  {title} ({len(todos)} 項)")
    print('─' * 50)

    if not todos:
        print("  (空)")
    else:
        # 按優先級排序
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_todos = sorted(todos, key=lambda x: (x.completed, priority_order.get(x.priority, 1)))

        for todo in sorted_todos:
            print(f"  {todo.display(show_id=True)}")

    print('─' * 50)


def main():
    manager = TodoManager()

    print("""
╔══════════════════════════════════════════════════════╗
║            待辦事項管理器 v1.0                         ║
║         綜合運用分支和迴圈結構                          ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        stats = manager.get_stats()
        overdue = manager.get_overdue()

        print(f"""
📋 待辦事項 | 待完成: {stats['pending']} | 已完成: {stats['completed']} | 完成率: {stats['completion_rate']:.0f}%
{f"⚠️  有 {len(overdue)} 項已過期！" if overdue else ""}

【選單】
  1. 查看所有  2. 新增     3. 完成/取消  4. 刪除
  5. 編輯      6. 篩選     7. 搜尋       8. 統計
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n資料已自動儲存，再見！👋")
            break

        elif choice == '1':
            print("\n查看選項: 1.全部 2.未完成 3.已完成 4.過期")
            sub = input("選擇: ").strip()
            if sub == '1':
                display_todos(manager.todos, "所有待辦事項")
            elif sub == '2':
                display_todos(manager.get_pending(), "未完成事項")
            elif sub == '3':
                display_todos(manager.get_completed(), "已完成事項")
            elif sub == '4':
                display_todos(manager.get_overdue(), "過期事項")

        elif choice == '2':
            title = input("待辦事項內容: ").strip()
            if not title:
                print("❌ 內容不能為空！")
                continue

            print("優先級: 1.高 2.中 3.低")
            p = input("選擇 (預設2): ").strip()
            priority = {'1': 'high', '2': 'medium', '3': 'low'}.get(p, 'medium')

            print(f"分類: {', '.join(f'{i+1}.{c}' for i, c in enumerate(TodoItem.CATEGORIES))}")
            c = input("選擇 (預設4): ").strip()
            try:
                category = TodoItem.CATEGORIES[int(c) - 1]
            except:
                category = '其他'

            due = input("幾天後到期 (留空=無期限): ").strip()
            due_days = int(due) if due.isdigit() else None

            item = manager.add(title, priority, category, due_days)
            print(f"✅ 已新增: {item.display()}")

        elif choice == '3':
            display_todos(manager.get_pending(), "未完成事項")
            item_id = input("輸入ID (後4碼): ").strip()
            item = manager.toggle(item_id)
            if item:
                status = "完成" if item.completed else "未完成"
                print(f"✅ 已標記為{status}: {item.title}")
            else:
                print("❌ 找不到該項目！")

        elif choice == '4':
            display_todos(manager.todos, "所有待辦事項")
            item_id = input("輸入要刪除的ID (後4碼): ").strip()
            item = manager.delete(item_id)
            if item:
                print(f"✅ 已刪除: {item.title}")
            else:
                print("❌ 找不到該項目！")

        elif choice == '5':
            display_todos(manager.todos, "所有待辦事項")
            item_id = input("輸入要編輯的ID (後4碼): ").strip()
            new_title = input("新的內容: ").strip()
            item = manager.edit(item_id, new_title)
            if item:
                print(f"✅ 已更新: {item.display()}")
            else:
                print("❌ 找不到該項目！")

        elif choice == '6':
            print("篩選方式: 1.依分類 2.依優先級")
            sub = input("選擇: ").strip()

            if sub == '1':
                print(f"分類: {', '.join(f'{i+1}.{c}' for i, c in enumerate(TodoItem.CATEGORIES))}")
                c = input("選擇: ").strip()
                try:
                    category = TodoItem.CATEGORIES[int(c) - 1]
                    display_todos(manager.filter_by_category(category), f"{category} 分類")
                except:
                    print("❌ 無效的選擇！")
            elif sub == '2':
                print("優先級: 1.高 2.中 3.低")
                p = input("選擇: ").strip()
                priority = {'1': 'high', '2': 'medium', '3': 'low'}.get(p)
                if priority:
                    display_todos(manager.filter_by_priority(priority), f"{priority} 優先級")
                else:
                    print("❌ 無效的選擇！")

        elif choice == '7':
            keyword = input("搜尋關鍵字: ").strip()
            results = manager.search(keyword)
            display_todos(results, f"搜尋結果: '{keyword}'")

        elif choice == '8':
            stats = manager.get_stats()
            print(f"""
╔══════════════════════════════════════╗
║              統計報告                 ║
╠══════════════════════════════════════╣
║  總項目數: {stats['total']:>5} 項                 ║
║  已完成:   {stats['completed']:>5} 項                 ║
║  待完成:   {stats['pending']:>5} 項                 ║
║  已過期:   {stats['overdue']:>5} 項                 ║
║  完成率:   {stats['completion_rate']:>5.1f}%                ║
╠══════════════════════════════════════╣
║  依分類:                              ║""")
            for cat, count in stats['by_category'].items():
                print(f"║    {cat}: {count} 項")
            print(f"""╠══════════════════════════════════════╣
║  依優先級:                            ║
║    🔴 高: {stats['by_priority'].get('high', 0)} 項
║    🟡 中: {stats['by_priority'].get('medium', 0)} 項
║    🟢 低: {stats['by_priority'].get('low', 0)} 項
╚══════════════════════════════════════╝
""")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
