"""Robot Spider execute file

This file designs a spider for search-engine
"""
import scrapy
import queue
from .. import settings
from urllib.parse import urlparse
from ..execute import pretask
from scrapy import signals


class DistributedSpider(scrapy.Spider):
    name = 'dspider'
    url_queue = queue.Queue()

    def start_requests(self):
        # load start urls from outer files
        url_list = pretask.getURLS(settings.STORAGE_FILE)
        # convert list to queue
        url_queue = pretask.listToQueue(url_list)
        while url_queue.empty() is not True:
            yield scrapy.Request(url=url_queue.get(), callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DistributedSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        # get current domain url
        domain = pretask.getDomain(response.url)
        # extract all non-media href from current page
        link_selectors = response.css('a')
        for selector in link_selectors:
            href = selector.css('a::attr(href)').extract_first()
            text = selector.css('a *::text').extract()
            yield {
                'link': href,
                'text': ''.join(text)
            }

    def spider_closed(self, spider):
        """Custom closed function
        this function will be called when spider will be closed, then url_queue will be clean
        but we need extract data contains in it to url_storage.txt
        """
        spider.logger.info('Dspider has been closed!')
