"""
Scrapy 設定檔
=============
專案的所有設定都在這裡配置
"""

# 專案名稱
BOT_NAME = "quotes_scraper"

# Spider 模組路徑
SPIDER_MODULES = ["quotes_scraper.spiders"]
NEWSPIDER_MODULE = "quotes_scraper.spiders"

# =====================================
# 爬蟲行為設定
# =====================================

# 是否遵守 robots.txt
ROBOTSTXT_OBEY = True

# 同時請求數量
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 下載延遲（秒）- 避免對伺服器造成過大壓力
DOWNLOAD_DELAY = 1

# 隨機化下載延遲 (0.5 * DOWNLOAD_DELAY 到 1.5 * DOWNLOAD_DELAY)
RANDOMIZE_DOWNLOAD_DELAY = True

# =====================================
# 請求標頭設定
# =====================================

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

# User-Agent（可以使用 scrapy-fake-useragent 擴展來輪換）
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# =====================================
# 中介軟體設定
# =====================================

# Spider 中介軟體
SPIDER_MIDDLEWARES = {
    # "quotes_scraper.middlewares.QuotesScraperSpiderMiddleware": 543,
}

# 下載器中介軟體
DOWNLOADER_MIDDLEWARES = {
    "quotes_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "quotes_scraper.middlewares.RetryMiddleware": 500,
}

# =====================================
# 管線設定（資料處理）
# =====================================

ITEM_PIPELINES = {
    "quotes_scraper.pipelines.CleanDataPipeline": 100,
    "quotes_scraper.pipelines.DuplicateFilterPipeline": 200,
    "quotes_scraper.pipelines.JsonWriterPipeline": 300,
    "quotes_scraper.pipelines.SQLitePipeline": 400,
}

# =====================================
# 快取設定（開發時建議開啟）
# =====================================

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1 小時
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 408]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# =====================================
# 日誌設定
# =====================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_FILE = None  # 設定檔案路徑來儲存日誌

# =====================================
# 輸出設定
# =====================================

# 自動輸出到檔案
FEEDS = {
    "output/quotes_%(time)s.json": {
        "format": "json",
        "encoding": "utf8",
        "store_empty": False,
        "indent": 2,
    },
    "output/quotes_%(time)s.csv": {
        "format": "csv",
        "encoding": "utf8",
    },
}

# =====================================
# 其他設定
# =====================================

# 請求超時（秒）
DOWNLOAD_TIMEOUT = 30

# 重試設定
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 自動節流（當伺服器回應變慢時自動降低速度）
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Twisted reactor 設定（用於 scrapy-playwright）
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# 設定 Python 版本兼容性
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
