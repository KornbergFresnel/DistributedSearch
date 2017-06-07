from pyes import *
from pyes.mappings import *


SEARCH_INDEX = "dspider"
DOC_TYPE = "search_engine"
PAGE_SIZE = 15


class SearchIndex:
    def __init__(self):
        self.conn = ES('xulight.cn:9200')   # Use HTTP

    def create_index(self, index=SEARCH_INDEX):
        """Create a new index
        """
        self.conn.indices.delete_index_if_exists(index)
        self.conn.indices.create_index(index)

    def init_mapping(self, mapping=None):
        if mapping is None:
            mapping = {
                'content': {
                    'boost': 1.0,
                    'index': 'analyzed',
                    'indexAnalyzer': 'ik',
                    'searchAnalyzer': 'ik',
                    'type': 'string',
                    'term_vector': 'with_positions_offsets',
                    'store': 'yes'
                },
                'title': {
                    'boost': 1.0,
                    'index': 'analyzed',
                    'indexAnalyzer': 'ik',
                    'searchAnalyzer': 'ik',
                    'type': 'string',
                    'term_vector': 'with_positions_offsets',
                    'store': 'yes'
                },
                'url': {
                    'boost': 1.0,
                    'index': 'not_analyzed',
                    'type': 'string',
                    'term_vector': 'with_positions_offsets',
                    'store': 'yes'
                },
                'link': {
                    'boost': 1.0,
                    'index': 'not_analyzed',
                    'type': 'integer',
                    'store': 'yes'
                }
            }
        # self.conn.indices.put_mapping(DOC_TYPE,{'properties':mapping},[SEARCH_INDEX])

    # add new item to our search engine
    def add_item(self, item):
        print("Adding item url %s to our search engine" % item['url'])
        self.conn.index({"content": item['content'], "title": item['title'], "url": item['url'], "link": 0}, SEARCH_INDEX, DOC_TYPE)

    def finish_index(self):
        self.conn.default_indices = [SEARCH_INDEX]
        # self.conn.refresh()  # refresh es


# search function
# def search_request(search_text, up_page=0):
#     conn = ES("xulight.cn:9200", timeout=20)
#     q_title = MatchQuery("title", search_text)
#     q_content = MatchQuery("content", search_text)
#     query = BoolQuery(should=[q_title, q_content])
#     h = HighLighter(['<b>'], ['</b>'])
#     if up_page < 1:
#         up_page = 1
#     s = Search(query, start=(up_page - 1) * PAGE_SIZE, size=PAGE_SIZE, highlight=h)
#     s.add_highlight("title")
#     s.add_highlight("content")
#     resultset = conn.search(s, indices=SEARCH_INDEX)
#     ret_list = []
#     for item in resultset:
#         # has_key() is deprecated, use 'in'
#         if item._meta.highlight.has_key("title"):
#         # if item._meta.highlight.in("title"):
#             item['title'] = item._meta.highlight['title'][0]
#         if item._meta.highlight.has_key("content"):
#         # if item._meta.hightlight.in("content"):
#             item['content'] = item._meta.highlight['content'][0]
#         ret = Item()
#         ret.title = item['title'].encode().decode('utf-8')
#         ret.content = item['content'].encode().decode('utf-8')
#         ret.url = item['url']
#         ret_list.append(ret)
#     return ret_list


class Item:
    def __init__(self):
        self.content = None
        self.title = None
        self.url = None


# s = Search(query,f,)
# example of some query type
def query_demo(self):
    conn = ES("xulight.cn:9200", timeout=20)
    # term query, for numbers, booleans and dates or text
    # it works very fast without calculating the relevant rate
    # it's a kind of accurate query
    tq = TermQuery("field", "value", "boost")

    # bool query, filter the data with these rules.
    # must means the rules must be followed completely
    # must_not means the rules must not be followed completely
    # should means one or more than one of the rulse must be followed.
    bq = BoolQuery("must", "most_not", "should", "boost")
