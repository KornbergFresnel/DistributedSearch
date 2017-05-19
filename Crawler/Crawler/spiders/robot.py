"""Robot Spider execute file

This file designs a spider for search-engine
"""
import scrapy
import queue
from .. import settings
from urllib.parse import urlparse
from ..execute import pretask


class DistributedSpider(scrapy.Spider):
    name = 'dspider'
    url_queue = queue.Queue()

    def start_requests(self):
        # load start urls from outer files
        url_list = pretask.getURLS(settings.SOTRE_FILE)
        # convert list to queue
        url_queue = pretask.listToQueue(url_list)
        while url_queue.empty() is not True:
            yield scrapy.Request(url=url_queue.get(), callback=self.parse)

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

    def close(self, reason):
        yield 'This is my Reason'
        super.close(reason)
