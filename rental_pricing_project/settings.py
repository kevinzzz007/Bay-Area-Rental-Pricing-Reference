# -*- coding: utf-8 -*-

# Scrapy settings for rental_pricing_project project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rental_pricing_project'

SPIDER_MODULES = ['rental_pricing_project.spiders']
NEWSPIDER_MODULE = 'rental_pricing_project.spiders'

ITEM_PIPELINES = ['rental_pricing_project.pipelines.MongoDBPipeline', ]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "rental_pricing"
MONGODB_COLLECTION = "partial_links"

DOWNLOAD_DELAY = 20


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rental_pricing_project (+http://www.yourdomain.com)'
