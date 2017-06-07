"""Robot Spider execute file

This file designs a spider for search-engine
"""
import scrapy
import queue
import re
from urllib.parse import urlparse
from scrapy import signals
from scrapy.selector import HtmlXPathSelector
from Crawler.items import CrawlerItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class DistributedSpider(RedisCrawlSpider):
    """Spider that reads urls from redis queue(dspider:start_urls)."""
    name = 'dspider'
    redis_key = "dspider:start_urls"

    rules = (
        # follow links
        Rule(LinkExtractor(tags=('a',), attrs=('href',), unique=True), callback="parse_page", follow=True),
    )

    # start_urls = ['http://jwc.scu.edu.cn/jwc/frontPage.action']

    def __init__(self, *args, **kwargs):
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(DistributedSpider, self).__init__(*args, **kwargs)

    def parse_page(self, response):
        """This function is mainly do the parsing task,
        we should focus on the depth of BFO and the relative urls,
        when the depth of crawling is over thant the maximum, we block current url, then note it with BLOCK_URLS
        when we meet a relative urls, we check it then bind it with DOMAIN
        """
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.xpath('/html/head/title/text()').extract_first()

        # extract content from current page, just text content
        tmpContent = response.xpath('/html/body//*/text()').extract()
        item['content'] = ''
        for ele in tmpContent:
            item['content'] += ele.strip() + ' '
        item['content'] = item['content'][:116]

        yield {'url': item['url'], 'name': item['title']}
        return item
