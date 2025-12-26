"""
Quotes Spider - 名言爬蟲
========================
爬取 http://quotes.toscrape.com 的名言和作者資訊

使用方法：
    scrapy crawl quotes
    scrapy crawl quotes -o output.json
    scrapy crawl quotes -a max_pages=5
"""

import scrapy
from datetime import datetime
from urllib.parse import urljoin
from quotes_scraper.items import QuoteItem, AuthorItem, QuoteLoader, AuthorLoader


class QuotesSpider(scrapy.Spider):
    """名言爬蟲"""

    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, max_pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_pages = int(max_pages) if max_pages else None
        self.page_count = 0
        self.scraped_authors = set()

    def parse(self, response):
        """解析名言列表頁面"""
        self.page_count += 1
        self.logger.info(f"正在處理第 {self.page_count} 頁: {response.url}")

        # 擷取每條名言
        for quote_div in response.css('div.quote'):
            yield from self.parse_quote(quote_div, response)

        # 處理分頁
        if self.max_pages and self.page_count >= self.max_pages:
            self.logger.info(f"已達到最大頁數限制: {self.max_pages}")
            return

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_quote(self, quote_div, response):
        """解析單條名言"""
        # 使用 ItemLoader 來處理資料
        loader = QuoteLoader(item=QuoteItem(), selector=quote_div)

        loader.add_css('text', 'span.text::text')
        loader.add_css('author', 'small.author::text')
        loader.add_css('author_url', 'a[href*="author"]::attr(href)')
        loader.add_css('tags', 'a.tag::text')
        loader.add_value('source_url', response.url)
        loader.add_value('scraped_at', datetime.now().isoformat())

        item = loader.load_item()

        # 處理 author_url（轉換為完整 URL）
        if item.get('author_url'):
            item['author_url'] = urljoin(response.url, item['author_url'])

            # 爬取作者資訊（避免重複）
            author = item.get('author', '')
            if author and author not in self.scraped_authors:
                self.scraped_authors.add(author)
                yield response.follow(
                    item['author_url'],
                    callback=self.parse_author,
                    meta={'author_name': author}
                )

        yield item

    def parse_author(self, response):
        """解析作者頁面"""
        self.logger.info(f"正在擷取作者: {response.meta.get('author_name')}")

        loader = AuthorLoader(item=AuthorItem(), response=response)

        loader.add_css('name', 'h3.author-title::text')
        loader.add_css('born_date', 'span.author-born-date::text')
        loader.add_css('born_location', 'span.author-born-location::text')
        loader.add_css('description', 'div.author-description::text')
        loader.add_value('url', response.url)
        loader.add_value('scraped_at', datetime.now().isoformat())

        yield loader.load_item()


class QuotesTagSpider(scrapy.Spider):
    """依標籤爬取名言"""

    name = "quotes_tag"
    allowed_domains = ["quotes.toscrape.com"]

    def __init__(self, tag='love', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = tag
        self.start_urls = [f"http://quotes.toscrape.com/tag/{tag}/"]

    def parse(self, response):
        """解析標籤頁面"""
        self.logger.info(f"正在爬取標籤: {self.tag}")

        for quote_div in response.css('div.quote'):
            loader = QuoteLoader(item=QuoteItem(), selector=quote_div)

            loader.add_css('text', 'span.text::text')
            loader.add_css('author', 'small.author::text')
            loader.add_css('tags', 'a.tag::text')
            loader.add_value('source_url', response.url)
            loader.add_value('scraped_at', datetime.now().isoformat())

            yield loader.load_item()

        # 分頁
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


class QuotesAllTagsSpider(scrapy.Spider):
    """爬取所有標籤的名言"""

    name = "quotes_all_tags"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        """首先擷取所有標籤"""
        tag_links = response.css('div.tags-box a.tag::attr(href)').getall()
        self.logger.info(f"找到 {len(tag_links)} 個標籤")

        for tag_link in tag_links:
            yield response.follow(tag_link, callback=self.parse_tag_page)

    def parse_tag_page(self, response):
        """解析標籤頁面"""
        current_tag = response.css('h3.tag::text').get()
        self.logger.info(f"正在爬取標籤: {current_tag}")

        for quote_div in response.css('div.quote'):
            loader = QuoteLoader(item=QuoteItem(), selector=quote_div)

            loader.add_css('text', 'span.text::text')
            loader.add_css('author', 'small.author::text')
            loader.add_css('tags', 'a.tag::text')
            loader.add_value('source_url', response.url)
            loader.add_value('scraped_at', datetime.now().isoformat())

            yield loader.load_item()

        # 分頁
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_tag_page)
