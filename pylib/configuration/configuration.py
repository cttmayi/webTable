
from pylib.database.dbelasticsearch import DbElasticsearch

DB = 'configuration'
db = DbElasticsearch()
db.create(DB)


INT = 'int'
STR = 'str'
LIST = 'list'
DICT = 'dict'

TYPES = [ INT, STR, LIST, DICT ]

def get(group, name, _type, default=None):
    rows = db.query(DB, {'group': group, 'name': name, 'type': _type})

    ret = default

    try:
        if _type == INT:
            ret = int(rows[-1]['value'])

        elif _type == STR:
            if 'value' in rows[-1]:
                ret = rows[-1]['value']
            else:
                ret = ''
        elif _type == LIST:
            ret = []
            for row in rows:
                if 'value' in row: 
                    ret.append(row['value'])
        elif _type == DICT:
            ret = {}
            for row in rows:
                # print('dict row:', row)
                if 'key' in row and 'value' in row:
                    ret[row['key']] = row['value']
    except:
        #print('configuration.get error', rows)
        pass

    return ret


def set(group, name, value):
    if isinstance(value, int):
        db.insert(DB, {'group': group, 'name': name, 'type': INT, 'value': str(value)})
    elif isinstance(value, str):
        db.insert(DB, {'group': group, 'name': name, 'type': STR, 'value': str(value)})
    elif isinstance(value, list):
        for v in value:
            db.insert(DB, {'group': group, 'name': name, 'type': LIST, 'value': str(v)})
    elif isinstance(value, dict):
        for k in value:
            v = value[k]
            db.insert(DB, {'group': group, 'name': name, 'type': DICT, 'key': str(k), 'value': str(v)})


def clear(group, name, _type):
    rows = db.query(DB, {'group': group, 'name': name, 'type': _type})

    for row in rows:
        _id = row['_id']
        db.delete(DB, _id)




        
        
