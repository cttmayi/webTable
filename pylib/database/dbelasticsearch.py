#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from elasticsearch import Elasticsearch


DB_DOC_TYPE = "news"
HITS = "hits"
SOURCE = "_source"
ID = "_id"

es = Elasticsearch(maxsize=25)

class DbElasticsearch():
    

    def __init__(self):

        super().__init__()

    def create(self, table_name):
        if not es.indices.exists(index=table_name):
            es.indices.create(index=table_name)

    def query_id(self, table_name, id):
        res = self.query(table_name, {ID : id})
        if len(res) > 0:
            return res[0]
        return None

    def query(self, table_name, conds, from_=0, size=10000):
        es.indices.refresh(index=table_name)
        query_body = {
            "query" : {
                "bool": {
                    "must":[]
                }
            }
        }

        for key in conds.keys():
            cond = conds[key]
            query_body['query']['bool']['must'].append({'match': {key: cond}})

        res_list = es.search(index=table_name, body=query_body, from_=from_, size=size)[HITS][HITS]
        return self._to_list(res_list)

    def query_all(self, table_name):
        es.indices.refresh(index=table_name)

        query_body = {
            'query' : {"match_all" : {}},
        }

        res_list = es.search(index=table_name, body=query_body, from_=0, size=10000)[HITS][HITS]
        return self._to_list(res_list)
    
    @staticmethod
    def _to_list(res_list):
        content_list = []
        for res in res_list:
            content = res[SOURCE]
            content[ID] = (res[ID])
            content_list.append(content)
        return content_list

    def update(self, table_name, id, db_body):
        update_body = {
            'doc': db_body
        }
        es.update(index=table_name, id=id, body=update_body)


    def insert(self, table_name, db_body, id=None):
        if id is None:
            id = es.index(index=table_name,  body=db_body)[ID]
        else:
            es.index(index=table_name,  id=id, body=db_body)
        es.indices.refresh(index=table_name)
        return id

    def delete(self, table_name, id):
        try:
            return es.delete(index=table_name, id=id)
        except:
            return None


    def refresh(self, table_name):
        es.indices.refresh(index=table_name)

    # def __get_cur_time(self):
        # cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # return cur_time