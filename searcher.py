from elasticsearch import Elasticsearch
import json

class Searcher:
    def __init__(self) -> None:
        self.es = Elasticsearch()

    def search(self, key, method):
        ''' 搜索，返回一个由字典组成的列表结果。
        若没有满足条件返回None。
        method可以为 id, title, tags, userId, userName。
        当选取前三个时返回的是插画，选取后两个时返回的是画师'''
        searchQuery = {
            'query': {
                'match': {
                    method: key
                }
            }
        }
        if method in ['id', 'title', 'tags']:
            result = self.es.search(index="illusts_index", body=searchQuery)
            return result['hits']['hits']
        elif method in ['userId', 'userName']:
            result = self.es.search(index='users_index', body=searchQuery)
        else:
            print('No match result!')
            return None

# if __name__ == '__main__':
#     se = Searcher()
#     result = se.search(22646094, 'id')
#     print(json.dumps(result[0], indent=2, separators=(',', ';')))