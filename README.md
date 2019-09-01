# webTable
本应用运行于Tornado, 用于快速开发表格, 用于共享数据, 快速编辑.
前端的部分主要基于datatables,以及其插件jeditable.

# 环境
安装tornado, ```python -m pip install tornado```

# 运行
运行 ```python main.py```

# 访问
使用浏览器访问 http://127.0.0.1/example/_ . 其中, listprice以及unitcost可以编辑修改其值.
![image.png](https://img.hacpai.com/file/2019/09/image-05b2af80.png)


# 范例
http://127.0.0.1/example/_ 中的 example 即为如下page页面下的example.py. 可参考其中的代码进行客制化.
![image.png](https://img.hacpai.com/file/2019/09/image-3975201a.png)

# 客制化

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.dbelasticsearch import DbElasticsearch
from database.dbdummy import DbDummy

import module.datatables as dt

#db = DbElasticsearch() # 本代码支持使用Elasticsearch
db = DbDummy() # Dummy数据库(使用), 用于调试

DB = 'example' # 数据库名称
db.create(DB) # 如没有数据库, 创建数据库

def html(p0):
    ret = {}

    datatables = {}
    datatables['id'] = 'itemid' # 唯一 field ID, 用于修改数据
    datatables['order'] = [[ 1, "desc" ]] # 默认的排列(第2列, 降序)
    datatables['number'] = True # 支持第1列自动序列
    datatables['scrollY'] = 'window.screen.availHeight' # 是否支持垂直scroll(如不支持, 注释即可), 可用javacript代码, 或者数字(600, 800等).
    #datatables['pageLength'] = 25 #  # 是否支持翻页(如不支持, 注释即可), 支持页面数: 10, 25, 50, 100
    datatables['th'] = [] # 用于列描述
    datatables['th'].append(dt.th('ID', 'itemid', "100px")) # 列宽度为100px, 第1个参数为显示名, 第2参数为Key名称.  
    datatables['th'].append(dt.th('PID', 'productid', "200px"))
    datatables['th'].append(dt.th('Price', 'listprice', "200px", 'edit')) # edit: 可编辑
    datatables['th'].append(dt.th('Cost', 'unitcost', "200px", 'select', ['100', '200'])) # select: 可选择
    datatables['th'].append(dt.th('Attr', 'attr1', "200px"))
    datatables['th'].append(dt.th('Status', 'status'))

    ret['title'] = 'CQ' # Web 标题
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
# 范例 Dummy数据库的内容插入
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

```




