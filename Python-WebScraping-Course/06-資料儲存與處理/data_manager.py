"""
資料管理器 - Data Manager
========================
這是一個完整的爬蟲資料管理應用程式，展示多種資料儲存和處理技術。

功能：
1. 多格式匯入匯出（CSV, JSON, Excel, SQLite）
2. 資料清理與驗證
3. 增量更新與去重
4. 資料分析與統計
5. 資料備份與還原

使用方法：
    python data_manager.py
"""

import json
import csv
import sqlite3
import hashlib
import shutil
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod
import re


# =====================================
# 資料模型
# =====================================

@dataclass
class ScrapedItem:
    """爬蟲資料基礎結構"""
    id: str = ""
    title: str = ""
    url: str = ""
    content: str = ""
    category: str = ""
    tags: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    scraped_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat()

    def _generate_id(self) -> str:
        """根據 URL 生成唯一 ID"""
        content = f"{self.url}{self.title}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        """轉換為字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ScrapedItem':
        """從字典建立"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# =====================================
# 資料清理器
# =====================================

class DataCleaner:
    """資料清理工具"""

    @staticmethod
    def clean_text(text: str) -> str:
        """清理文字"""
        if not text:
            return ""
        # 移除多餘空白
        text = ' '.join(text.split())
        # 移除特殊字元
        text = text.strip()
        return text

    @staticmethod
    def clean_url(url: str) -> str:
        """清理 URL"""
        if not url:
            return ""
        url = url.strip()
        # 確保有協議前綴
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    @staticmethod
    def clean_tags(tags: Any) -> list:
        """清理標籤"""
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        elif isinstance(tags, list):
            tags = [str(t).strip() for t in tags if t]
        else:
            tags = []
        return list(set(tags))  # 去重

    @staticmethod
    def validate_item(item: ScrapedItem) -> tuple[bool, list]:
        """驗證資料項目"""
        errors = []

        if not item.title:
            errors.append("標題不能為空")
        if not item.url:
            errors.append("URL 不能為空")
        elif not item.url.startswith(('http://', 'https://')):
            errors.append("URL 格式不正確")

        return len(errors) == 0, errors

    def clean_item(self, item: ScrapedItem) -> ScrapedItem:
        """清理單個資料項目"""
        item.title = self.clean_text(item.title)
        item.url = self.clean_url(item.url)
        item.content = self.clean_text(item.content)
        item.category = self.clean_text(item.category)
        item.tags = self.clean_tags(item.tags)
        item.updated_at = datetime.now().isoformat()
        return item


# =====================================
# 儲存後端（抽象類別）
# =====================================

class StorageBackend(ABC):
    """儲存後端抽象類別"""

    @abstractmethod
    def save(self, items: list[ScrapedItem]) -> int:
        pass

    @abstractmethod
    def load(self) -> list[ScrapedItem]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


# =====================================
# JSON 儲存
# =====================================

class JsonStorage(StorageBackend):
    """JSON 檔案儲存"""

    def __init__(self, filepath: str = "data.json"):
        self.filepath = Path(filepath)

    def save(self, items: list[ScrapedItem]) -> int:
        """儲存到 JSON"""
        data = [item.to_dict() for item in items]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return len(items)

    def load(self) -> list[ScrapedItem]:
        """從 JSON 載入"""
        if not self.filepath.exists():
            return []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [ScrapedItem.from_dict(d) for d in data]

    def count(self) -> int:
        return len(self.load())

    def append(self, items: list[ScrapedItem]) -> int:
        """追加資料"""
        existing = self.load()
        existing.extend(items)
        return self.save(existing)


class JsonLinesStorage(StorageBackend):
    """JSON Lines 儲存（適合大型資料集）"""

    def __init__(self, filepath: str = "data.jsonl"):
        self.filepath = Path(filepath)

    def save(self, items: list[ScrapedItem]) -> int:
        """儲存到 JSONL"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + '\n')
        return len(items)

    def load(self) -> list[ScrapedItem]:
        """從 JSONL 載入"""
        if not self.filepath.exists():
            return []
        items = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    items.append(ScrapedItem.from_dict(json.loads(line)))
        return items

    def count(self) -> int:
        if not self.filepath.exists():
            return 0
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)

    def append(self, items: list[ScrapedItem]) -> int:
        """追加資料"""
        with open(self.filepath, 'a', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + '\n')
        return len(items)


