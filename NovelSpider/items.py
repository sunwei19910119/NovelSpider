# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re
import scrapy
from scrapy.loader import ItemLoader

class NovelspiderItem(scrapy.Item):
    pass


class ZxcsItem(scrapy.Item):
    file_urls = scrapy.Field()
    file = scrapy.Field()

