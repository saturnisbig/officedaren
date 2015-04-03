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
        Rule(lxml(allow=('/word/2003/', )), follow=True),
        Rule(lxml(allow=('/word/2003/1017_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/word/2007/\d+.html$', )), callback='parse_word_2007'),
        Rule(lxml(allow=('/word/2007/', )), follow=True),
        Rule(lxml(allow=('/word/2007/1018_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/word/2010/\d+.html$', )), callback='parse_word_2010'),
        Rule(lxml(allow=('/word/2010/', )), follow=True),
        #Rule(lxml(allow=('/word/2010/1019_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/word/jiqiao/\d+.html$', )),
             callback='parse_word_jiqiao'),
        Rule(lxml(allow=('/word/jiqiao/', )), follow=True),
        Rule(lxml(allow=('/word/jiqiao/1023_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/word/wenda/\d+.html$', )),
             callback='parse_word_wenda'),
        Rule(lxml(allow=('/word/wenda/', )), follow=True),
        Rule(lxml(allow=('/word/wenda/1022_\d+.html$', )), follow=True),
        # excel
        Rule(lxml(allow=('/excel/jichu/\d+.html$', )),
             callback='parse_excel_jichu'),
        Rule(lxml(allow=('/excel/jichu/', )), follow=True),
        Rule(lxml(allow=('/excel/jichu/1010_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/excel/biaoge/\d+.html$', )),
             callback='parse_excel_biaoge'),
        Rule(lxml(allow=('/excel/biaoge/', )), follow=True),
        Rule(lxml(allow=('/excel/biaoge/1011_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/excel/hanshu/\d+.html$', )),
             callback='parse_excel_hanshu'),
        Rule(lxml(allow=('/excel/hanshu/', )), follow=True),
        Rule(lxml(allow=('/excel/2003/\d+.html$', )), callback='parse_excel_2003'),
        Rule(lxml(allow=('/excel/2003/', )), follow=True),
        Rule(lxml(allow=('/excel/2007/\d+.html$', )), callback='parse_excel_2007'),
        Rule(lxml(allow=('/excel/2007/', )), follow=True),
        Rule(lxml(allow=('/excel/2010/\d+.html$', )), callback='parse_excel_2010'),
        Rule(lxml(allow=('/excel/2010/', )), follow=True),
        # ppt
        Rule(lxml(allow=('/ppt/jichu/\d+.html$', )), callback='parse_ppt_jichu'),
        Rule(lxml(allow=('/ppt/jichu/', )), follow=True),
        Rule(lxml(allow=('/ppt/jichu/1004_\d+.html$', )), follow=True),
        Rule(lxml(allow=('/ppt/gaoji/\d+.html$', )), callback='parse_ppt_gaoji'),
        Rule(lxml(allow=('/ppt/gaoji/', )), follow=True),
        Rule(lxml(allow=('/ppt/zhizuo/\d+.html$', )), callback='parse_ppt_gaoji'),
        Rule(lxml(allow=('/ppt/zhizuo/', )), follow=True),
        Rule(lxml(allow=('/ppt/2003/\d+.html$', )), callback='parse_ppt_2003'),
        Rule(lxml(allow=('/ppt/2003/', )), follow=True),
        Rule(lxml(allow=('/ppt/2007/\d+.html$', )), callback='parse_ppt_2007'),
        Rule(lxml(allow=('/ppt/2007/', )), follow=True),
        Rule(lxml(allow=('/ppt/2010/\d+.html$', )), callback='parse_ppt_2010'),
        Rule(lxml(allow=('/ppt/2010/', )), follow=True),
    )

    def parse_examw_item(self, response, cat):
        items = []
        # check if has p tag in html file, 比如211756
        content = response.css('#conbox')
        content = content.xpath('string(.)').extract()
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

    def parse_word_2007(self, response):
        return self.parse_examw_item(response, 'word_2007')

    def parse_word_2010(self, response):
        return self.parse_examw_item(response, 'word_2010')

    def parse_word_jiqiao(self, response):
        return self.parse_examw_item(response, 'word_jiqiao')

    def parse_word_wenda(self, response):
        return self.parse_examw_item(response, 'word_wenda')

    def parse_excel_jichu(self, response):
        return self.parse_examw_item(response, 'excel_jichu')

    def parse_excel_biaoge(self, response):
        return self.parse_examw_item(response, 'excel_biaoge')

    def parse_excel_hanshu(self, response):
        return self.parse_examw_item(response, 'excel_hanshu')

    def parse_excel_2003(self, response):
        return self.parse_examw_item(response, 'excel_2003')

    def parse_excel_2007(self, response):
        return self.parse_examw_item(response, 'excel_2007')

    def parse_excel_2010(self, response):
        return self.parse_examw_item(response, 'excel_2010')

    def parse_ppt_jichu(self, response):
        return self.parse_examw_item(response, 'ppt_jichu')

    def parse_ppt_gaoji(self, response):
        return self.parse_examw_item(response, 'ppt_gaoji')

    def parse_ppt_2003(self, response):
        return self.parse_examw_item(response, 'ppt_2003')

    def parse_ppt_2007(self, response):
        return self.parse_examw_item(response, 'ppt_2007')

    def parse_ppt_2010(self, response):
        return self.parse_examw_item(response, 'ppt_2010')

    def extract_article(self, response, content):
        aid = response.url.split('/')[-1][:-5]
        # 解决乱码cp1252, 比如171852
        title = response.css('.con_box h2::text').extract()[0]
        content = ''.join(content)
        if response.encoding == 'cp1252':
            title = title.encode('cp1252').decode('gb2312').encode('utf-8')
            content = content.encode('cp1252').decode('gb2312').encode('utf-8')
        return aid, title, content

