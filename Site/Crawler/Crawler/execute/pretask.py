"""Pretask execute file

This file list some functions which designed for executing some pretask, such as:
    1. load web urls from outer file which store the urls last visit time, in the future, it will be
        distributed to all slave machines
    2. others, I cannot propose any at this time, hahah~
"""
import queue
from urllib.parse import urlparse


def getURLS(filename):
    content, res_list = None, None
    with open(filename, 'r') as f:
        content = f.read()
    if content is not None:
        # convert str-like data to list
        res_list = content.split('\n')[:-1]
    return res_list


def listToQueue(original):
    """Convert list structure to Queue
    """
    que = queue.Queue()
    for ele in original:
        que.put(ele)
    return que


def getDomain(url):
    """Get domain from a absolute url, this function designed for solve the relative links
    """
    parse_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parse_url)
    return domain
