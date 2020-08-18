import conf

from pylib.database.dbelasticsearch import DbElasticsearch

DB = 'configuration'
db = conf.db
db.create(DB)


def set(group, name, value):
    if isinstance(value, int):
        db.insert(DB, {'group': group, 'name': name, 'value': str(value)})
    elif isinstance(value, str):
        db.insert(DB, {'group': group, 'name': name, 'value': str(value)})
    elif isinstance(value, list):
        for i, v in enumerate(value):
            db.insert(DB, {'group': group, 'name': name, 'key': 'L%03d' % (i),  'value': str(v)})
    elif isinstance(value, dict):
        for k in value:
            v = value[k]
            db.insert(DB, {'group': group, 'name': name, 'key': str(k), 'value': str(v)})


def get_dict(group, name, default_value={}):
    rows = db.query(DB, {'group': group, 'name': name})
    ret = {}
    for row in rows:
        if 'key' in row and 'value' in row:
            ret[row['key']] = row['value']
    if len(ret.keys()) == 0:
        ret = default_value
    return ret


def get_values(group, name):
    rows = db.query(DB, {'group': group, 'name': name})
    ret = []
    for row in rows:
        if 'value' in row:
            ret.append(row['value'])
    return ret


def get_keys(group, name):
    rows = db.query(DB, {'group': group, 'name': name})
    ret = []
    for row in rows:
        if 'key' in row:
            ret.append(row['key'])
    return ret



def get_key(group, name):
    keys = get_keys(group, name)
    if len(keys) > 0:
        return keys[-1]
    return None


def get_value(group, name):
    values = get_values(group, name)
    if len(values) > 0:
        return values[-1]
    return None


def get_int(group, name, default_value=0):
    value = get_value(group, name)
    try:
        ret = int(value)
    except:
        ret = default_value
    return ret


def get_str(group, name, default_value=''):
    value = get_value(group, name)
    if value is not None:
        ret = value
    else:
        ret = default_value
    return ret


def get_list(group, name, default_value=[]):
    values = get_dict(group, name)
    keys = values.keys()
    ret = None
    if len(keys) > 0:
        keys = list(keys)
        keys.sort()
        ret = [values[key] for key in keys] 

    if ret is None:
        values = get_values(group, name)
        if len(values) > 0:
            ret = values
        else:
            ret = default_value
    return ret


def clear(group, name):
    rows = db.query(DB, {'group': group, 'name': name})

    for row in rows:
        _id = row['_id']
        db.delete(DB, _id)




        
        
