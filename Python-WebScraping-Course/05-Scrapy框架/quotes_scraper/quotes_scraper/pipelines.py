"""
Scrapy Pipelines - 資料處理管線
===============================
處理爬取到的資料：清理、驗證、儲存
"""

import json
import sqlite3
import hashlib
import logging
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class CleanDataPipeline:
    """清理資料的管線"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 清理文字欄位
        for field in ['text', 'author', 'name', 'description']:
            value = adapter.get(field)
            if value and isinstance(value, str):
                # 移除多餘空白
                adapter[field] = ' '.join(value.split())

        # 確保 tags 是列表
        tags = adapter.get('tags')
        if tags and isinstance(tags, str):
            adapter['tags'] = [t.strip() for t in tags.split(',')]

        return item


class DuplicateFilterPipeline:
    """過濾重複資料的管線"""

    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 根據 text 和 author 生成唯一 ID
        text = adapter.get('text', '')
        author = adapter.get('author', '')

        if text and author:
            unique_id = hashlib.md5(f"{text}{author}".encode()).hexdigest()

            if unique_id in self.seen:
                raise DropItem(f"Duplicate item: {author}")

            self.seen.add(unique_id)

        return item


class JsonWriterPipeline:
    """寫入 JSON 檔案的管線"""

    def open_spider(self, spider):
        """爬蟲開始時執行"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file = open(f'quotes_{timestamp}.jsonl', 'w', encoding='utf-8')
        self.count = 0

    def close_spider(self, spider):
        """爬蟲結束時執行"""
        self.file.close()
        logger.info(f"JsonWriterPipeline: 已寫入 {self.count} 筆資料")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(dict(adapter), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.count += 1
        return item


class SQLitePipeline:
    """儲存到 SQLite 資料庫的管線"""

    def open_spider(self, spider):
        """爬蟲開始時建立資料庫連線"""
        self.connection = sqlite3.connect('quotes.db')
        self.cursor = self.connection.cursor()

        # 建立資料表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                author_url TEXT,
                tags TEXT,
                source_url TEXT,
                scraped_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(text, author)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                born_date TEXT,
                born_location TEXT,
                description TEXT,
                url TEXT,
                scraped_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.connection.commit()
        self.quote_count = 0
        self.author_count = 0

    def close_spider(self, spider):
        """爬蟲結束時關閉連線"""
        self.connection.close()
        logger.info(f"SQLitePipeline: 已儲存 {self.quote_count} 條名言, {self.author_count} 位作者")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 判斷是 Quote 還是 Author
        if 'text' in adapter:
            self._save_quote(adapter)
        elif 'born_date' in adapter:
            self._save_author(adapter)

        return item

    def _save_quote(self, adapter):
        """儲存名言"""
        try:
            tags = adapter.get('tags', [])
            if isinstance(tags, list):
                tags = ', '.join(tags)

            self.cursor.execute('''
                INSERT OR IGNORE INTO quotes
                (text, author, author_url, tags, source_url, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('text'),
                adapter.get('author'),
                adapter.get('author_url'),
                tags,
                adapter.get('source_url'),
                adapter.get('scraped_at')
            ))

            self.connection.commit()
            if self.cursor.rowcount > 0:
                self.quote_count += 1

        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}")

    def _save_author(self, adapter):
        """儲存作者"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO authors
                (name, born_date, born_location, description, url, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('name'),
                adapter.get('born_date'),
                adapter.get('born_location'),
                adapter.get('description'),
                adapter.get('url'),
                adapter.get('scraped_at')
            ))

            self.connection.commit()
            if self.cursor.rowcount > 0:
                self.author_count += 1

        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}")


class StatsPipeline:
    """統計管線"""

    def __init__(self):
        self.stats = {
            'quotes': 0,
            'authors': 0,
            'tags': set(),
        }

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'text' in adapter:
            self.stats['quotes'] += 1
            tags = adapter.get('tags', [])
            if isinstance(tags, list):
                self.stats['tags'].update(tags)

        elif 'born_date' in adapter:
            self.stats['authors'] += 1

        return item

    def close_spider(self, spider):
        """輸出統計資訊"""
        logger.info("=" * 50)
        logger.info("爬蟲統計:")
        logger.info(f"  名言數量: {self.stats['quotes']}")
        logger.info(f"  作者數量: {self.stats['authors']}")
        logger.info(f"  標籤種類: {len(self.stats['tags'])}")
        logger.info("=" * 50)
