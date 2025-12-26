"""
書籍商城爬蟲 - Books to Scrape
==============================
這是一個使用 BeautifulSoup 的完整電商爬蟲應用程式。
使用 http://books.toscrape.com 作為練習網站（專為爬蟲練習設計的網站）。

功能：
1. 爬取所有書籍分類
2. 擷取每本書的詳細資訊
3. 處理分頁
4. 資料清理與驗證
5. 價格分析與統計

使用方法：
    python book_scraper.py
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict, field
from typing import Optional, Generator
from urllib.parse import urljoin
import json
import csv
import re
import time
import random
from datetime import datetime
from collections import defaultdict


@dataclass
class Book:
    """書籍資料結構"""
    title: str
    price: float
    rating: int
    availability: str
    url: str
    category: str = ""
    description: str = ""
    upc: str = ""
    product_type: str = ""
    tax: float = 0.0
    num_reviews: int = 0
    image_url: str = ""
    scraped_at: str = ""


class BooksScraper:
    """Books to Scrape 爬蟲"""

    BASE_URL = "http://books.toscrape.com"

    # 評分對照表
    RATING_MAP = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }

    def __init__(self, delay_range: tuple = (0.3, 1.0)):
        self.delay_range = delay_range
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.books: list[Book] = []
        self.categories: dict[str, str] = {}

    def _request(self, url: str) -> Optional[BeautifulSoup]:
        """發送請求並返回 BeautifulSoup 物件"""
        time.sleep(random.uniform(*self.delay_range))

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"  ⚠️ 請求失敗: {url} - {e}")
            return None

    def _parse_price(self, price_text: str) -> float:
        """解析價格文字"""
        # 移除貨幣符號並轉換為浮點數
        match = re.search(r'[\d.]+', price_text)
        return float(match.group()) if match else 0.0

    def _parse_rating(self, rating_class: str) -> int:
        """解析評分"""
        for word, num in self.RATING_MAP.items():
            if word in rating_class.lower():
                return num
        return 0

    def get_categories(self) -> dict[str, str]:
        """取得所有書籍分類"""
        print("\n📚 正在擷取分類...")

        soup = self._request(self.BASE_URL)
        if not soup:
            return {}

        nav = soup.select_one('div.side_categories ul.nav-list > li > ul')
        if not nav:
            return {}

        for li in nav.select('li > a'):
            name = li.text.strip()
            href = li.get('href', '')
            full_url = urljoin(self.BASE_URL, href)
            self.categories[name] = full_url

        print(f"  ✓ 找到 {len(self.categories)} 個分類")
        return self.categories

    def scrape_book_list(self, url: str, category: str = "") -> Generator[str, None, None]:
        """擷取書籍列表頁面，返回書籍詳情頁 URL"""
        page = 1

        while url:
            print(f"  📄 正在處理第 {page} 頁...")
            soup = self._request(url)

            if not soup:
                break

            # 找到所有書籍連結
            for article in soup.select('article.product_pod'):
                book_link = article.select_one('h3 > a')
                if book_link:
                    href = book_link.get('href', '')
                    # 處理相對路徑
                    if href.startswith('../'):
                        href = href.replace('../', '')
                    full_url = urljoin(f"{self.BASE_URL}/catalogue/", href)
                    yield full_url

            # 檢查下一頁
            next_btn = soup.select_one('li.next > a')
            if next_btn:
                next_href = next_btn.get('href', '')
                url = urljoin(url, next_href)
                page += 1
            else:
                url = None

    def scrape_book_detail(self, url: str, category: str = "") -> Optional[Book]:
        """擷取單本書籍的詳細資訊"""
        soup = self._request(url)
        if not soup:
            return None

        try:
            # 標題
            title_elem = soup.select_one('div.product_main > h1')
            title = title_elem.text.strip() if title_elem else "Unknown"

            # 價格
            price_elem = soup.select_one('p.price_color')
            price = self._parse_price(price_elem.text) if price_elem else 0.0

            # 評分
            rating_elem = soup.select_one('p.star-rating')
            rating = 0
            if rating_elem:
                classes = rating_elem.get('class', [])
                for cls in classes:
                    if cls.lower() in self.RATING_MAP:
                        rating = self.RATING_MAP[cls.lower()]
                        break

            # 庫存狀態
            stock_elem = soup.select_one('p.instock')
            availability = stock_elem.text.strip() if stock_elem else "Unknown"
            # 提取數量
            stock_match = re.search(r'(\d+)', availability)
            availability = f"In stock ({stock_match.group(1)} available)" if stock_match else availability

            # 描述
            desc_elem = soup.select_one('article.product_page > p')
            description = desc_elem.text.strip() if desc_elem else ""

            # 圖片
            img_elem = soup.select_one('div.item.active > img')
            image_url = ""
            if img_elem:
                img_src = img_elem.get('src', '')
                image_url = urljoin(self.BASE_URL, img_src.replace('../', ''))

            # 產品資訊表格
            upc = ""
            product_type = ""
            tax = 0.0
            num_reviews = 0

            info_table = soup.select('table.table-striped tr')
            for row in info_table:
                th = row.select_one('th')
                td = row.select_one('td')
                if th and td:
                    key = th.text.strip().lower()
                    value = td.text.strip()

                    if 'upc' in key:
                        upc = value
                    elif 'product type' in key:
                        product_type = value
                    elif 'tax' in key:
                        tax = self._parse_price(value)
                    elif 'reviews' in key:
                        num_reviews = int(value) if value.isdigit() else 0

            # 如果沒有提供分類，嘗試從麵包屑獲取
            if not category:
                breadcrumb = soup.select('ul.breadcrumb li')
                if len(breadcrumb) >= 3:
                    category = breadcrumb[2].text.strip()

            return Book(
                title=title,
                price=price,
                rating=rating,
                availability=availability,
                url=url,
                category=category,
                description=description[:500] if description else "",  # 限制長度
                upc=upc,
                product_type=product_type,
                tax=tax,
                num_reviews=num_reviews,
                image_url=image_url,
                scraped_at=datetime.now().isoformat()
            )

        except Exception as e:
            print(f"  ⚠️ 解析書籍失敗: {url} - {e}")
            return None

    def scrape_all(self, max_books: int = 100):
        """爬取所有書籍（限制數量以避免過長時間）"""
        print("\n" + "=" * 60)
        print("🚀 開始爬取 Books to Scrape")
        print("=" * 60)

        # 先取得分類
        if not self.categories:
            self.get_categories()

        count = 0
        # 爬取首頁的書籍列表
        print("\n📚 正在爬取書籍...")

        for book_url in self.scrape_book_list(f"{self.BASE_URL}/catalogue/page-1.html"):
            if count >= max_books:
                print(f"\n⚠️ 已達到最大數量限制 ({max_books})")
                break

            book = self.scrape_book_detail(book_url)
            if book:
                self.books.append(book)
                count += 1
                print(f"  [{count}/{max_books}] {book.title[:40]}... - £{book.price}")

        print(f"\n✅ 共爬取 {len(self.books)} 本書籍")

    def scrape_category(self, category_name: str, max_books: int = 50):
        """爬取特定分類的書籍"""
        if not self.categories:
            self.get_categories()

        # 找到匹配的分類
        category_url = None
        for name, url in self.categories.items():
            if category_name.lower() in name.lower():
                category_url = url
                category_name = name
                break

        if not category_url:
            print(f"❌ 找不到分類: {category_name}")
            print(f"可用分類: {', '.join(self.categories.keys())}")
            return

        print(f"\n📚 正在爬取分類: {category_name}")

        count = 0
        for book_url in self.scrape_book_list(category_url, category_name):
            if count >= max_books:
                break

            book = self.scrape_book_detail(book_url, category_name)
            if book:
                self.books.append(book)
                count += 1
                print(f"  [{count}] {book.title[:40]}... - £{book.price}")

    def analyze(self):
        """分析爬取的資料"""
        if not self.books:
            print("❌ 沒有資料可分析")
            return

        print("\n" + "=" * 60)
        print("📊 資料分析")
        print("=" * 60)

        # 基本統計
        prices = [b.price for b in self.books]
        ratings = [b.rating for b in self.books if b.rating > 0]

        print(f"\n📈 基本統計:")
        print(f"  總書籍數量: {len(self.books)}")
        print(f"  價格範圍: £{min(prices):.2f} - £{max(prices):.2f}")
        print(f"  平均價格: £{sum(prices)/len(prices):.2f}")
        print(f"  平均評分: {sum(ratings)/len(ratings):.1f}/5" if ratings else "  評分: N/A")

        # 分類統計
        category_counts = defaultdict(int)
        category_prices = defaultdict(list)
        for book in self.books:
            category_counts[book.category] += 1
            category_prices[book.category].append(book.price)

        print(f"\n📁 分類統計:")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            avg_price = sum(category_prices[cat]) / len(category_prices[cat])
            print(f"  {cat}: {count} 本 (平均 £{avg_price:.2f})")

        # 評分分布
        rating_counts = defaultdict(int)
        for book in self.books:
            rating_counts[book.rating] += 1

        print(f"\n⭐ 評分分布:")
        for rating in range(5, 0, -1):
            count = rating_counts[rating]
            bar = "█" * (count // 2)
            print(f"  {rating}星: {bar} ({count})")

        # 最貴的書
        print(f"\n💰 最貴的 5 本書:")
        for book in sorted(self.books, key=lambda x: x.price, reverse=True)[:5]:
            print(f"  £{book.price:.2f} - {book.title[:40]}...")

        # 最便宜的書
        print(f"\n🏷️ 最便宜的 5 本書:")
        for book in sorted(self.books, key=lambda x: x.price)[:5]:
            print(f"  £{book.price:.2f} - {book.title[:40]}...")

    def export_json(self, filename: str = "books_data.json"):
        """匯出為 JSON"""
        data = [asdict(b) for b in self.books]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已匯出到: {filename}")

    def export_csv(self, filename: str = "books_data.csv"):
        """匯出為 CSV"""
        if not self.books:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(asdict(self.books[0]).keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.books:
                writer.writerow(asdict(book))

        print(f"✅ 已匯出到: {filename}")


def main():
    """主程式"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║            書籍商城爬蟲 - Books to Scrape                     ║
