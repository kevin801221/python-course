# Quotes Scraper - Scrapy 完整專案範例

這是一個使用 Scrapy 框架的完整網頁爬蟲專案，用於爬取 http://quotes.toscrape.com 網站的名言和作者資訊。

## 專案結構

```
quotes_scraper/
├── scrapy.cfg                 # Scrapy 配置檔
├── quotes.db                  # SQLite 資料庫（執行後產生）
├── README.md                  # 專案說明
└── quotes_scraper/
    ├── __init__.py
    ├── items.py               # 資料結構定義
    ├── middlewares.py         # 中介軟體
    ├── pipelines.py           # 資料處理管線
    ├── settings.py            # 專案設定
    └── spiders/
        ├── __init__.py
        └── quotes_spider.py   # 爬蟲程式
```

## 安裝

```bash
# 安裝 Scrapy
uv pip install scrapy

# 進入專案目錄
cd quotes_scraper
```

## 使用方法

### 基本爬取

```bash
# 執行主爬蟲
scrapy crawl quotes

# 限制爬取頁數
scrapy crawl quotes -a max_pages=5

# 輸出到 JSON 檔案
scrapy crawl quotes -o quotes.json

# 輸出到 CSV 檔案
scrapy crawl quotes -o quotes.csv
```

### 依標籤爬取

```bash
# 爬取特定標籤
scrapy crawl quotes_tag -a tag=love
scrapy crawl quotes_tag -a tag=life

# 爬取所有標籤
scrapy crawl quotes_all_tags
```

### 測試與除錯

```bash
# 互動式 Shell
scrapy shell 'http://quotes.toscrape.com'

# 在 Shell 中測試選擇器
>>> response.css('div.quote span.text::text').getall()
>>> response.xpath('//small[@class="author"]/text()').get()

# 列出所有爬蟲
scrapy list

# 檢查爬蟲
scrapy check quotes
```

## 功能特色

### 1. Items & ItemLoader
- 使用 `dataclass` 風格的 Item 定義
- ItemLoader 自動清理和處理資料

### 2. Middlewares
- RandomUserAgentMiddleware: 隨機 User-Agent
- RetryMiddleware: 自訂重試邏輯
- ProxyMiddleware: 代理支援（範例）

### 3. Pipelines
- CleanDataPipeline: 清理資料
- DuplicateFilterPipeline: 過濾重複
- JsonWriterPipeline: 寫入 JSON Lines
- SQLitePipeline: 儲存到 SQLite

### 4. 其他功能
- 自動節流（AutoThrottle）
- HTTP 快取
- 隨機延遲
- 詳細日誌

## 設定說明

主要設定在 `settings.py`：

```python
# 同時請求數
CONCURRENT_REQUESTS = 16

# 下載延遲
DOWNLOAD_DELAY = 1

# 啟用 Pipeline
ITEM_PIPELINES = {
    "quotes_scraper.pipelines.CleanDataPipeline": 100,
    "quotes_scraper.pipelines.SQLitePipeline": 400,
}
```

## 輸出範例

### JSON 格式

```json
{
  "text": "The world as we have created it is a process of our thinking.",
  "author": "Albert Einstein",
  "author_url": "http://quotes.toscrape.com/author/Albert-Einstein",
  "tags": ["change", "deep-thoughts", "thinking", "world"],
  "source_url": "http://quotes.toscrape.com/",
  "scraped_at": "2024-01-15T10:30:00"
}
```

### SQLite 資料庫

```sql
-- 查詢所有名言
SELECT * FROM quotes;

-- 依作者統計
SELECT author, COUNT(*) as count
FROM quotes
GROUP BY author
ORDER BY count DESC;

-- 搜尋標籤
SELECT * FROM quotes WHERE tags LIKE '%love%';
```

## 擴展建議

1. **加入代理池**: 修改 `ProxyMiddleware`
2. **整合 Playwright**: 處理 JavaScript 頁面
3. **加入 API 輸出**: 建立 REST API
4. **定時執行**: 使用 cron 或 celery

## 參考資源

- [Scrapy 官方文件](https://docs.scrapy.org/)
- [Scrapy 教學](https://docs.scrapy.org/en/latest/intro/tutorial.html)
