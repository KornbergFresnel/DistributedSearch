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
from ..items import CrawlerItem


class DistributedSpider(scrapy.Spider):
    name = 'dspider'
    filter_pattern1 = re.compile(pattern='.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf)|(gif))x?$')
    filter_pattern2 = re.compile(pattern='^((javascript:)|(openapi)).+')
    BLOCK_URLS = ""

    def start_requests(self):
        # load start urls from outer files
        url_list = pretask.getURLS(settings.STORAGE_FILE)
        # convert list to queue
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DistributedSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        """This function is mainly do the parsing task,
        we should focus on the depth of BFO and the relative urls,
        when the depth of crawling is over thant the maximum, we block current url, then note it with BLOCK_URLS
        when we meet a relative urls, we check it then bind it with DOMAIN
        """
        # first check whether current depth is maximum, store current url
        if response.meta["depth"] > settings.DEPTH_LIMIT:
            self.BLOCK_URLS += response.url + '\n'
            return
        # get current domain url
        domain = pretask.getDomain(response.url)
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.xpath('/html/head/title/text()').extract_first()

        # extract content from current page, just text content
        tmpContent = response.xpath('/html/body//*/text()').extract()
        item['summary'] = ''
        for ele in tmpContent:
            item['summary'] += ele.strip() + ' '

        yield "Current depth: " + str(response.meta['depth'])

        # extract inner urls from current page, in this part, we need focus on some special urls,
        # such as some resource urls.
        # another problem: some urls maybe relative
        innerURLS = response.xpath('//@href').extract()
        for url in innerURLS:
            if self.illegal(url):
                continue
            if not url.startswith('http://'):
                url = domain + '/' + url
            yield scrapy.Request(url=url, callback=self.parse)

    def spider_closed(self, reason):
        # store before we close our spider completely
        if self.BLOCK_URLS != '':
            self.store()
        self.logger.info('%s data has been store!!!' % len(self.BLOCK_URLS))

    def illegal(self, ori_url):
        """If ori_url is not a visitable url, this function will return true
        """
        return re.match(string=ori_url, pattern=self.filter_pattern1) is not None or re.match(string=ori_url, pattern=self.filter_pattern2) is not None

    def store(self):
        """Store block urls which stoped for depth has over the maximum
        """
        with open(settings.STORAGE_FILE, 'w') as f:
            f.write(self.BLOCK_URLS)
