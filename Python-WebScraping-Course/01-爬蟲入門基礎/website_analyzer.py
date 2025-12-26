"""
網站資訊分析器 - Website Analyzer
================================
這是一個完整的網站資訊擷取工具，可以分析網站的基本資訊、連結、圖片、Meta 標籤等。

功能：
1. 擷取網站基本資訊（標題、描述、關鍵字）
2. 分析所有連結（內部連結 vs 外部連結）
3. 擷取所有圖片資訊
4. 檢查網站技術棧
5. 輸出結構化報告

使用方法：
    python website_analyzer.py https://example.com
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field
from typing import Optional
import json
import sys
from datetime import datetime


@dataclass
class WebsiteInfo:
    """網站資訊資料結構"""
    url: str
    title: str = ""
    description: str = ""
    keywords: str = ""
    language: str = ""
    internal_links: list = field(default_factory=list)
    external_links: list = field(default_factory=list)
    images: list = field(default_factory=list)
    scripts: list = field(default_factory=list)
    stylesheets: list = field(default_factory=list)
    meta_tags: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    status_code: int = 0
    response_time: float = 0.0
    analyzed_at: str = ""


class WebsiteAnalyzer:
    """網站分析器類別"""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup: Optional[BeautifulSoup] = None
        self.response: Optional[requests.Response] = None
        self.info = WebsiteInfo(url=url)

        # 設定請求標頭，模擬真實瀏覽器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def fetch_page(self) -> bool:
        """擷取網頁內容"""
        try:
            start_time = datetime.now()
            self.response = requests.get(
                self.url,
                headers=self.headers,
                timeout=30,
                allow_redirects=True
            )
            end_time = datetime.now()

            self.info.response_time = (end_time - start_time).total_seconds()
            self.info.status_code = self.response.status_code
            self.info.headers = dict(self.response.headers)
            self.info.analyzed_at = datetime.now().isoformat()

            if self.response.status_code == 200:
                self.soup = BeautifulSoup(self.response.text, 'html.parser')
                return True
            else:
                print(f"警告: HTTP 狀態碼 {self.response.status_code}")
                return False

        except requests.RequestException as e:
            print(f"錯誤: 無法連接到網站 - {e}")
            return False

    def extract_basic_info(self):
        """擷取基本資訊"""
        if not self.soup:
            return

        # 標題
        title_tag = self.soup.find('title')
        self.info.title = title_tag.text.strip() if title_tag else ""

        # 語言
        html_tag = self.soup.find('html')
        if html_tag and html_tag.get('lang'):
            self.info.language = html_tag.get('lang')

        # Meta 標籤
        for meta in self.soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')

            if name and content:
                self.info.meta_tags[name] = content

                if name.lower() == 'description':
                    self.info.description = content
                elif name.lower() == 'keywords':
                    self.info.keywords = content

    def extract_links(self):
        """擷取所有連結"""
        if not self.soup:
            return

        for a_tag in self.soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            text = a_tag.text.strip()

            # 跳過空連結和錨點
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            # 轉換相對路徑為絕對路徑
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)

            link_info = {
                'url': full_url,
                'text': text[:100] if text else '',  # 限制長度
                'is_https': parsed.scheme == 'https'
            }

            # 判斷內部或外部連結
            if parsed.netloc == self.domain or not parsed.netloc:
                self.info.internal_links.append(link_info)
            else:
                self.info.external_links.append(link_info)

    def extract_images(self):
        """擷取所有圖片"""
        if not self.soup:
            return

        for img in self.soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                continue

            full_url = urljoin(self.url, src)

            image_info = {
                'url': full_url,
                'alt': img.get('alt', ''),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
            }
            self.info.images.append(image_info)

    def extract_resources(self):
        """擷取 JS 和 CSS 資源"""
        if not self.soup:
            return

        # JavaScript
        for script in self.soup.find_all('script', src=True):
            src = script.get('src', '')
            full_url = urljoin(self.url, src)
            self.info.scripts.append(full_url)

        # CSS
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            full_url = urljoin(self.url, href)
            self.info.stylesheets.append(full_url)

    def detect_technologies(self) -> list:
        """偵測網站使用的技術"""
        technologies = []

        if not self.soup:
            return technologies

        html = str(self.soup).lower()
        headers_str = str(self.info.headers).lower()

        # 偵測常見框架和技術
        tech_signatures = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'React': ['react', '_next', 'reactroot'],
            'Vue.js': ['vue', 'v-app', 'nuxt'],
            'Angular': ['ng-', 'angular'],
            'jQuery': ['jquery'],
            'Bootstrap': ['bootstrap'],
            'Tailwind CSS': ['tailwind'],
            'Google Analytics': ['google-analytics', 'gtag', 'ga.js'],
            'Google Tag Manager': ['googletagmanager'],
            'Cloudflare': ['cloudflare'],
            'nginx': ['nginx'],
            'Apache': ['apache'],
        }

        for tech, signatures in tech_signatures.items():
            for sig in signatures:
                if sig in html or sig in headers_str:
                    if tech not in technologies:
                        technologies.append(tech)
                    break

        return technologies

    def analyze(self) -> WebsiteInfo:
        """執行完整分析"""
        print(f"\n正在分析: {self.url}")
        print("=" * 50)

        if not self.fetch_page():
            return self.info

        print("擷取基本資訊...")
        self.extract_basic_info()

        print("分析連結...")
        self.extract_links()

        print("擷取圖片...")
        self.extract_images()

        print("擷取資源檔案...")
        self.extract_resources()

        return self.info

    def generate_report(self) -> str:
        """生成文字報告"""
        technologies = self.detect_technologies()

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                     網站分析報告                               ║
╚══════════════════════════════════════════════════════════════╝

📌 基本資訊
────────────────────────────────────────────────────────────────
URL: {self.info.url}
標題: {self.info.title}
描述: {self.info.description[:100] + '...' if len(self.info.description) > 100 else self.info.description}
語言: {self.info.language}
HTTP 狀態碼: {self.info.status_code}
回應時間: {self.info.response_time:.2f} 秒

📊 連結統計
────────────────────────────────────────────────────────────────
內部連結: {len(self.info.internal_links)} 個
外部連結: {len(self.info.external_links)} 個
圖片數量: {len(self.info.images)} 個
JavaScript 檔案: {len(self.info.scripts)} 個
CSS 檔案: {len(self.info.stylesheets)} 個

🔧 偵測到的技術
────────────────────────────────────────────────────────────────
{', '.join(technologies) if technologies else '無法偵測'}

📝 Meta 標籤
────────────────────────────────────────────────────────────────"""

        for name, content in list(self.info.meta_tags.items())[:10]:
            report += f"\n{name}: {content[:50]}..."

        report += f"""

🔗 前 10 個內部連結
────────────────────────────────────────────────────────────────"""
        for link in self.info.internal_links[:10]:
            report += f"\n• {link['url'][:70]}..."

        report += f"""

🌐 前 10 個外部連結
────────────────────────────────────────────────────────────────"""
        for link in self.info.external_links[:10]:
            report += f"\n• {link['url'][:70]}..."

        report += f"""

────────────────────────────────────────────────────────────────
分析時間: {self.info.analyzed_at}
"""
        return report

    def export_json(self, filename: str = None):
        """匯出為 JSON 檔案"""
        if not filename:
            # 使用網站域名作為檔名
            safe_domain = self.domain.replace('.', '_').replace(':', '_')
            filename = f"analysis_{safe_domain}.json"

        data = {
            'url': self.info.url,
            'title': self.info.title,
            'description': self.info.description,
            'keywords': self.info.keywords,
            'language': self.info.language,
            'status_code': self.info.status_code,
            'response_time': self.info.response_time,
            'technologies': self.detect_technologies(),
            'statistics': {
                'internal_links': len(self.info.internal_links),
                'external_links': len(self.info.external_links),
                'images': len(self.info.images),
                'scripts': len(self.info.scripts),
                'stylesheets': len(self.info.stylesheets),
            },
            'meta_tags': self.info.meta_tags,
            'internal_links': self.info.internal_links[:50],  # 限制數量
            'external_links': self.info.external_links[:50],
            'images': self.info.images[:50],
            'analyzed_at': self.info.analyzed_at,
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 已匯出到: {filename}")
        return filename


def main():
    """主程式"""
    # 預設測試網址
    default_url = "https://www.python.org"

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(f"請輸入要分析的網址 (預設: {default_url}): ").strip()
        if not url:
            url = default_url

    # 確保 URL 有協議前綴
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # 執行分析
    analyzer = WebsiteAnalyzer(url)
    analyzer.analyze()

    # 顯示報告
    print(analyzer.generate_report())

    # 匯出 JSON
    export = input("\n是否匯出 JSON 報告? (y/n): ").strip().lower()
    if export == 'y':
        analyzer.export_json()


if __name__ == "__main__":
    main()
