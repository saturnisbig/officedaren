# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
#import scrapy


class ArticleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    content = Field()
    category = Field()
    publishTime = Field()
