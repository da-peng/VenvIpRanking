# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class VenviprankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IpItem(Item):
    ip = Field()#  代理ip地址
    port = Field() #端口
    address = Field() # 服务地址

