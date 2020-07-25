#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf

if conf.configuration:

    from pylib.database.dbelasticsearch import DbElasticsearch


    import pylib.module.vuetables as dt
    import pylib.configuration.configuration as configuration



    DB = 'configuration'
    db = DbElasticsearch()
    db.create(DB)


    def html(p0, p1):
        ret = {}

        vuetables = {}

        vuetables['id'] = '_id'
        vuetables['toolbar'] = ['insert', 'delete']
        vuetables['search'] = ['name']
        vuetables['fixed'] = {'left': 3}

        vuetables['height'] = 'window.innerHeight - 50'
        vuetables['th'] = []
        vuetables['th'].append(dt.th('Group', 'group', "200px", 'edit'))

        type_list = ['']
        type_list.extend(configuration.TYPES)

        vuetables['th'].append(dt.th('Type', 'type', "100px", 'select', type_list))
        vuetables['th'].append(dt.th('Name', 'name', "200px", 'edit'))
        vuetables['th'].append(dt.th('Key/Index', 'key', "200px", 'edit'))
        vuetables['th'].append(dt.th('Value', 'value', "200px", 'edit'))
        vuetables['th'].append(dt.th('Comment', 'commnet', '*', 'edit'))

        ret['title'] = 'Configuration'
        ret['vuetables'] = vuetables

        #ret['template'] = 'example'
        return ret


    def query(p0, p1):
        data = db.query_all(DB)

        ret = {
            'data': data
        }

        return ret


    def update(p0, p1, db_id, field, value):
        body = {
            field: value
        }
        db.update(DB, db_id, body)
        return value


    def insert(p0, p1):
        data = {}
        db_id = db.insert(DB, data)


        data['_id'] = db_id
        return data


    def delete(p0, p1, db_id):
        return db.delete(DB, db_id)



