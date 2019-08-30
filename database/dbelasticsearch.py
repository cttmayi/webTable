#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from elasticsearch import Elasticsearch


DB_DOC_TYPE = "news"
HITS = "hits"
SOURCE = "_source"
ID = "_id"

class DbElasticsearch():
    es = Elasticsearch()

    def __init__(self):
        super().__init__()

    def create(self, table_name):
        if not self.es.indices.exists(index=table_name):
            self.es.indices.create(index=table_name)

    def query_id(self, table_name, id):
        res = self.query(table_name, {ID : id})
        if len(res) > 0:
            return res[0][SOURCE]
        return None

    def query(self, table_name, cond=None):
        if cond is None:
            query_body = {
                "query" : {"match_all" : {}}
            }
        else:
            query_body = {
                "query" : {"match" : cond}
            }

        content_list = []
        res_list = self.es.search(index=table_name, doc_type=table_name, body=query_body)[HITS][HITS]
        for res in res_list:
            content = res[SOURCE]
            content_list.append(content)
        return content_list

    def update(self, table_name, id, db_body):
        update_body = {
            'doc': db_body
        }
        self.es.update(index=table_name, doc_type=table_name, id=id, body=update_body)
        self.es.indices.refresh(index=table_name)

    def insert(self, table_name, db_body, id=None):
        if id is None:
            id = self.__get_cur_time()
        self.es.index(index=table_name, doc_type=table_name, id=id, body=db_body)
        self.es.indices.refresh(index=table_name)
        return id

    def delete(self, table_name, id):
        self.es.delete(index=table_name, doc_type=table_name, id=id)
        self.es.indices.refresh(index=table_name)

    def __get_cur_time(self):
        cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return cur_time