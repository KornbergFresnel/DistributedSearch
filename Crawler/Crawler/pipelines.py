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


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
