# DistributedSearch

> this is a distributed mainly based on Elasticsearch and Scrapy, implemented with python3. Our project was built in Centos6.8, so we will write tutorial for this system platform

## What you need in your python3 and your Centos

**For python3**

1. django1.9.5+
2. pyes
3. pybloomfiltermmap3
4. scrapy1.4.0+
5. scrapy_redis

all above these you can use `pip3 install [library name]` to download and install

**For Centos**

1. python3
2. redis3.2.9

## About Distributed Crawler

> we need focus on how to deal with relative links and how to avoid the loop links

**Dealing with Relative Links**: such like these `example.figure.html`, without TLD or DOMAIN, while we can get DOMAIN from the expire url

**Avoiding the loop links**: what I mean is that loop links will allocate our machine's resource and without end

I proposed a naive method (so that we can advance it in the future):
1. using BFS algorithm to walk through our links
2. records the maximum number of sites to visit, or the search's maximum depth (links to links to links)

**Begin crawl with last URLS which had not been visited last time**: as what we think, some URLS had not been visited last time for we terminating them on purpose,
	so we need store them in a file and extract them from file when we start our crawl task next time

## Aditional Attention

> This part will introduce for installing python, redis and so on for Centos6.8, something different with other system version also will be noted in this part. 

**How to install python3 at Centos**
