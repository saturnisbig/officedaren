#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import re
import urllib2
import time
import os

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
#from scrapy.selector import Selector
from scrapy import log

from officedaren.items import ArticleItem


SITE_NAME = 'http://www.officedaren.com'

class XueXiLaSpider(CrawlSpider):
    name = "xuexila.com"
    allowed_domains = ["xuexila.com"]
    start_urls = ['http://www.xuexila.com/word/',
                  'http://www.xuexila.com/excel/',
                  'http://www.xuexila.com/ppt/',
                  'http://www.xuexila.com/diannao/wps/']
    rules = (
        # word
        Rule(lxml(allow=('/word/2003/\d+.html$', )), callback='parse_word_2003'),
             #cb_kwargs={'category': 'word_2003'}),
        #Rule(lxml(allow=('/word/2003/', )), follow=True),
        #Rule(lxml(allow=('/word/2003/1017_\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/word/2007/\d+.html$', )), callback='parse_word'),
        #Rule(lxml(allow=('/oa/word/index\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/oa/excel/\d+/?$', )), callback='parse_excel'),
        #Rule(lxml(allow=('/oa/excel/indexA\d.html$', )), follow=True),
        #Rule(lxml(allow=('/oa/excel/index\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/oa/powerpoint/\d+/?$', )), callback='parse_powerpoint'),
        #Rule(lxml(allow=('/oa/powerpoint/indexA\d.html$', )), follow=True),
        #Rule(lxml(allow=('/oa/powerpoint/index\d+.html$', )), follow=True),
    )

    def parse_examw_item(self, response, cat):
        items = []
        # check if has p tag in html file, 比如211756
        content = response.css('#conbox::text').extract()
        aid, title, content = self.extract_article(response, content)
        item = ArticleItem()
        item['aid'] = aid
        item['category'] = cat
        item['title'] = title
        item['content'] = content
        items.append(item)
        time.sleep(1)
        return items

    def parse_word_2003(self, response):
        return self.parse_examw_item(response, 'word_2003')

    def parse_excel(self, response):
        return self.parse_examw_item(response, 'excel')

    def parse_powerpoint(self, response):
        return self.parse_examw_item(response, 'powerpoint')

    def extract_article(self, response, content):
        aid = response.url.split('/')[-1][:-5]
        # 解决乱码cp1252, 比如171852
        title = response.css('.con_box h2::text').extract()[0]
        content = ''.join(content)
        if response.encoding == 'cp1252':
            title = title.encode('cp1252').decode('gb2312').encode('utf-8')
            content = content.encode('cp1252').decode('gb2312').encode('utf-8')
        return aid, title, content

