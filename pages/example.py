#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.dbelasticsearch import DbElasticsearch
from database.dbdummy import DbDummy



#db = DbElasticsearch()
db = DbDummy()

DB = 'example'
db.create(DB)


def th(name, field, width='*', editor='text', data=[]):
    map_data = {}
    for d in data:
        map_data[d] = d

    return {'name': name, 'field': field, 'editor': editor, 'data': str(map_data)}

def html(p0):
    ret = {}

    datatables = {}
    datatables['title'] = 'T'
    datatables['id'] = 'itemid'
    datatables['th'] = []
    datatables['th'].append(th('itemid', 'itemid', 100))
    datatables['th'].append(th('productid', 'productid', 100))
    datatables['th'].append(th('listprice', 'listprice', 100, 'edit'))
    datatables['th'].append(th('unitcost', 'unitcost', 100, 'select', ['100', '200']))
    datatables['th'].append(th('attr1', 'attr1', 100))
    datatables['th'].append(th('status', 'status'))

    ret['title'] = 'CQ'
    ret['datatables'] = datatables

    #ret['template'] = 'example'
    #ret['th'] = _table_th()
    return ret




def query(p0):
    ret = db.query(DB)

    return ret

def update(p0, id, field, value):
    body = {
        field: value
    }

    db.update(DB, id, body)
    return True



##########################################################

def insert(db, id, price):
    data = {
        'itemid' : str(id),
        'productid' : 'PD',
        'listprice' : str(price),
        'unitcost' : '200',
        'attr1' : 'A',
        'status' : 'O',
    }

    id = db.insert('example', data, id)


for i in range(100):
    insert(db, 'TV.'+str(i), 1000)

