# Scrapy 框架完整教學

> Python 最強大的網頁爬蟲框架

## 什麼是 Scrapy?

Scrapy 是一個基於 Twisted 非同步網路引擎的 Python 網頁爬蟲框架。它專為大規模資料擷取而設計，提供高效能、可擴展的解決方案。

### Scrapy 的優勢

- **高效能**：內建非同步處理，可同時處理多個請求
- **可擴展**：支援中介軟體、管線等擴展機制
- **功能完整**：內建請求處理、資料解析、儲存等功能
- **社群活躍**：豐富的插件和文件資源

## 安裝 Scrapy

```bash
# 使用 uv (推薦)
uv pip install scrapy

# 或使用 pip
pip install scrapy
```

## 建立 Scrapy 專案

```bash
# 建立新專案
scrapy startproject myproject

# 進入專案目錄
cd myproject

# 查看專案結構
tree
```

### 專案結構

```
myproject/
├── myproject/
│   ├── __init__.py
│   ├── items.py          # 定義資料結構
│   ├── middlewares.py    # 中介軟體
│   ├── pipelines.py      # 資料處理管線
│   ├── settings.py       # 專案設定
│   └── spiders/          # 爬蟲程式
│       └── __init__.py
└── scrapy.cfg
```

## 建立爬蟲 (Spider)

```bash
# 使用命令建立爬蟲
scrapy genspider products example.com
```

### 基本爬蟲範例

```python
# spiders/products.py
import scrapy

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['web-scraping.dev']
    start_urls = ['https://web-scraping.dev/products']

    def parse(self, response):
        # 找到所有產品連結
        product_links = response.xpath(
            "//div[@class='product-card']//h3/a/@href"
        ).getall()

        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        # 處理分頁
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        yield {
            'title': response.xpath("//h1/text()").get(),
            'price': response.css('.price::text').get(),
            'description': response.css('.description::text').get(),
            'url': response.url,
        }
```

## 選擇器：XPath vs CSS

### XPath 選擇器

```python
# 取得文字
response.xpath('//h1/text()').get()

# 取得屬性
response.xpath('//a/@href').get()

# 取得多個元素
response.xpath('//div[@class="item"]').getall()

# 包含特定文字
response.xpath('//div[contains(@class, "product")]')

# 取得所有文字 (包含子元素)
response.xpath('//div//text()').getall()
```

### CSS 選擇器

```python
# 取得文字
response.css('h1::text').get()

# 取得屬性
response.css('a::attr(href)').get()

# 取得多個元素
response.css('div.item').getall()

# 組合選擇器
response.css('div.product > h3.title::text').get()
```

## 設定檔 (settings.py)

```python
# settings.py

# 基本設定
BOT_NAME = 'myproject'
ROBOTSTXT_OBEY = False  # 是否遵守 robots.txt

# 同時請求數量
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 下載延遲 (秒)
DOWNLOAD_DELAY = 1

# 請求標頭
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}

# 啟用快取 (開發時建議開啟)
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = 'httpcache'

# 日誌等級
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# 輸出設定
FEEDS = {
    'output.json': {
        'format': 'json',
        'encoding': 'utf8',
        'overwrite': True,
    },
}
```

## Item 定義

```python
# items.py
import scrapy

class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    crawled_at = scrapy.Field()
```

### 在爬蟲中使用 Item

```python
# spiders/products.py
from myproject.items import ProductItem
from datetime import datetime

class ProductsSpider(scrapy.Spider):
    # ...

    def parse_product(self, response):
        item = ProductItem()
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('.price::text').get()
        item['description'] = response.css('.description::text').get()
        item['url'] = response.url
        item['crawled_at'] = datetime.now().isoformat()
        yield item
```

## Pipeline 資料處理

