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

class WordArticleSpider(CrawlSpider):
    name = "examw.com"
    allowed_domains = ["examw.com"]
    start_urls = ['http://www.examw.com/oa/word/',
                  'http://www.examw.com/oa/excel/',
                  'http://www.examw.com/oa/powerpoint/']
    #allowed_domains = ["officezu.com"]
    #start_urls = ['http://www.officezu.com/word/2003']
                  #'http://www.officezu.com/word/jiqiao']

    rules = (
        #Rule(lxml(allow=('/a/word/\d{3}.html$', )), callback='parse_item'),
        #Rule(lxml(allow=('/word/2003/index\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/word/jiqiao/index\d+.html$', )), follow=True),
        Rule(lxml(allow=('/oa/word/\d+/$', )), callback='parse_word'),
        Rule(lxml(allow=('/oa/word/indexA\d.html$', )), follow=True),
        Rule(lxml(allow=('/oa/word/index\d+.html$', )), follow=True),
        Rule(lxml(allow=('/oa/excel/\d+/?$', )), callback='parse_excel'),
        Rule(lxml(allow=('/oa/excel/indexA\d.html$', )), follow=True),
        Rule(lxml(allow=('/oa/excel/index\d+.html$', )), follow=True),
        Rule(lxml(allow=('/oa/powerpoint/\d+/?$', )), callback='parse_powerpoint'),
        Rule(lxml(allow=('/oa/powerpoint/indexA\d.html$', )), follow=True),
        Rule(lxml(allow=('/oa/powerpoint/index\d+.html$', )), follow=True),
    )

    def parse_item(self, response):
        pass

    def extract_article(self, response, content):
        aid = response.url.split('/')[-2]
        # 解决乱码cp1252, 比如171852
        title = response.css('#News h3::text').extract()[0]
        content = ''.join(content)
        if response.encoding == 'cp1252':
            try:
                title = title.encode('cp1252').decode('gb2312').encode('utf-8')
                content = content.encode('cp1252').decode('gb2312').encode('utf-8')
            except UnicodeEncodeError, UnicodeDecodeError:
                title = title.replace(' ', '')
                content = content.replace(' ', '')
                title = title.encode('cp1252').decode('gbk').encode('utf-8')
                content = content.encode('cp1252').decode('gbk').encode('utf-8')
        return aid, title, content

    def parse_examw_item(self, response, cat):
        items = []
        # check if has p tag in html file, 比如211756
        content_p = response.xpath('//div[@id="NewsBox"]/p[descendant-or-self::text()]').extract()
        content_1 = ''
        content_2 = ''
        if len(content_p) > 0:
            aid, title, content_1 = self.extract_article(response, content_p)

        content_box = response.css('#NewsBox::text').extract()
        content_box = [line.strip() for line in content_box]
        if len(content_box) > 0:
            aid, title, content_2 = self.extract_article(response, content_box)
        if not len(content_box) and not len(content_p):
            self.log('"%s" NotParsed' % response.url, level=log.WARNING)
        item = ArticleItem()
        item['aid'] = aid
        item['title'] = title
        item['content'] = content_1 + content_2
        item['category'] = cat
        items.append(item)
        time.sleep(1)
        return items

    def parse_word(self, response):
        return self.parse_examw_item(response, 'word')

    def parse_excel(self, response):
        return self.parse_examw_item(response, 'excel')

    def parse_powerpoint(self, response):
        return self.parse_examw_item(response, 'powerpoint')
