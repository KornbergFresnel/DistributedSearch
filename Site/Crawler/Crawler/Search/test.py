from pyes import *
from search import *


class test:
    def __init__(self):
        self.s = search()

    def test(self):
        self.s.create_index()
        self.s.init_mapping()
        t = self.test_set()
        for item in t:
            self.s.add_item(item)
        ret = search_request("川大", 1)
        for i in ret:
            print(i.title)
            print(i.content)
            print(i.url)

    def test_set(self):
        test_list = []
        item = {}
        item['content'] = "这是我的内容啊什么的不重要。朋友嘛，就要哈哈哈大笑。希望你呢喜欢川大"
        item['title'] = "我的第一篇四川大学博客"
        item['url'] = "wijodajifosdi"
        test_list.append(item)
        return test_list

