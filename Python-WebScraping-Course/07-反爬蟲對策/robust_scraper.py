"""
穩健爬蟲 - Robust Scraper
=========================
這是一個實現各種反反爬蟲技術的完整爬蟲應用程式。

功能：
1. 隨機 User-Agent 輪換
2. 請求頻率控制與指數退避
3. 代理輪換支援
4. Session 和 Cookie 管理
5. 自動重試機制
6. robots.txt 遵守檢查
7. 請求指紋隨機化
8. 詳細日誌記錄

使用方法：
    python robust_scraper.py

注意：本程式僅供學習用途，請遵守網站的服務條款和法律規定。
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional, Callable
import urllib.robotparser
from urllib.parse import urljoin, urlparse
import random
import time
import logging
import json
from datetime import datetime
from abc import ABC, abstractmethod


# =====================================
# 日誌設定
# =====================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('RobustScraper')


# =====================================
# User-Agent 管理器
# =====================================

class UserAgentManager:
    """User-Agent 管理器"""

    # 桌面瀏覽器
    DESKTOP_AGENTS = [
        # Chrome (Windows)
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # Chrome (Mac)
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    ]

    # 行動裝置瀏覽器
    MOBILE_AGENTS = [
        # iPhone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        # Android
        'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    ]

    def __init__(self, include_mobile: bool = False):
        self.agents = self.DESKTOP_AGENTS.copy()
        if include_mobile:
            self.agents.extend(self.MOBILE_AGENTS)
        self.current_index = 0

    def random(self) -> str:
        """隨機選擇一個 User-Agent"""
        return random.choice(self.agents)

    def next(self) -> str:
        """按順序輪換 User-Agent"""
        agent = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.agents)
        return agent


# =====================================
# 代理管理器
# =====================================

class ProxyManager:
    """代理管理器"""

    def __init__(self, proxies: list[str] = None):
        self.proxies = proxies or []
        self.failed_proxies = set()

    def add_proxy(self, proxy: str):
        """新增代理"""
        self.proxies.append(proxy)

    def get_proxy(self) -> Optional[dict]:
        """取得可用代理"""
        available = [p for p in self.proxies if p not in self.failed_proxies]
        if not available:
            return None

        proxy = random.choice(available)
        return {
            'http': proxy,
            'https': proxy
        }

    def mark_failed(self, proxy: str):
        """標記代理為失敗"""
        self.failed_proxies.add(proxy)
        logger.warning(f"代理失敗: {proxy}")

    def reset_failed(self):
        """重置失敗列表"""
        self.failed_proxies.clear()


# =====================================
# 請求指紋隨機化
# =====================================

class RequestFingerprint:
    """請求指紋生成器 - 模擬真實瀏覽器請求"""

    ACCEPT_HEADERS = [
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    ]

    ACCEPT_LANGUAGES = [
        'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'zh-TW,zh;q=0.9,en;q=0.8',
        'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'en-US,en;q=0.9',
    ]

    ACCEPT_ENCODINGS = [
        'gzip, deflate, br',
        'gzip, deflate',
    ]

    @classmethod
    def generate(cls, user_agent: str) -> dict:
        """生成隨機請求標頭"""
        headers = {
            'User-Agent': user_agent,
            'Accept': random.choice(cls.ACCEPT_HEADERS),
            'Accept-Language': random.choice(cls.ACCEPT_LANGUAGES),
            'Accept-Encoding': random.choice(cls.ACCEPT_ENCODINGS),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # 隨機加入其他標頭
        if random.random() > 0.5:
            headers['Cache-Control'] = 'max-age=0'

        if random.random() > 0.5:
            headers['Sec-Fetch-Dest'] = 'document'
            headers['Sec-Fetch-Mode'] = 'navigate'
            headers['Sec-Fetch-Site'] = random.choice(['none', 'same-origin', 'same-site'])
            headers['Sec-Fetch-User'] = '?1'

        return headers


# =====================================
# Robots.txt 檢查器
# =====================================

class RobotsChecker:
    """Robots.txt 遵守檢查器"""

    def __init__(self):
        self.parsers = {}

    def can_fetch(self, url: str, user_agent: str = '*') -> bool:
        """檢查是否允許爬取"""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        if base_url not in self.parsers:
            rp = urllib.robotparser.RobotFileParser()
            robots_url = urljoin(base_url, '/robots.txt')
            rp.set_url(robots_url)

            try:
                rp.read()
                self.parsers[base_url] = rp
            except Exception as e:
                logger.warning(f"無法讀取 robots.txt: {e}")
                return True  # 預設允許

        return self.parsers[base_url].can_fetch(user_agent, url)

    def get_crawl_delay(self, url: str, user_agent: str = '*') -> Optional[float]:
        """取得建議的爬取延遲"""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        if base_url in self.parsers:
            return self.parsers[base_url].crawl_delay(user_agent)
        return None


# =====================================
# 速率限制器
# =====================================

class RateLimiter:
    """請求速率限制器"""

    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
        self.consecutive_errors = 0

    def wait(self):
        """等待適當的時間"""
        # 計算基礎延遲
        delay = random.uniform(self.min_delay, self.max_delay)

        # 指數退避（遇到錯誤時增加延遲）
        if self.consecutive_errors > 0:
            delay *= (2 ** min(self.consecutive_errors, 5))
            logger.info(f"指數退避: 等待 {delay:.2f} 秒")

        # 確保與上次請求有足夠間隔
        elapsed = time.time() - self.last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)

        self.last_request_time = time.time()

    def record_success(self):
        """記錄成功請求"""
        self.consecutive_errors = 0

    def record_error(self):
        """記錄錯誤請求"""
        self.consecutive_errors += 1


# =====================================
# 穩健爬蟲主類別
# =====================================

@dataclass
class ScrapedPage:
    """爬取結果"""
    url: str
    status_code: int
    content: str = ""
    soup: Optional[BeautifulSoup] = None
    headers: dict = field(default_factory=dict)
    elapsed_time: float = 0.0
    scraped_at: str = ""
    error: str = ""


class RobustScraper:
    """穩健爬蟲 - 實現各種反反爬蟲技術"""

    def __init__(
        self,
        min_delay: float = 1.0,
        max_delay: float = 3.0,
        max_retries: int = 3,
        timeout: int = 30,
        respect_robots: bool = True,
        proxies: list[str] = None
    ):
        # 基本設定
        self.max_retries = max_retries
        self.timeout = timeout
        self.respect_robots = respect_robots

        # 管理器
        self.ua_manager = UserAgentManager()
        self.proxy_manager = ProxyManager(proxies)
        self.robots_checker = RobotsChecker()
        self.rate_limiter = RateLimiter(min_delay, max_delay)

        # Session
        self.session = self._create_session()

        # 統計
        self.stats = {
            'requests': 0,
            'success': 0,
            'failed': 0,
            'retried': 0,
            'blocked': 0
        }

    def _create_session(self) -> requests.Session:
        """建立帶有重試機制的 Session"""
        session = requests.Session()

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _check_robots(self, url: str) -> bool:
        """檢查 robots.txt"""
        if not self.respect_robots:
            return True

        can_fetch = self.robots_checker.can_fetch(url)
        if not can_fetch:
            logger.warning(f"robots.txt 禁止爬取: {url}")
            self.stats['blocked'] += 1

        # 檢查建議延遲
        crawl_delay = self.robots_checker.get_crawl_delay(url)
        if crawl_delay:
            self.rate_limiter.min_delay = max(self.rate_limiter.min_delay, crawl_delay)
            logger.info(f"使用 robots.txt 建議延遲: {crawl_delay}s")

        return can_fetch

    def get(self, url: str, **kwargs) -> ScrapedPage:
        """發送 GET 請求"""
        self.stats['requests'] += 1

        # 檢查 robots.txt
        if not self._check_robots(url):
            return ScrapedPage(
                url=url,
                status_code=0,
                error="robots.txt 禁止爬取",
                scraped_at=datetime.now().isoformat()
            )

        # 速率限制
        self.rate_limiter.wait()

        # 生成請求標頭
        user_agent = self.ua_manager.random()
        headers = RequestFingerprint.generate(user_agent)
        headers.update(kwargs.pop('headers', {}))

        # 取得代理
        proxies = self.proxy_manager.get_proxy()

        attempt = 0
        last_error = ""

        while attempt < self.max_retries:
            try:
                start_time = time.time()

                response = self.session.get(
                    url,
                    headers=headers,
                    proxies=proxies,
                    timeout=self.timeout,
                    **kwargs
                )

                elapsed = time.time() - start_time

                # 檢查是否被封鎖
                if response.status_code == 403:
                    logger.warning(f"403 Forbidden - 可能被封鎖: {url}")
                    self.stats['blocked'] += 1

                if response.status_code == 429:
                    logger.warning(f"429 Too Many Requests - 請求過於頻繁")
                    self.rate_limiter.record_error()
                    attempt += 1
                    self.stats['retried'] += 1
                    continue

                if response.status_code == 200:
                    self.rate_limiter.record_success()
                    self.stats['success'] += 1

                    soup = BeautifulSoup(response.text, 'html.parser')

                    return ScrapedPage(
                        url=url,
                        status_code=response.status_code,
                        content=response.text,
                        soup=soup,
                        headers=dict(response.headers),
                        elapsed_time=elapsed,
                        scraped_at=datetime.now().isoformat()
                    )
                else:
                    logger.warning(f"HTTP {response.status_code}: {url}")
                    return ScrapedPage(
                        url=url,
                        status_code=response.status_code,
                        error=f"HTTP {response.status_code}",
                        scraped_at=datetime.now().isoformat()
                    )

            except requests.exceptions.ProxyError as e:
                if proxies:
                    self.proxy_manager.mark_failed(list(proxies.values())[0])
                    proxies = self.proxy_manager.get_proxy()
                last_error = str(e)
                attempt += 1
                self.stats['retried'] += 1

            except requests.exceptions.Timeout as e:
                logger.warning(f"請求超時: {url}")
                last_error = str(e)
                attempt += 1
                self.rate_limiter.record_error()
                self.stats['retried'] += 1

            except requests.exceptions.RequestException as e:
                logger.error(f"請求錯誤: {url} - {e}")
                last_error = str(e)
                attempt += 1
                self.rate_limiter.record_error()
                self.stats['retried'] += 1

        # 所有重試都失敗
        self.stats['failed'] += 1
        return ScrapedPage(
            url=url,
            status_code=0,
            error=f"達到最大重試次數: {last_error}",
            scraped_at=datetime.now().isoformat()
        )

    def scrape_multiple(
        self,
        urls: list[str],
        callback: Callable[[ScrapedPage], None] = None
    ) -> list[ScrapedPage]:
        """批量爬取多個 URL"""
        results = []

        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] 正在爬取: {url}")

            page = self.get(url)
            results.append(page)

            if callback:
                callback(page)

            if page.status_code == 200:
                logger.info(f"  ✓ 成功 ({page.elapsed_time:.2f}s)")
            else:
                logger.warning(f"  ✗ 失敗: {page.error}")

        return results

    def get_stats(self) -> dict:
        """取得統計資訊"""
        return {
            **self.stats,
            'success_rate': f"{(self.stats['success'] / max(self.stats['requests'], 1) * 100):.1f}%"
        }

    def print_stats(self):
        """顯示統計資訊"""
        stats = self.get_stats()
        print("\n" + "=" * 50)
        print("📊 爬取統計")
        print("=" * 50)
        print(f"  總請求數: {stats['requests']}")
        print(f"  成功: {stats['success']}")
        print(f"  失敗: {stats['failed']}")
        print(f"  重試: {stats['retried']}")
        print(f"  被封鎖: {stats['blocked']}")
        print(f"  成功率: {stats['success_rate']}")


def demo():
    """示範程式"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  穩健爬蟲 - Robust Scraper                     ║
