# _*_ coding: utf-8 _*_

import re
import urllib2
import time
import os

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
#from scrapy.selector import Selector

from officedaren.items import ArticleItem


SITE_NAME = 'http://www.officedaren.com'

class WordArticleSpider(CrawlSpider):
    name = "examw.com"
    allowed_domains = ["examw.com"]
    start_urls = ['http://www.examw.com/oa/word/']
    #allowed_domains = ["officezu.com"]
    #start_urls = ['http://www.officezu.com/word/2003']
                  #'http://www.officezu.com/word/jiqiao']

    rules = (
        #Rule(lxml(allow=('/a/word/\d{3}.html$', )), callback='parse_item'),
        #Rule(lxml(allow=('/word/2003/index\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/word/jiqiao/index\d+.html$', )), follow=True),
        Rule(lxml(allow=('/oa/word/\d+/?$', )), callback='parse_2'),
        #Rule(lxml(allow=('/oa/word/indexA\d+.html$', )), follow=True),
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


    def parse_2(self, response):
        items = []
        content = response.css('#NewsBox::text').extract()
        if content[0].strip():
            item = ArticleItem()
            item['aid'] = response.url.split('/')[-2]
            item['title'] = response.css('#News h3::text').extract()[0]
            item['content'] = ''.join(content)
            #item['category'] = 'word'
            #print item['title'], item['content']
            items.append(item)
        else:
            # log innormal article
            pass
        return items
