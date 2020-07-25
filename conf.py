from pylib.database.dbdummy import DbDummy

debug = True

port = 80

site = '' #'web/'

queue = False

configuration = True

#db = DbElasticsearch() # 本代码支持使用Elasticsearch
db = DbDummy() # Dummy数据库(使用), 用于调试