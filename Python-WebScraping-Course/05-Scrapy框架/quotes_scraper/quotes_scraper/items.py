"""
Scrapy Items 定義
==================
定義爬蟲要擷取的資料結構
"""

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader


def clean_text(text):
    """清理文字：移除多餘空白"""
    if isinstance(text, str):
        return ' '.join(text.split())
    return text


def parse_tags(tags_text):
    """解析標籤"""
    if isinstance(tags_text, str):
        return [t.strip() for t in tags_text.split(',') if t.strip()]
    return tags_text


class QuoteItem(scrapy.Item):
    """名言資料結構"""
    text = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    tags = scrapy.Field()
    source_url = scrapy.Field()
    scraped_at = scrapy.Field()


class AuthorItem(scrapy.Item):
    """作者資料結構"""
    name = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()


class QuoteLoader(ItemLoader):
    """名言 ItemLoader - 自動處理資料"""
    default_output_processor = TakeFirst()

    text_in = MapCompose(clean_text, lambda x: x.strip('""'))
    author_in = MapCompose(clean_text)
    tags_out = lambda x: x  # 保持列表格式


class AuthorLoader(ItemLoader):
    """作者 ItemLoader"""
    default_output_processor = TakeFirst()

    name_in = MapCompose(clean_text)
    born_location_in = MapCompose(clean_text, lambda x: x.replace('in ', ''))
    description_in = MapCompose(clean_text)
    description_out = Join(' ')
