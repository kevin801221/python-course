# Python 網頁爬蟲完整教學課程

> 從入門到進階的 Python 網頁爬蟲學習資源 (2024-2025)

## 課程概述

本課程整理自網路上最新、最優質的 Python 網頁爬蟲教學資源，涵蓋從基礎到進階的完整學習路徑。

## 課程目錄

### 01 - 爬蟲入門基礎
- [網頁爬蟲概述](01-爬蟲入門基礎/01-網頁爬蟲概述.md) - 了解網頁爬蟲的基本概念與工具總覽
- **實作專案**: [website_analyzer.py](01-爬蟲入門基礎/website_analyzer.py) - 網站資訊分析器

### 02 - Requests 與 HTTP 請求
- [Requests 基礎教學](02-Requests與HTTP請求/01-Requests基礎教學.md) - 學習 Python 最受歡迎的 HTTP 請求函式庫
- **實作專案**: [news_scraper.py](02-Requests與HTTP請求/news_scraper.py) - 新聞聚合爬蟲

### 03 - BeautifulSoup 解析
- [BeautifulSoup 基礎教學](03-BeautifulSoup解析/01-BeautifulSoup基礎教學.md) - 掌握 HTML 解析與資料擷取
- **實作專案**: [book_scraper.py](03-BeautifulSoup解析/book_scraper.py) - 書籍商城爬蟲

### 04 - Selenium 動態爬取
- [Selenium 基礎教學](04-Selenium動態爬取/01-Selenium基礎教學.md) - 處理 JavaScript 渲染的動態網頁
- **實作專案**: [quotes_scraper.py](04-Selenium動態爬取/quotes_scraper.py) - 動態網頁爬蟲

### 05 - Scrapy 框架
- [Scrapy 框架教學](05-Scrapy框架/01-Scrapy框架教學.md) - 使用 Python 最強大的爬蟲框架
- **實作專案**: [quotes_scraper/](05-Scrapy框架/quotes_scraper/) - 完整 Scrapy 專案

### 06 - 資料儲存與處理
- [資料儲存教學](06-資料儲存與處理/01-資料儲存教學.md) - CSV、JSON、Excel、資料庫儲存
- **實作專案**: [data_manager.py](06-資料儲存與處理/data_manager.py) - 多格式資料管理器

### 07 - 反爬蟲對策
- [反爬蟲對策教學](07-反爬蟲對策/01-反爬蟲對策教學.md) - 避免被封鎖的技巧與最佳實踐
- **實作專案**: [robust_scraper.py](07-反爬蟲對策/robust_scraper.py) - 穩健爬蟲

## 建議學習順序

```
基礎篇                     進階篇
   │                         │
   ▼                         ▼
01-爬蟲入門 ──► 02-Requests ──► 03-BeautifulSoup
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
            04-Selenium                           05-Scrapy
            (動態網頁)                            (大規模爬蟲)
                    │                                   │
                    └─────────────┬─────────────────────┘
                                  ▼
                          06-資料儲存
                                  │
                                  ▼
                          07-反爬蟲對策
```

## 快速開始

### 環境設置

```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安裝必要套件
uv pip install requests beautifulsoup4 lxml selenium scrapy pandas
```

### 第一個爬蟲程式

```python
import requests
from bs4 import BeautifulSoup

# 發送請求
response = requests.get('https://example.com')

# 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 取得標題
title = soup.find('h1').text
print(f'網頁標題: {title}')
```

## 工具比較

| 工具 | 用途 | 難度 | 速度 | JavaScript |
|------|------|------|------|------------|
| Requests | HTTP 請求 | 簡單 | 快 | 不支援 |
| BeautifulSoup | HTML 解析 | 簡單 | 快 | 不支援 |
| Selenium | 瀏覽器自動化 | 中等 | 慢 | 支援 |
| Scrapy | 爬蟲框架 | 進階 | 非常快 | 需擴展 |
| Playwright | 現代瀏覽器自動化 | 中等 | 中等 | 支援 |

## 學習資源

- [ScrapingBee 教學](https://www.scrapingbee.com/blog/)
- [Real Python 教學](https://realpython.com/tutorials/web-scraping/)
- [Scrapy 官方文件](https://docs.scrapy.org/)
- [Selenium 官方文件](https://www.selenium.dev/documentation/)

## 實作專案總覽

每個章節都包含一個完整的 Python 應用程式，可以直接執行學習：

| 專案 | 說明 | 主要技術 |
|------|------|----------|
| `website_analyzer.py` | 網站資訊分析器 | Requests, BeautifulSoup |
| `news_scraper.py` | 新聞聚合爬蟲 | Requests, Session, 重試機制 |
| `book_scraper.py` | 書籍商城爬蟲 | BeautifulSoup, 分頁處理 |
| `quotes_scraper.py` | 動態網頁爬蟲 | Selenium, 無限滾動 |
| `quotes_scraper/` | Scrapy 專案 | Scrapy, Pipeline, Middleware |
| `data_manager.py` | 多格式資料管理 | JSON, CSV, SQLite |
| `robust_scraper.py` | 穩健爬蟲 | 反反爬蟲, 代理, 重試 |

### 執行專案

```bash
# 進入專案目錄
cd Python-WebScraping-Course

# 安裝依賴
uv pip install requests beautifulsoup4 lxml selenium scrapy pandas fake-useragent

# 執行任一專案
python 01-爬蟲入門基礎/website_analyzer.py
python 02-Requests與HTTP請求/news_scraper.py
python 03-BeautifulSoup解析/book_scraper.py
# ...
```

## 注意事項

1. **法律責任**：請確保爬取行為符合當地法律和網站服務條款
2. **尊重 robots.txt**：遵守網站的爬取規則
3. **控制頻率**：避免對伺服器造成過大負擔
4. **保護隱私**：不要收集個人隱私資料

---

*本課程內容整理自 ScrapingBee, Oxylabs, Real Python, Scrapfly 等優質資源 (2024-2025)*
