"""
動態網頁爬蟲 - Quotes to Scrape (JavaScript版)
==============================================
這是一個使用 Selenium 的完整動態網頁爬蟲應用程式。
使用 http://quotes.toscrape.com/js/ 作為練習網站（JavaScript 渲染版本）。

功能：
1. 處理 JavaScript 渲染的頁面
2. 模擬使用者行為（點擊、滾動）
3. 處理無限滾動頁面
4. 自動登入示範
5. 截圖功能

使用方法：
    python quotes_scraper.py

需要安裝：
    uv pip install selenium webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dataclasses import dataclass, asdict
from typing import Optional
import json
import csv
import time
import random
from datetime import datetime


@dataclass
class Quote:
    """名言資料結構"""
    text: str
    author: str
    author_url: str
    tags: list
    scraped_at: str = ""


@dataclass
class Author:
    """作者資料結構"""
    name: str
    born_date: str
    born_location: str
    description: str
    url: str


class DynamicQuotesScraper:
    """動態名言網站爬蟲"""

    BASE_URL = "http://quotes.toscrape.com"
    JS_URL = "http://quotes.toscrape.com/js/"
    SCROLL_URL = "http://quotes.toscrape.com/scroll"

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.quotes: list[Quote] = []
        self.authors: dict[str, Author] = {}

    def _setup_driver(self):
        """設定並啟動 Chrome 瀏覽器"""
        options = Options()

        if self.headless:
            options.add_argument('--headless=new')

        # 基本設定
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # 模擬真實瀏覽器
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # 停用圖片以加速（可選）
        # prefs = {'profile.managed_default_content_settings.images': 2}
        # options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(options=options)

        # 設定隱式等待
        self.driver.implicitly_wait(10)

        # 隱藏 webdriver 標誌
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

    def _random_sleep(self, min_sec: float = 0.5, max_sec: float = 2.0):
        """隨機延遲，模擬人類行為"""
        time.sleep(random.uniform(min_sec, max_sec))

    def _scroll_to_bottom(self):
        """滾動到頁面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._random_sleep(1, 2)

    def _scroll_to_element(self, element):
        """滾動到特定元素"""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)
        self._random_sleep(0.5, 1)

    def scrape_js_page(self, pages: int = 3) -> list[Quote]:
        """爬取 JavaScript 渲染的頁面"""
        print("\n" + "=" * 60)
        print("🚀 開始爬取 JavaScript 渲染頁面")
        print("=" * 60)

        try:
            self._setup_driver()

            for page in range(1, pages + 1):
                url = f"{self.JS_URL}page/{page}/" if page > 1 else self.JS_URL
                print(f"\n📄 正在處理第 {page} 頁: {url}")

                self.driver.get(url)

                # 等待名言載入
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
                    )
                except TimeoutException:
                    print(f"  ⚠️ 第 {page} 頁載入超時")
                    continue

                # 模擬滾動
                self._scroll_to_bottom()

                # 擷取名言
                quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")
                print(f"  找到 {len(quote_elements)} 條名言")

                for elem in quote_elements:
                    try:
                        text_elem = elem.find_element(By.CLASS_NAME, "text")
                        author_elem = elem.find_element(By.CLASS_NAME, "author")
                        author_link = elem.find_element(By.CSS_SELECTOR, "a[href*='author']")
                        tag_elems = elem.find_elements(By.CLASS_NAME, "tag")

                        quote = Quote(
                            text=text_elem.text.strip('""'),
                            author=author_elem.text,
                            author_url=author_link.get_attribute('href'),
                            tags=[t.text for t in tag_elems],
                            scraped_at=datetime.now().isoformat()
                        )
                        self.quotes.append(quote)

                    except NoSuchElementException as e:
                        print(f"  ⚠️ 解析名言失敗: {e}")
                        continue

                print(f"  ✓ 已擷取 {len(self.quotes)} 條名言")

                # 截圖
                screenshot_path = f"page_{page}_screenshot.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"  📸 已儲存截圖: {screenshot_path}")

        finally:
            if self.driver:
                self.driver.quit()

        return self.quotes

    def scrape_infinite_scroll(self, max_scrolls: int = 5) -> list[Quote]:
        """爬取無限滾動頁面"""
        print("\n" + "=" * 60)
        print("🚀 開始爬取無限滾動頁面")
        print("=" * 60)

        try:
            self._setup_driver()
            self.driver.get(self.SCROLL_URL)

            # 等待初始內容載入
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quote"))
            )

            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_count = 0

            while scroll_count < max_scrolls:
                print(f"\n🔄 第 {scroll_count + 1} 次滾動...")

                # 滾動到底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self._random_sleep(2, 3)

                # 檢查是否有新內容載入
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    print("  已到達頁面底部")
                    break

                last_height = new_height
                scroll_count += 1

                # 擷取當前頁面的名言
                current_quotes = len(self.driver.find_elements(By.CLASS_NAME, "quote"))
                print(f"  目前載入 {current_quotes} 條名言")

            # 擷取所有名言
            print("\n📝 正在擷取所有名言...")
            quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")

            for elem in quote_elements:
                try:
                    text_elem = elem.find_element(By.CLASS_NAME, "text")
                    author_elem = elem.find_element(By.CLASS_NAME, "author")
                    tag_elems = elem.find_elements(By.CLASS_NAME, "tag")

                    quote = Quote(
                        text=text_elem.text.strip('""'),
                        author=author_elem.text,
                        author_url="",
                        tags=[t.text for t in tag_elems],
                        scraped_at=datetime.now().isoformat()
                    )
                    self.quotes.append(quote)

                except NoSuchElementException:
                    continue

            print(f"✅ 共擷取 {len(self.quotes)} 條名言")

        finally:
            if self.driver:
                self.driver.quit()

        return self.quotes

    def demo_login(self):
        """示範自動登入功能"""
        print("\n" + "=" * 60)
        print("🔐 示範自動登入功能")
        print("=" * 60)

        try:
            self._setup_driver()

            # 前往登入頁面
            login_url = f"{self.BASE_URL}/login"
            print(f"\n正在前往登入頁面: {login_url}")
            self.driver.get(login_url)

            self._random_sleep(1, 2)

            # 找到輸入框
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

            # 模擬人類輸入（逐字輸入）
            print("正在輸入帳號...")
            for char in "testuser":
                username_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))

            self._random_sleep(0.5, 1)

            print("正在輸入密碼...")
            for char in "testpass":
                password_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))

            self._random_sleep(0.5, 1)

            # 截圖（登入前）
            self.driver.save_screenshot("login_before.png")
            print("📸 已儲存登入前截圖: login_before.png")

            # 點擊登入按鈕
            print("正在點擊登入按鈕...")
            submit_button.click()

            self._random_sleep(2, 3)

            # 檢查是否登入成功
            try:
                logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
                print("✅ 登入成功!")

                # 截圖（登入後）
                self.driver.save_screenshot("login_after.png")
                print("📸 已儲存登入後截圖: login_after.png")

            except NoSuchElementException:
                print("❌ 登入失敗")

                # 檢查錯誤訊息
                try:
                    error = self.driver.find_element(By.CLASS_NAME, "error")
                    print(f"錯誤訊息: {error.text}")
                except NoSuchElementException:
                    pass

        finally:
            if self.driver:
                self.driver.quit()

    def scrape_author_details(self, author_url: str) -> Optional[Author]:
        """爬取作者詳細資訊"""
        try:
            self.driver.get(author_url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "author-details"))
            )

            name = self.driver.find_element(By.CLASS_NAME, "author-title").text
            born_date = self.driver.find_element(By.CLASS_NAME, "author-born-date").text
            born_location = self.driver.find_element(By.CLASS_NAME, "author-born-location").text
            description = self.driver.find_element(By.CLASS_NAME, "author-description").text

            return Author(
                name=name,
                born_date=born_date,
                born_location=born_location.replace('in ', ''),
                description=description[:500],
                url=author_url
            )

        except Exception as e:
            print(f"  ⚠️ 擷取作者資訊失敗: {e}")
            return None

    def analyze(self):
        """分析爬取的資料"""
        if not self.quotes:
            print("❌ 沒有資料可分析")
            return

        print("\n" + "=" * 60)
        print("📊 資料分析")
        print("=" * 60)

        # 作者統計
        from collections import Counter
        author_counts = Counter(q.author for q in self.quotes)

        print(f"\n📈 基本統計:")
        print(f"  總名言數量: {len(self.quotes)}")
        print(f"  不同作者數: {len(author_counts)}")

        print(f"\n👤 最多名言的作者:")
        for author, count in author_counts.most_common(5):
            print(f"  {author}: {count} 條")

        # 標籤統計
        all_tags = []
        for q in self.quotes:
            all_tags.extend(q.tags)
        tag_counts = Counter(all_tags)

        print(f"\n🏷️ 最熱門的標籤:")
        for tag, count in tag_counts.most_common(10):
            print(f"  #{tag}: {count} 次")

        # 名言長度分析
        lengths = [len(q.text) for q in self.quotes]
        print(f"\n📏 名言長度分析:")
        print(f"  最短: {min(lengths)} 字元")
        print(f"  最長: {max(lengths)} 字元")
        print(f"  平均: {sum(lengths)//len(lengths)} 字元")

    def export_json(self, filename: str = "quotes_data.json"):
        """匯出為 JSON"""
        data = {
            'quotes': [asdict(q) for q in self.quotes],
            'total': len(self.quotes),
            'exported_at': datetime.now().isoformat()
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已匯出到: {filename}")

    def export_csv(self, filename: str = "quotes_data.csv"):
        """匯出為 CSV"""
        if not self.quotes:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['text', 'author', 'author_url', 'tags', 'scraped_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for quote in self.quotes:
                row = asdict(quote)
                row['tags'] = ', '.join(row['tags'])
                writer.writerow(row)

        print(f"✅ 已匯出到: {filename}")


def main():
    """主程式"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           動態網頁爬蟲 - Quotes to Scrape                     ║
║              Selenium 完整應用範例                            ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # 選擇模式
    print("請選擇爬取模式:")
    print("1. 爬取 JavaScript 渲染頁面")
    print("2. 爬取無限滾動頁面")
    print("3. 示範自動登入")
    print("4. 完整測試（全部執行）")

    choice = input("\n請選擇 (1-4): ").strip()

    # 是否使用無頭模式
    headless_input = input("使用無頭模式? (y/n, 預設 y): ").strip().lower()
    headless = headless_input != 'n'

    scraper = DynamicQuotesScraper(headless=headless)

    if choice == '1':
        pages = input("要爬取幾頁? (預設 3): ").strip()
        pages = int(pages) if pages.isdigit() else 3
        scraper.scrape_js_page(pages=pages)

    elif choice == '2':
        scrolls = input("最多滾動幾次? (預設 5): ").strip()
        scrolls = int(scrolls) if scrolls.isdigit() else 5
        scraper.scrape_infinite_scroll(max_scrolls=scrolls)

    elif choice == '3':
        scraper.demo_login()
        return  # 登入示範不需要匯出

    elif choice == '4':
        print("\n--- JavaScript 渲染頁面 ---")
        scraper.scrape_js_page(pages=2)

        print("\n--- 無限滾動頁面 ---")
        scraper.scrape_infinite_scroll(max_scrolls=3)

    else:
        print("無效選擇")
        return

    # 分析與匯出
    if scraper.quotes:
        scraper.analyze()

        print("\n" + "=" * 60)
        export = input("是否匯出資料? (y/n): ").strip().lower()
        if export == 'y':
            scraper.export_json()
            scraper.export_csv()

    print("\n🎉 完成!")


if __name__ == "__main__":
    main()
