# _*_ coding: utf-8 _*_

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
from scrapy.selector import Selector

from officedaren.items import ArticleItem


class WordArticleSpider(CrawlSpider):
    name = "wordcrawler"
    #allowed_domains = ["examw.com"]
    #start_urls = ['http://www.examw.com/oa/word/']
    allowed_domains = ["officezu.com"]
    start_urls = ['http://www.officezu.com/word/2003']

    rules = (
        Rule(lxml(allow=('/a/word/\d+.html$', )), callback='parse_item'),
        Rule(lxml(allow=('/word/2003/index\d+.html$', )), follow=True),
        #Rule(lxml(allow=('/oa/word/\d+/?$', )), callback='parse_2'),
        #Rule(lxml(allow=('/oa/word/indexA\d+.html$', )), follow=True),
    )

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        sites = sel.

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('#News')
        for site in sites:
            item = ArticleItem()
            item['title'] = site.css('.title h3::text').extract()
            item['content'] = site.css('#NewsBox::text').extract()
            item['category'] = 'word'
            #print item['title'], item['content']
            items.append(item)
        return items
