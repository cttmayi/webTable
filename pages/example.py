#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.dbelasticsearch import DbElasticsearch
from database.dbdummy import DbDummy

import module.datatables as dt


#db = DbElasticsearch()
db = DbDummy()

DB = 'example'
db.create(DB)


def html(p0):
    ret = {}

    datatables = {}
    datatables['id'] = 'itemid'
    datatables['order'] = [[ 1, "desc" ]]
    datatables['number'] = True
    datatables['scrollY'] = 'window.screen.availHeight'
    #datatables['pageLength'] = 25 # 10, 25, 50, 100
    datatables['th'] = []
    datatables['th'].append(dt.th('itemid', 'itemid', "100px"))
    datatables['th'].append(dt.th('productid', 'productid', "200px"))
    datatables['th'].append(dt.th('listprice', 'listprice', "200px", 'edit'))
    datatables['th'].append(dt.th('unitcost', 'unitcost', "200px", 'select', ['100', '200']))
    datatables['th'].append(dt.th('attr1', 'attr1', "200px"))
    datatables['th'].append(dt.th('status', 'status'))

    ret['title'] = 'CQ'
    ret['datatables'] = datatables

    #ret['template'] = 'example'
    return ret




def query(p0):
    ret = db.query(DB)

    return ret

def update(p0, db_id, field, value):
    body = {
        field: value
    }

    db.update(DB, db_id, body)
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