║                反反爬蟲技術完整實作                             ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # 建立爬蟲實例
    scraper = RobustScraper(
        min_delay=1.0,
        max_delay=2.0,
        max_retries=3,
        respect_robots=True
    )

    # 測試 URL 列表
    test_urls = [
        "http://quotes.toscrape.com/",
        "http://quotes.toscrape.com/page/2/",
        "http://books.toscrape.com/",
        "https://httpbin.org/html",
        "https://httpbin.org/headers",
    ]

    print("\n🚀 開始爬取測試...")
    print("=" * 50)

    results = []

    def on_page_scraped(page: ScrapedPage):
        """每頁爬取完成的回調"""
        if page.soup:
            title = page.soup.find('title')
            title_text = title.text.strip() if title else "無標題"
            print(f"  📄 {title_text[:40]}...")

    results = scraper.scrape_multiple(test_urls, callback=on_page_scraped)

    # 顯示統計
    scraper.print_stats()

    # 顯示詳細結果
    print("\n" + "=" * 50)
    print("📋 詳細結果")
    print("=" * 50)

    for page in results:
        status = "✓" if page.status_code == 200 else "✗"
        print(f"\n{status} {page.url}")
        print(f"  狀態碼: {page.status_code}")
        if page.elapsed_time:
            print(f"  耗時: {page.elapsed_time:.2f}s")
        if page.error:
            print(f"  錯誤: {page.error}")

    # 匯出結果
    print("\n" + "=" * 50)
    export = input("是否匯出結果? (y/n): ").strip().lower()

    if export == 'y':
        output_data = []
        for page in results:
            output_data.append({
                'url': page.url,
                'status_code': page.status_code,
                'elapsed_time': page.elapsed_time,
                'scraped_at': page.scraped_at,
                'error': page.error
            })

        with open('scrape_results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print("✅ 已匯出到: scrape_results.json")

    print("\n🎉 完成!")


if __name__ == "__main__":
    demo()
