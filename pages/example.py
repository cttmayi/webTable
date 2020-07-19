#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylib.page.basepage import BasePage

# from pylib.database.dbelasticsearch import DbElasticsearch
from pylib.database.dbdummy import DbDummy

#import module.datatables as dt
import pylib.module.vuetables as dt

import conf

DB = 'example' # 数据库名称
#db = DbElasticsearch() # 本代码支持使用Elasticsearch
db = DbDummy() # Dummy数据库(使用), 用于调试
db.create(DB) # 如没有数据库, 创建数据库


def html(p0, p1):
    ret = {}

    vuetables = {}
    vuetables['name'] = 'app' 
    vuetables['id'] = 'itemid' # 唯一 field ID, 用于修改数据
    vuetables['order'] = {'field': 'itemid', 'order': 'desc'} # 排序，asc/desc
    vuetables['toolbar'] = ['insert', 'delete']
    vuetables['search'] = ['itemid', 'listprice', 'unitcost'] # 搜索范围
    # vuetables['number'] = True # 支持第1列自动序列
    vuetables['height'] = 'window.screen.height*2/3' # 是否支持垂直scroll(如不支持, 注释即可), 可用javacript代码, 或者数字(600, 800等).
    vuetables['th'] = [] # 用于列描述
    vuetables['th'].append(dt.th('ID', 'itemid', "100px")) # 第1个参数为显示名, 第2参数为Key名称. 列宽度为100px, 
    vuetables['th'].append(dt.th('PID', 'productid', "200px"))
    vuetables['th'].append(dt.th('Price', 'listprice', "200px", 'edit')) # edit: 可编辑
    vuetables['th'].append(dt.th('Cost', 'unitcost', "200px", 'select', ['', '100', '200'])) # select: 可选择
    vuetables['th'].append(dt.th('Attr', 'attr1', "200px"))
    vuetables['th'].append(dt.th('Status', 'status'))

    vuetables['summary'] = { 
        'height': '100px', 
        'font-size': '10px' 
    }

    ret['title'] = 'Web' # Web 标题
    ret['vuetables'] = vuetables

    #ret['template'] = 'example'
    return ret


def query(p0, p1):
    data = db.query(DB)

    ret = {
        'text': '<br>'.join(['Show data']*10),
        'data': data
    }

    return ret


def update_thread(p0, p1, db_id, field, value):
    print('update_thread', p0, db_id, field, value)
    body = {
        field: value
    }
    db.update(DB, db_id, body)


def update(p0, p1, db_id, field, value):
    #conf.queue.put(('example', p0, db_id, field, value))
    self.update_thread(p0, db_id, field, value)
    return True


def insert(p0, p1):
    data = {'productid': 'N'}
    db_id = db.insert('example', data)
    data['itemid'] = str(db_id)
    return data


def delete(p0, p1, db_id):
    return db.delete('example', db_id)


##########################################################
# 范例 Dummy数据库的内容插入

def db_insert(db, id, price):
    data = {
        'itemid' : str(id),
        'productid' : 'PD',
        'listprice' : str(price),
        'unitcost' : '200',
        'attr1' : 'A',
        'status' : 'O',
    }
    id = db.insert('example', data, id)

for i in range(2):
    db_insert(db, 'TV.'+str(i), 1000)