# =====================================
# CSV 儲存
# =====================================

class CsvStorage(StorageBackend):
    """CSV 檔案儲存"""

    def __init__(self, filepath: str = "data.csv"):
        self.filepath = Path(filepath)
        self.fieldnames = ['id', 'title', 'url', 'content', 'category', 'tags', 'scraped_at', 'updated_at']

    def save(self, items: list[ScrapedItem]) -> int:
        """儲存到 CSV"""
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for item in items:
                row = item.to_dict()
                row['tags'] = ', '.join(row.get('tags', []))
                row['metadata'] = json.dumps(row.get('metadata', {}))
                writer.writerow({k: row.get(k, '') for k in self.fieldnames})
        return len(items)

    def load(self) -> list[ScrapedItem]:
        """從 CSV 載入"""
        if not self.filepath.exists():
            return []
        items = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['tags'] = [t.strip() for t in row.get('tags', '').split(',') if t.strip()]
                items.append(ScrapedItem.from_dict(row))
        return items

    def count(self) -> int:
        if not self.filepath.exists():
            return 0
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f) - 1  # 減去標頭


# =====================================
# SQLite 儲存
# =====================================

class SQLiteStorage(StorageBackend):
    """SQLite 資料庫儲存"""

    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT,
                content TEXT,
                category TEXT,
                tags TEXT,
                metadata TEXT,
                scraped_at TEXT,
                updated_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 建立索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON items(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scraped_at ON items(scraped_at)')

        conn.commit()
        conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def save(self, items: list[ScrapedItem]) -> int:
        """儲存到資料庫（更新或插入）"""
        conn = self._get_connection()
        cursor = conn.cursor()
        count = 0

        for item in items:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO items
                    (id, title, url, content, category, tags, metadata, scraped_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.id,
                    item.title,
                    item.url,
                    item.content,
                    item.category,
                    ', '.join(item.tags),
                    json.dumps(item.metadata),
                    item.scraped_at,
                    item.updated_at or datetime.now().isoformat()
                ))
                count += 1
            except sqlite3.Error as e:
                print(f"儲存錯誤: {e}")

        conn.commit()
        conn.close()
        return count

    def load(self, limit: int = None, offset: int = 0) -> list[ScrapedItem]:
        """從資料庫載入"""
        conn = self._get_connection()
        cursor = conn.cursor()

        query = 'SELECT id, title, url, content, category, tags, metadata, scraped_at, updated_at FROM items'
        if limit:
            query += f' LIMIT {limit} OFFSET {offset}'

        cursor.execute(query)
        items = []

        for row in cursor.fetchall():
            items.append(ScrapedItem(
                id=row[0],
                title=row[1],
                url=row[2],
                content=row[3],
                category=row[4],
                tags=[t.strip() for t in (row[5] or '').split(',') if t.strip()],
                metadata=json.loads(row[6]) if row[6] else {},
                scraped_at=row[7],
                updated_at=row[8]
            ))

        conn.close()
        return items

    def count(self) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM items')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def search(self, keyword: str) -> list[ScrapedItem]:
        """搜尋資料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, url, content, category, tags, metadata, scraped_at, updated_at
            FROM items
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

        items = []
        for row in cursor.fetchall():
            items.append(ScrapedItem(
                id=row[0], title=row[1], url=row[2], content=row[3],
                category=row[4], tags=[t.strip() for t in (row[5] or '').split(',') if t.strip()],
                metadata=json.loads(row[6]) if row[6] else {},
                scraped_at=row[7], updated_at=row[8]
            ))

        conn.close()
        return items

    def get_stats(self) -> dict:
        """取得統計資訊"""
        conn = self._get_connection()
        cursor = conn.cursor()

        stats = {}

        # 總數
        cursor.execute('SELECT COUNT(*) FROM items')
        stats['total'] = cursor.fetchone()[0]

        # 分類統計
        cursor.execute('SELECT category, COUNT(*) FROM items GROUP BY category ORDER BY COUNT(*) DESC')
        stats['by_category'] = dict(cursor.fetchall())

        # 最近更新
        cursor.execute('SELECT MAX(scraped_at) FROM items')
        stats['last_scraped'] = cursor.fetchone()[0]

        conn.close()
        return stats

    def delete(self, item_id: str) -> bool:
        """刪除資料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted


