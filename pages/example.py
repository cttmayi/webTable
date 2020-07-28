#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf


DB = 'example' # 数据库名称
db = conf.db
init = db.create(DB) # 如没有数据库, 创建数据库


def html(p0, p1):
    ret = {}

    vuetables = {}
    # vuetables['name'] = 'app' 
    vuetables['id'] = 'itemid' # 唯一 field ID, 用于修改数据
    vuetables['default_sort'] = {'field': 'itemid', 'order': 'desc'} # 排序，asc/desc
    vuetables['toolbar'] = ['insert', 'delete', 'export'] # 配置 Toolbar 按钮
    vuetables['height'] = 'window.innerHeight - 150' # '700' # 设定表格高度, 可用javacript代码, 或者字符串('600'等).


    vuetables['th'] = [
        {'name': 'ID', 'field': 'itemid', 'width': '100', # name为显示名, field为Key名称. width为100,
            'fixed': 'left'}, # fixed 表示是否固定
        {'name': 'EXT', 'field': 'productid', 'width': '50', 
            'extend': {'value': '{[ row.listprice ]}'}
        },

        {'name': 'PID', 'field': 'productid', 'width': '200',
            'editor': 'select', 'options': [
                { 'label': '', 'value': '' }, # label为选项显示名称， value为保存数据 
                { 'label': '产品1', 'value': 'P1' }, 
                { 'label': '产品2', 'value': 'P2' }, 
                { 'label': '产品3', 'value': 'P3' }, 
            ],},
        {'name': 'Price', 'field': 'listprice', 'width': '200', 'editor': 'edit',
            'tooltip': 'unitcost'},
        {'name': 'Cost', 'field': 'unitcost', 'width': '200',
            'editor': 'select', 'options': ['', '100', '200', '300'], # Options 简洁表达方式，lable和value一致
            'style': [{'cond': "row.unitcost > 150", 'style': 'bg-green'}]},
        {'name': 'Status', 'field': 'status', 'width': '*', 'editor': 'textarea', 
            'search': 'false'}, # 字段默认可搜索， 设定不可搜索（'search': 'false'）
    ]


    vuetables['summary'] = { 
        'height': '100px', 
        'font-size': '10px' 
    }

    vuetables['computed'] = {'name': '成本: ', 'field': 'unitcost', 'method': 'float'} # 计算求和显示

    vuetables['row_style'] = [
        {'cond': "row.listprice < 700", 'style': 'bg-red'} # 行颜色条件设定
    ]

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
    print('update_thread', p0, p1, db_id, field, value)
    body = {
        field: value
    }
    db.update(DB, db_id, body)


def update(p0, p1, db_id, field, value):
    #conf.queue.put(('example', p0, p1, db_id, field, value))
    update_thread(p0, p1, db_id, field, value)
    return value


def insert(p0, p1):
    data = {}
    db_id = db.insert(DB, data)
    db.update(DB, db_id, {'itemid': db_id})

    data['itemid'] = db_id
    return data


def delete(p0, p1, db_id):
    return db.delete('example', db_id)


##########################################################
# 范例 Dummy数据库的内容插入
if init:
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
    db_insert(db, 'TVD', 300)
