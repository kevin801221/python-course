"""
新聞聚合爬蟲 - News Aggregator Scraper
=====================================
這是一個使用 Requests 庫的完整新聞爬蟲應用程式，展示 HTTP 請求的各種技巧。

功能：
1. 從多個新聞來源擷取最新新聞
2. 處理 Session 和 Cookies
3. 自動重試機制
4. 請求頻率控制
5. 匯出為多種格式

使用方法：
    python news_scraper.py
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import Optional, Generator
import json
import csv
import time
import random
from datetime import datetime
from abc import ABC, abstractmethod


@dataclass
class NewsArticle:
    """新聞文章資料結構"""
    title: str
    url: str
    source: str
    summary: str = ""
    author: str = ""
    published_date: str = ""
    category: str = ""
    image_url: str = ""
    scraped_at: str = ""


class BaseNewsScraper(ABC):
    """新聞爬蟲基礎類別"""

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """創建帶有重試機制的 Session"""
        session = requests.Session()

        # 設定重試策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # 設定預設標頭
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        return session

    def _polite_request(self, url: str, min_delay: float = 0.5, max_delay: float = 2.0) -> Optional[requests.Response]:
        """禮貌的請求（帶有隨機延遲）"""
        time.sleep(random.uniform(min_delay, max_delay))

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"  ⚠️ 請求失敗: {url} - {e}")
            return None

    @abstractmethod
    def scrape(self) -> Generator[NewsArticle, None, None]:
        """擷取新聞（子類別必須實作）"""
        pass


class HackerNewsScraper(BaseNewsScraper):
    """Hacker News 爬蟲"""

    def __init__(self):
        super().__init__("Hacker News", "https://news.ycombinator.com")

    def scrape(self, pages: int = 2) -> Generator[NewsArticle, None, None]:
        """擷取 Hacker News 文章"""
        print(f"\n📰 正在擷取 {self.name}...")

        for page in range(1, pages + 1):
            url = f"{self.base_url}/news?p={page}" if page > 1 else self.base_url

            response = self._polite_request(url)
            if not response:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到所有文章
            for item in soup.select('tr.athing'):
                try:
                    title_cell = item.select_one('td.title > span.titleline > a')
                    if not title_cell:
                        continue

                    title = title_cell.text.strip()
                    link = title_cell.get('href', '')

                    # 處理相對連結
                    if link.startswith('item?'):
                        link = f"{self.base_url}/{link}"

                    # 取得副標題資訊（分數、作者等）
                    subtext = item.find_next_sibling('tr')
                    score = ""
                    author = ""
                    age = ""

                    if subtext:
                        score_elem = subtext.select_one('span.score')
                        author_elem = subtext.select_one('a.hnuser')
                        age_elem = subtext.select_one('span.age')

                        if score_elem:
                            score = score_elem.text
                        if author_elem:
                            author = author_elem.text
                        if age_elem:
                            age = age_elem.text

                    yield NewsArticle(
                        title=title,
                        url=link,
                        source=self.name,
                        summary=f"Score: {score}" if score else "",
                        author=author,
                        published_date=age,
                        category="Tech",
                        scraped_at=datetime.now().isoformat()
                    )

                except Exception as e:
                    print(f"  ⚠️ 解析錯誤: {e}")
                    continue

            print(f"  ✓ 完成第 {page} 頁")


class PythonOrgNewsScraper(BaseNewsScraper):
    """Python.org 新聞爬蟲"""

    def __init__(self):
        super().__init__("Python.org", "https://www.python.org")

    def scrape(self) -> Generator[NewsArticle, None, None]:
        """擷取 Python.org 最新消息"""
        print(f"\n📰 正在擷取 {self.name}...")

        url = f"{self.base_url}/blogs/"
        response = self._polite_request(url)

        if not response:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到新聞列表
        for article in soup.select('ul.list-recent-posts li'):
            try:
                link_elem = article.select_one('a')
                if not link_elem:
                    continue

                title = link_elem.text.strip()
                href = link_elem.get('href', '')
                full_url = f"{self.base_url}{href}" if href.startswith('/') else href

                # 取得日期
                date_elem = article.select_one('time')
                date = date_elem.get('datetime', '') if date_elem else ""

                yield NewsArticle(
                    title=title,
                    url=full_url,
                    source=self.name,
                    published_date=date,
                    category="Python",
                    scraped_at=datetime.now().isoformat()
                )

            except Exception as e:
                print(f"  ⚠️ 解析錯誤: {e}")
                continue

        print(f"  ✓ 完成擷取")


class GitHubTrendingScraper(BaseNewsScraper):
    """GitHub Trending 爬蟲"""

    def __init__(self):
        super().__init__("GitHub Trending", "https://github.com")

    def scrape(self, language: str = "python") -> Generator[NewsArticle, None, None]:
        """擷取 GitHub 趨勢專案"""
        print(f"\n📰 正在擷取 {self.name} ({language})...")

        url = f"{self.base_url}/trending/{language}?since=daily"
        response = self._polite_request(url)

        if not response:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        for repo in soup.select('article.Box-row'):
            try:
                # 專案名稱和連結
                name_elem = repo.select_one('h2 a')
                if not name_elem:
                    continue

                repo_path = name_elem.get('href', '').strip()
                full_url = f"{self.base_url}{repo_path}"
                name = repo_path.strip('/')

                # 描述
                desc_elem = repo.select_one('p')
                description = desc_elem.text.strip() if desc_elem else ""

                # 語言
                lang_elem = repo.select_one('[itemprop="programmingLanguage"]')
                lang = lang_elem.text.strip() if lang_elem else language

                # 星星數
                stars_elem = repo.select('a.Link--muted')
                stars = ""
                for elem in stars_elem:
                    if 'stargazers' in elem.get('href', ''):
                        stars = elem.text.strip()
                        break

                yield NewsArticle(
                    title=name,
                    url=full_url,
                    source=self.name,
                    summary=description,
                    category=lang,
                    published_date=f"⭐ {stars}" if stars else "",
                    scraped_at=datetime.now().isoformat()
                )

            except Exception as e:
                print(f"  ⚠️ 解析錯誤: {e}")
                continue

        print(f"  ✓ 完成擷取")


class NewsAggregator:
    """新聞聚合器"""

    def __init__(self):
        self.scrapers = [
            HackerNewsScraper(),
            PythonOrgNewsScraper(),
            GitHubTrendingScraper(),
        ]
        self.articles: list[NewsArticle] = []

    def scrape_all(self):
        """從所有來源擷取新聞"""
        print("\n" + "=" * 60)
        print("🚀 開始擷取新聞")
        print("=" * 60)

        for scraper in self.scrapers:
            try:
                for article in scraper.scrape():
                    self.articles.append(article)
            except Exception as e:
                print(f"❌ 爬蟲 {scraper.name} 發生錯誤: {e}")

        print(f"\n✅ 總共擷取 {len(self.articles)} 篇文章")

    def get_by_source(self, source: str) -> list[NewsArticle]:
        """依來源篩選"""
        return [a for a in self.articles if a.source.lower() == source.lower()]

    def get_by_category(self, category: str) -> list[NewsArticle]:
        """依分類篩選"""
        return [a for a in self.articles if a.category.lower() == category.lower()]

    def display_summary(self):
        """顯示摘要"""
        print("\n" + "=" * 60)
        print("📊 擷取摘要")
        print("=" * 60)

        # 依來源統計
        sources = {}
        for article in self.articles:
            sources[article.source] = sources.get(article.source, 0) + 1

        for source, count in sources.items():
            print(f"  {source}: {count} 篇")

        # 顯示前 10 篇
        print("\n📰 最新文章 (前 10 篇)")
        print("-" * 60)

        for i, article in enumerate(self.articles[:10], 1):
            print(f"\n{i}. [{article.source}] {article.title[:50]}...")
            print(f"   🔗 {article.url[:60]}...")
            if article.summary:
                print(f"   📝 {article.summary[:50]}...")

    def export_json(self, filename: str = "news_data.json"):
        """匯出為 JSON"""
        data = [asdict(a) for a in self.articles]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已匯出到: {filename}")

    def export_csv(self, filename: str = "news_data.csv"):
        """匯出為 CSV"""
        if not self.articles:
            print("⚠️ 沒有資料可匯出")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(asdict(self.articles[0]).keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for article in self.articles:
                writer.writerow(asdict(article))

        print(f"✅ 已匯出到: {filename}")

    def export_markdown(self, filename: str = "news_report.md"):
        """匯出為 Markdown 報告"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 新聞聚合報告\n\n")
            f.write(f"> 產生時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"總共 {len(self.articles)} 篇文章\n\n")

            # 依來源分組
            current_source = ""
            for article in self.articles:
                if article.source != current_source:
                    current_source = article.source
                    f.write(f"\n## {current_source}\n\n")

                f.write(f"### {article.title}\n\n")
                f.write(f"- 🔗 連結: [{article.url}]({article.url})\n")
                if article.summary:
                    f.write(f"- 📝 摘要: {article.summary}\n")
                if article.author:
                    f.write(f"- 👤 作者: {article.author}\n")
                if article.published_date:
                    f.write(f"- 📅 日期: {article.published_date}\n")
                f.write("\n")

        print(f"✅ 已匯出到: {filename}")


def main():
    """主程式"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    新聞聚合爬蟲                                ║
║              News Aggregator Scraper                         ║
╚══════════════════════════════════════════════════════════════╝
    """)

    aggregator = NewsAggregator()

    # 執行擷取
    aggregator.scrape_all()

    # 顯示摘要
    aggregator.display_summary()

    # 匯出選項
    print("\n" + "=" * 60)
    print("📤 匯出選項")
    print("=" * 60)
    print("1. 匯出 JSON")
    print("2. 匯出 CSV")
    print("3. 匯出 Markdown 報告")
    print("4. 全部匯出")
    print("5. 跳過匯出")

    choice = input("\n請選擇 (1-5): ").strip()

    if choice == '1':
        aggregator.export_json()
    elif choice == '2':
        aggregator.export_csv()
    elif choice == '3':
        aggregator.export_markdown()
    elif choice == '4':
        aggregator.export_json()
        aggregator.export_csv()
        aggregator.export_markdown()
    else:
        print("跳過匯出")

    print("\n🎉 完成!")


if __name__ == "__main__":
    main()