```python
# pipelines.py
from itemadapter import ItemAdapter

class CleanDataPipeline:
    """清理資料的管線"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 清理價格
        price = adapter.get('price', '')
        if price:
            adapter['price'] = float(price.replace('$', '').strip())

        # 清理標題
        title = adapter.get('title', '')
        if title:
            adapter['title'] = title.strip()

        return item


class FilterPricePipeline:
    """過濾低價產品"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get('price', 0)

        if price < 10:
            raise DropItem(f"價格過低: {item}")

        return item


class SaveToDBPipeline:
    """儲存到資料庫"""

    def open_spider(self, spider):
        # 開啟資料庫連線
        self.connection = sqlite3.connect('products.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                title TEXT,
                price REAL,
                url TEXT
            )
        ''')

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cursor.execute('''
            INSERT INTO products (title, price, url)
            VALUES (?, ?, ?)
        ''', (adapter['title'], adapter['price'], adapter['url']))
        self.connection.commit()
        return item
```

### 在 settings.py 啟用 Pipeline

```python
# settings.py
ITEM_PIPELINES = {
    'myproject.pipelines.CleanDataPipeline': 100,
    'myproject.pipelines.FilterPricePipeline': 200,
    'myproject.pipelines.SaveToDBPipeline': 300,
}
# 數字越小，優先順序越高
```

## Middleware 中介軟體

### 下載器中介軟體

```python
# middlewares.py
import random

class RotateUserAgentMiddleware:
    """輪換 User-Agent"""

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        return None


class RetryMiddleware:
    """自訂重試邏輯"""

    def process_response(self, request, response, spider):
        if response.status == 403:
            spider.logger.warning(f'403 錯誤: {request.url}')
            # 可以在這裡加入重試邏輯
        return response
```

## 執行爬蟲

```bash
# 執行爬蟲
scrapy crawl products

# 輸出到檔案
scrapy crawl products -o output.json
scrapy crawl products -o output.csv

# 傳遞參數
scrapy crawl products -a category=electronics

# 在爬蟲中接收參數
class ProductsSpider(scrapy.Spider):
    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
```

## 處理 JavaScript 頁面

### 使用 Scrapy-Playwright

```bash
uv pip install scrapy-playwright
playwright install chromium
```

```python
# settings.py
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# spiders/dynamic.py
import scrapy

class DynamicSpider(scrapy.Spider):
    name = 'dynamic'

    def start_requests(self):
        yield scrapy.Request(
            'https://example.com',
            meta={
                'playwright': True,
                'playwright_include_page': True,
            },
        )

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.wait_for_selector('.product-card')

        # 繼續解析...
        yield {
            'title': response.css('h1::text').get(),
        }

        await page.close()
```

## 實用技巧

### 1. 使用 ItemLoader 簡化資料處理

```python
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    price_in = MapCompose(str.strip, lambda x: x.replace('$', ''))
    title_in = MapCompose(str.strip)
    description_out = Join(' ')

# 使用
loader = ProductLoader(item=ProductItem(), response=response)
loader.add_css('title', 'h1::text')
loader.add_css('price', '.price::text')
item = loader.load_item()
```

### 2. 處理分頁

```python
def parse(self, response):
    # 處理當前頁面的資料
    for product in response.css('.product'):
        yield {...}

    # 取得下一頁連結
    next_page = response.css('a.next::attr(href)').get()
    if next_page:
        yield response.follow(next_page, callback=self.parse)
```

### 3. 使用 CrawlSpider 自動追蹤連結

```python
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AllProductsSpider(CrawlSpider):
    name = 'all_products'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com']

    rules = (
        Rule(LinkExtractor(allow=r'/category/'), follow=True),
        Rule(LinkExtractor(allow=r'/product/\d+'), callback='parse_product'),
    )

    def parse_product(self, response):
        yield {
            'title': response.css('h1::text').get(),
            'url': response.url,
        }
```

## 常用命令

```bash
# 列出所有爬蟲
scrapy list

# 測試爬蟲 (互動式)
scrapy shell 'https://example.com'

# 檢查爬蟲
scrapy check products

# 測試解析特定 URL
scrapy parse --spider=products https://example.com/product/1
```

## 下一步

學會 Scrapy 後，接下來學習如何將爬取的資料儲存到各種格式和資料庫。

---

*參考資源：Scrapfly, Scrapy 官方文件 (2024-2025)*
