"""Robot Spider execute file

This file designs a spider for search-engine
"""
import scrapy
import queue
import re
from .. import settings
from urllib.parse import urlparse
from ..execute import pretask
from scrapy import signals
from scrapy.selector import HtmlXPathSelector
from items import CrawlerItem


class DistributedSpider(scrapy.Spider):
    name = 'dspider'
    url_queue = queue.Queue()
    filter_pattern1 = re.compile(pattern='.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf))x?$')
    filter_pattern2 = re.compile(pattern='^((javascript:)|(openapi)).+')

    def start_requests(self):
        # load start urls from outer files
        url_list = pretask.getURLS(settings.STORAGE_FILE)
        # convert list to queue
        url_queue = pretask.listToQueue(url_list)
        while url_queue.empty() is not True:
            yield scrapy.Request(url=url_queue.get(), callback=self.parse)

    def parse(self, response):
        # get current domain url
        domain = pretask.getDomain(response.url)
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.xpath('/html/head/title/text()').exract_first()

        # extract content from current page, just text content
        tmpContent = response.xpath('/html/body//*/text()').extract()
        for ele in tmpContent:
            item['summary'] += ele.strip() + ' '

        yield item  # accepted by pipeline

        # extract inner urls from current page, in this part, we need focus on some special urls,
        # such as some resource urls.
        # another problem: some urls maybe relative
        innerURLS = response.xpath('//@href').extract()
        for url in innerURLS:
            if self.illegal(url):
                continue
            if not url.startwith('http://'):
                url = domain + url
            yield scrapy.Request(url=url, callback=self.parse)

    def illegal(self, ori_url):
        return re.match(str=ori_url, pattern=self.filter_pattern1) and re.match(str=ori_url, pattern=self.filter_pattern2)
