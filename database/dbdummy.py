#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DbDummy():
    def __init__(self):
        super().__init__()

    def create(self, table_name):
        self.__contents__ = {}
        self.__contents__[table_name] = {}


    def query_id(self, table_name, id):
        contents = self.__contents__[table_name]
        if id in contents:
            return contents[id]
        return None


    def query(self, table_name, cond=None):
        contents = self.__contents__[table_name]
        ret = []
        for k in contents.keys():
            content = contents[k]
            ret.append(content)
        return ret


    def update(self, table_name, id, db_body):
        contents = self.__contents__[table_name]
        if id in contents:
            content = contents[id]
            for u in db_body:
                content[u] = db_body[u]
            return True
        return False


    def insert(self, table_name, db_body, id=None):
        contents = self.__contents__[table_name]
        contents[id] = db_body


    def delete(self, table_name, id):
        contents = self.__contents__[table_name]
        if id in contents:
            del contents[id]