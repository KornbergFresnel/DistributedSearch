# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# we use pipeline do these tasks
# 1. cleansing HTML data
# 2. validating scraped data (checking that the items contain certain fields)
# 3. checking for duplicates (and dropping them)
# 4. storing the scraped item in a database
import json
from scrapy import signals
from pybloomfilter import BloomFilter
from . import settings
from scrapy.exceptions import DropItem


class CrawlerPipeline(object):
    def __init__(self):
        """Initialize the BloomFilter tool
        """
        # self.filter = BloomFilter(100000000, 0.01, 'filter.bloom')
        self.storage = open(settings.TMP_STORAGE_FILE, 'w')

    def process_item(self, item, spider):
        # if self.filter.add(item['url']):
        #     raise DropItem("Duplicated item founded: %s" % item['url'])
        # else:
        #     self.storage.write(str(item) + '\n')
        #     return item
        self.storage.writes(str(item) + '\n')
        return item

    def __del__(self):
        self.storage.close()