║           BeautifulSoup 完整應用範例                          ║
╚══════════════════════════════════════════════════════════════╝
    """)

    scraper = BooksScraper()

    # 顯示選項
    print("請選擇爬取模式:")
    print("1. 爬取所有書籍（前 50 本）")
    print("2. 爬取特定分類")
    print("3. 只顯示分類列表")

    choice = input("\n請選擇 (1-3): ").strip()

    if choice == '1':
        max_books = input("請輸入要爬取的數量 (預設 50): ").strip()
        max_books = int(max_books) if max_books.isdigit() else 50
        scraper.scrape_all(max_books=max_books)

    elif choice == '2':
        scraper.get_categories()
        print("\n可用分類:")
        for i, cat in enumerate(scraper.categories.keys(), 1):
            print(f"  {i}. {cat}")

        cat_input = input("\n請輸入分類名稱: ").strip()
        max_books = input("請輸入要爬取的數量 (預設 30): ").strip()
        max_books = int(max_books) if max_books.isdigit() else 30
        scraper.scrape_category(cat_input, max_books=max_books)

    elif choice == '3':
        scraper.get_categories()
        print("\n所有分類:")
        for cat in scraper.categories.keys():
            print(f"  • {cat}")
        return

    # 分析與匯出
    if scraper.books:
        scraper.analyze()

        print("\n" + "=" * 60)
        export = input("是否匯出資料? (y/n): ").strip().lower()
        if export == 'y':
            scraper.export_json()
            scraper.export_csv()

    print("\n🎉 完成!")


if __name__ == "__main__":
    main()
