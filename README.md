# DistributedSearch

> this is a distributed mainly based on Elasticsearch and Scrapy, implemented with python3

## About Distributed Crawler

> we need focus on how to deal with relative links and how to avoid the loop links

**Dealing with Relative Links**: such like these `example.figure.html`, without TLD or DOMAIN, while we can get DOMAIN from the expire url

**Avoiding the loop links**: what I mean is that loop links will allocate our machine's resource and without end

I proposed a naive method (so that we can advance it in the future):
1. using BFS algorithm to walk through our links
2. records the maximum number of sites to visit, or the search's maximum depth (links to links to links)
