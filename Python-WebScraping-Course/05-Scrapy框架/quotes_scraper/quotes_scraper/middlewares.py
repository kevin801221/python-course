"""
Scrapy 中介軟體
===============
處理請求和回應的中介軟體
"""

import random
import logging
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware as BaseRetryMiddleware

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware:
    """隨機 User-Agent 中介軟體"""

    USER_AGENTS = [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        # Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",

        # Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",

        # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    ]

    def process_request(self, request, spider):
        """處理每個請求，隨機選擇 User-Agent"""
        request.headers['User-Agent'] = random.choice(self.USER_AGENTS)
        return None


class RetryMiddleware(BaseRetryMiddleware):
    """自訂重試中介軟體"""

    def process_response(self, request, response, spider):
        """處理回應"""
        if response.status == 403:
            logger.warning(f"403 Forbidden: {request.url}")
            # 可以在這裡加入額外處理，如更換代理

        if response.status == 429:
            logger.warning(f"429 Too Many Requests: {request.url}")
            # 可以增加延遲後重試

        return super().process_response(request, response, spider)


class QuotesScraperSpiderMiddleware:
    """Spider 中介軟體範例"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class ProxyMiddleware:
    """代理中介軟體（範例）"""

    PROXIES = [
        # 在這裡填入你的代理列表
        # "http://user:pass@proxy1.example.com:8080",
        # "http://user:pass@proxy2.example.com:8080",
    ]

    def process_request(self, request, spider):
        if self.PROXIES:
            proxy = random.choice(self.PROXIES)
            request.meta['proxy'] = proxy
            logger.debug(f"Using proxy: {proxy}")
        return None

    def process_exception(self, request, exception, spider):
        """代理失敗時處理"""
        if 'proxy' in request.meta:
            proxy = request.meta['proxy']
            logger.warning(f"Proxy failed: {proxy}")
            # 可以從列表中移除失敗的代理
