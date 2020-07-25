#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf

if conf.configuration:

    from pylib.database.dbelasticsearch import DbElasticsearch
    import pylib.configuration.configuration as configuration

    DB = 'configuration'
    db = DbElasticsearch()
    db.create(DB)


    def html(p0, p1):
        ret = {}

        vuetables = {}

        vuetables['id'] = '_id'
        vuetables['toolbar'] = ['insert', 'delete']

        vuetables['height'] = 'window.innerHeight - 50'

        options = ['']
        options.extend(configuration.TYPES)

        vuetables['th'] = [
        {'name': 'Group', 'field': 'group', 'width': '200', 'editor': 'edit', 'fixed': 'left'},
        {'name': 'Type', 'field': 'type', 'width': '200', 'editor': 'select', 'fixed': 'left',
            'options': options},
        {'name': 'Name', 'field': 'name', 'width': '200', 'editor': 'edit', 'fixed': 'left'},
        {'name': 'Key', 'field': 'key', 'width': '200', 'editor': 'edit'},
        {'name': 'Value', 'field': 'value', 'width': '200', 'editor': 'edit'},
        {'name': 'Comment', 'field': 'commnet', 'width': '*', 'editor': 'edit'},
        ]

        ret['title'] = 'Configuration'
        ret['vuetables'] = vuetables

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



