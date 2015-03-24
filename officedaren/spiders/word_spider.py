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
        items = []
        pat_a = re.compile(r'href=".+?"', re.M)
        pat_img = re.compile(r'src="(http:.+?)"', re.M)
        try:
            content = response.xpath('//div[@class="c_content"]').extract()[0]
        except IndexError:
            print "Parse content error:", response.url
        else:
            try:
                img_url = pat_img.findall(content)[0]
            except IndexError:
                print 'Not a normal articel', response.url
            else:
                title = response.css('#index_left .c_title::text').extract()[0]
                item = ArticleItem()
                img_name = img_url.split('/')[-1]
                self.fetch_img(img_url, img_name)
                content = pat_a.sub(SITE_NAME+'/word/', content)
                content = pat_img.sub(SITE_NAME+'/media/'+img_name, content)
                item['title'] = title
                item['content'] = content
                item['category'] = 'word'
                items.append(item)
        return items

    def fetch_img(self, img_url, img_name):
        img_path = 'media/' + img_name
        if not os.path.exists(img_path):
            img = urllib2.urlopen(img_url)
            with open(img_path, 'wb') as fd:
                fd.write(img.read())
            time.sleep(1)

    def extract_article(self, response, content):
        aid = response.url.split('/')[-2]
        # 解决乱码cp1252, 比如171852
        title = response.css('#News h3::text').extract()[0]
        content = ''.join(content)
        if response.encoding == 'cp1252':
            title = title.encode('cp1252').decode('gb2312').encode('utf-8')
            content = content.encode('cp1252').decode('gb2312').encode('utf-8')
        return aid, title, content

    def parse_examw_item(self, response, cat):
        items = []
        # check if has p tag in html file, 比如211756
        has_paragraph = response.xpath('//div[@id="NewsBox"]/p[descendant-or-self::text()]').extract()
        if len(has_paragraph) > 0:
            item = ArticleItem()
            aid, title, content = self.extract_article(response, has_paragraph)
            item['aid'] = aid
            item['category'] = cat
            item['title'] = title
            item['content'] = content
            items.append(item)
        else:
            content = response.css('#NewsBox::text').extract()
            if content[0].strip():
                item = ArticleItem()
                aid, title, content = self.extract_article(response, content)
                item['aid'] = aid
                item['category'] = cat
                item['title'] = title
                item['content'] = content
                items.append(item)
            else:
                # log innormal article
                #pass
                self.log('"%s" NotParsed' % response.url, level=log.WARNING)
        time.sleep(1)
        return items

    def parse_word(self, response):
        return self.parse_examw_item(response, 'word')

    def parse_excel(self, response):
        return self.parse_examw_item(response, 'excel')

    def parse_powerpoint(self, response):
        return self.parse_examw_item(response, 'powerpoint')
