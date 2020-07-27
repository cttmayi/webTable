from pylib.database.dbdummy import DbDummy
from pylib.database.dbelasticsearch import DbElasticsearch

debug = True

port = 80

site = '' #'web/'

queue = False

#db = DbElasticsearch() # 本代码支持使用Elasticsearch
db = DbDummy() # Dummy数据库(使用), 用于调试