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
# from pybloomfilter import BloomFilter
from . import settings
from scrapy.exceptions import DropItem
from Crawler.Search import search


class CrawlerPipeline(object):
    """This pipeline class object is designed for ElasticSearch client
    """
    def __init__(self):
        # self.filter = BloomFilter(100000000, 0.01, 'filter.bloom')
        # self.storage = open(settings.TMP_STORAGE_FILE, 'w')
        self.searchIndex = search.SearchIndex()
        self.searchIndex.init_mapping()

    def process_item(self, item, spider):
        if self.filter.add(item['url']):
            raise DropItem("Duplicated item founded: %s" % item['url'])
        else:
            self.storage.write(str(item) + '\n')
            return item
        self.storage.writes(str(item) + '\n')
        self.searchIndex.add_item(item)
        return item

    def __del__(self):
        # self.storage.close()
        self.searchIndex.finish_index()