# =====================================
# 資料管理器
# =====================================

class DataManager:
    """資料管理器 - 整合所有功能"""

    def __init__(self, base_dir: str = "scraped_data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

        # 初始化各種儲存後端
        self.json_storage = JsonStorage(self.base_dir / "data.json")
        self.jsonl_storage = JsonLinesStorage(self.base_dir / "data.jsonl")
        self.csv_storage = CsvStorage(self.base_dir / "data.csv")
        self.sqlite_storage = SQLiteStorage(str(self.base_dir / "data.db"))

        self.cleaner = DataCleaner()
        self.items: list[ScrapedItem] = []

    def add_item(self, item: ScrapedItem, clean: bool = True) -> bool:
        """新增資料項目"""
        if clean:
            item = self.cleaner.clean_item(item)

        is_valid, errors = self.cleaner.validate_item(item)
        if not is_valid:
            print(f"驗證失敗: {errors}")
            return False

        self.items.append(item)
        return True

    def add_items(self, items: list[ScrapedItem], clean: bool = True) -> int:
        """批量新增"""
        count = 0
        for item in items:
            if self.add_item(item, clean):
                count += 1
        return count

    def remove_duplicates(self) -> int:
        """移除重複項目"""
        seen = set()
        unique_items = []

        for item in self.items:
            if item.id not in seen:
                seen.add(item.id)
                unique_items.append(item)

        removed = len(self.items) - len(unique_items)
        self.items = unique_items
        return removed

    def save_all(self) -> dict:
        """儲存到所有格式"""
        results = {}

        print("正在儲存資料...")
        results['json'] = self.json_storage.save(self.items)
        print(f"  ✓ JSON: {results['json']} 筆")

        results['jsonl'] = self.jsonl_storage.save(self.items)
        print(f"  ✓ JSONL: {results['jsonl']} 筆")

        results['csv'] = self.csv_storage.save(self.items)
        print(f"  ✓ CSV: {results['csv']} 筆")

        results['sqlite'] = self.sqlite_storage.save(self.items)
        print(f"  ✓ SQLite: {results['sqlite']} 筆")

        return results

    def load_from(self, format: str = 'sqlite') -> int:
        """從指定格式載入"""
        if format == 'json':
            self.items = self.json_storage.load()
        elif format == 'jsonl':
            self.items = self.jsonl_storage.load()
        elif format == 'csv':
            self.items = self.csv_storage.load()
        elif format == 'sqlite':
            self.items = self.sqlite_storage.load()
        else:
            raise ValueError(f"不支援的格式: {format}")

        return len(self.items)

    def export_to(self, format: str, filepath: str = None) -> str:
        """匯出到指定格式"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.base_dir / f"export_{timestamp}.{format}"

        if format == 'json':
            JsonStorage(filepath).save(self.items)
        elif format == 'csv':
            CsvStorage(filepath).save(self.items)
        elif format == 'jsonl':
            JsonLinesStorage(filepath).save(self.items)
        else:
            raise ValueError(f"不支援的格式: {format}")

        return str(filepath)

    def backup(self, backup_dir: str = None) -> str:
        """備份資料"""
        if not backup_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.base_dir / f"backup_{timestamp}"

        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # 複製所有資料檔案
        for file in self.base_dir.glob("data.*"):
            shutil.copy2(file, backup_path / file.name)

        print(f"✓ 已備份到: {backup_path}")
        return str(backup_path)

    def get_statistics(self) -> dict:
        """取得統計資訊"""
        stats = {
            'total_items': len(self.items),
            'categories': {},
            'tags': {},
        }

        for item in self.items:
            # 分類統計
            cat = item.category or 'Unknown'
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1

            # 標籤統計
            for tag in item.tags:
                stats['tags'][tag] = stats['tags'].get(tag, 0) + 1

        # 排序
        stats['categories'] = dict(sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True))
        stats['tags'] = dict(sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)[:20])

        return stats

    def display_summary(self):
        """顯示摘要"""
        stats = self.get_statistics()

        print("\n" + "=" * 60)
        print("📊 資料摘要")
        print("=" * 60)

        print(f"\n總資料數: {stats['total_items']}")

        print("\n📁 分類統計:")
        for cat, count in list(stats['categories'].items())[:10]:
            print(f"  {cat}: {count}")

        print("\n🏷️ 熱門標籤:")
        for tag, count in list(stats['tags'].items())[:10]:
            print(f"  #{tag}: {count}")


def demo():
    """示範程式"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 資料管理器 - Data Manager                      ║
║              多格式資料儲存與處理示範                           ║
╚══════════════════════════════════════════════════════════════╝
    """)

    manager = DataManager("demo_data")

    # 建立範例資料
    sample_data = [
        ScrapedItem(
            title="Python 網頁爬蟲入門",
            url="https://example.com/python-scraping",
            content="學習使用 Python 進行網頁爬蟲的基礎教學...",
            category="教學",
            tags=["python", "爬蟲", "入門"]
        ),
        ScrapedItem(
            title="BeautifulSoup 完整指南",
            url="https://example.com/beautifulsoup-guide",
            content="BeautifulSoup 是一個強大的 HTML 解析庫...",
            category="教學",
            tags=["python", "beautifulsoup", "解析"]
        ),
        ScrapedItem(
            title="Scrapy 框架教學",
            url="https://example.com/scrapy-tutorial",
            content="Scrapy 是 Python 最強大的爬蟲框架...",
            category="框架",
            tags=["python", "scrapy", "框架"]
        ),
        ScrapedItem(
            title="反爬蟲對策",
            url="https://example.com/anti-scraping",
            content="如何處理網站的反爬蟲機制...",
            category="進階",
            tags=["爬蟲", "反爬蟲", "進階"]
        ),
        ScrapedItem(
            title="資料清理技巧",
            url="https://example.com/data-cleaning",
            content="爬取資料後的清理和處理技巧...",
            category="資料處理",
            tags=["資料", "清理", "pandas"]
        ),
    ]

    print("📝 新增範例資料...")
    count = manager.add_items(sample_data)
    print(f"  ✓ 新增 {count} 筆資料")

    # 移除重複
    removed = manager.remove_duplicates()
    print(f"  ✓ 移除 {removed} 筆重複資料")

    # 顯示摘要
    manager.display_summary()

    # 儲存到所有格式
    print("\n" + "=" * 60)
    manager.save_all()

    # 搜尋示範
    print("\n" + "=" * 60)
    print("🔍 搜尋示範")
    print("=" * 60)

    results = manager.sqlite_storage.search("python")
    print(f"\n搜尋 'python' 找到 {len(results)} 筆結果:")
    for item in results[:5]:
        print(f"  • {item.title}")

    # 備份
    print("\n" + "=" * 60)
    backup_path = manager.backup()

    print("\n" + "=" * 60)
    print("✅ 示範完成!")
    print(f"資料目錄: {manager.base_dir}")


if __name__ == "__main__":
    demo()
