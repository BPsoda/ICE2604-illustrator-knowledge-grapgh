import json
import pymysql
from elasticsearch import Elasticsearch

es = Elasticsearch()
print(es.ping())

# 需要安装analysis-icu，在/bin目录下运行elastic-plugin install analysis-icu

illusts_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "title": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "url": {
                "type": "keyword",
            },
            "tags": {
                "type": "text",
                "analyzer": "simple"
            },
            "userId": {
                "type": "keyword",
            },
            "createDate": {
                "type": "keyword",
            },
            "bookmark_count": {
                "type": "long",
            }
        }
    }
}

users_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            "userId": {
                "type": "keyword",
            },
            "userName": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "userComment": {
                "type": "keyword",
            },
            "profileImageUrl": {
                "type": "keyword",
            },
            "illusts": {
                "type": "keyword",
            },
            "following": {
                "type": "keyword",
            },
            "following_count": {
                "type": "long",
            },
            "follower": {
                "type": "keyword"
            },
            "follower_count": {
                "type": "long"
            },
            "bg": {
                "type": "keyword"
            }
        }
    }
}

es.indices.create(index='illusts_index', body=illusts_mappings)
es.indices.create(index='users_index', body=users_mappings)

try:
    conn = pymysql.connect(host="101.132.109.217",
                            port=3306,
                            user="ieei",
                            passwd="Diangongdao_B",
                            charset="utf8",
                            db="Final_Homework")
    cursor = conn.cursor()
except:
    print('Fail to connect to the database.')

cursor.execute('SELECT * FROM illusts')
content = cursor.fetchall()

# 导入数据
id=0
for i in content:
    elem = {
        "id": i[0],
        "title": i[1],
        "url": i[7],
        "tags": i[3],
        "userId": i[4],
        "createDate": i[5],
        # "bookmard_count": int(i[6])
    }
    es.index(index="illusts_index", id=id, body=elem)
    id += 1

cursor.execute('SELECT * FROM Users')
content = cursor.fetchall()

id = 0
for i in content:
    elem = {
        "userId": i[0],
        "userName": i[1],
        "userComment": i[2],
        "profileImageUrl": i[3],
        "illusts": i[4],
        "following": i[5],
        "following_count": int(i[6]),
        "follower_count": int(i[8]),
        "bg": i[9]
    }
    es.index(index="users_index", id=id, body=elem)
    id += 1
