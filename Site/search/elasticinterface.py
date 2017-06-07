from pyes import *


# search function
def search_request(search_text, up_page=0):
    conn = ES("xulight.cn:9200", timeout=20)
    q_title = MatchQuery("title", search_text)
    q_content = MatchQuery("content", search_text)
    query = BoolQuery(should=[q_title, q_content])
    h = HighLighter(['<b>'], ['</b>'])
    if up_page < 1:
        up_page = 1
    s = Search(query, start=(up_page - 1) * PAGE_SIZE, size=PAGE_SIZE, highlight=h)
    s.add_highlight("title")
    s.add_highlight("content")
    resultset = conn.search(s, indices=SEARCH_INDEX)
    ret_list = []
    for item in resultset:
        # has_key() is deprecated, use 'in'
        if item._meta.highlight.has_key("title"):
        # if item._meta.highlight.in("title"):
            item['title'] = item._meta.highlight['title'][0]
        if item._meta.highlight.has_key("content"):
        # if item._meta.hightlight.in("content"):
            item['content'] = item._meta.highlight['content'][0]
        ret = Item()
        ret.title = item['title'].encode().decode('utf-8')
        ret.content = item['content'].encode().decode('utf-8')
        ret.url = item['url']
        ret_list.append(ret)
    return ret_list


class Item:
    def __init__(self):
        self.content = None
        self.title = None
        self.url = None
