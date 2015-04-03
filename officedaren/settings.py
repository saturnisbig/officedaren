# -*- coding: utf-8 -*-

# Scrapy settings for officedaren project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'officedaren'

SPIDER_MODULES = ['officedaren.spiders']
NEWSPIDER_MODULE = 'officedaren.spiders'

ITEM_PIPELINES = {
  #'officedaren.pipelines.JsonPipeline': 300,
  'officedaren.pipelines.SQLiteStorePipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'officedaren (+http://www.yourdomain.com)'

LOG_FILE = 'log.txt'
