# simpysql

A lightweight mysql orm based on pymysql

## Sample Code

```python
ModelDemo().where('id', 4).select('id', 'name').take(5).get()
```

# Content

- [Installation](#installation)
- [Initialization](#initialization)
- [Create Model](#create-model)
- [Create](#create)
    - [One Data](#one-data)
    - [Multi Data](#multi-data)
    - [Get Lastid](#get-lastid)
- [Update](#update)
    - [Update Data](#update-data)
    - [Increament](#increament)
    - [Decreament](#decreament)
- [Delete](#delete)
- [Select](#select)
    - [Select One Data](#select-one-data)
    - [Select Multi Data](#select-multi-data)
    - [Select Condition](#select-condition)
    - [Select Multi Condition](#select-multi-condition)
    - [Select Order](#select-order)
    - [Select Offset](#select-offset)
    - [Select Columns](#select-columns)
    - [Select Groupby](#select-groupby)
    - [Original SQL](#original-sql)
    - [Response](#response)
- [Transaction](#transaction)
- [Database](#database)
- [Log](#log)
- [Authors](#authors)


# Installation

```
pip install simpysql
```

# Initialization

you need to create a .env file at your project root path, and content as follows:

``` python
[default]
DB_HOST=127.0.0.1                              
DB_PORT=3306                                    
DB_NAME=test_db1                                
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
LOG_DIR=/home/logs/python/                      #open sql log

[test_db2]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db2
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
#LOG_DIR=/home/logs/python/                     #close sql log
```

## Create Model
Create your Model extend DBModel as follows:

``` python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from simpysql.DBModel import DBModel

class ModelDemo(DBModel):
    __basepath__ = '/home/project/'             # .env file path
    #__database__ = 'default'                   # database
    __tablename__ = 'lh_test'                   # table name
    __create_time__ = 'create_time'             # it will be ignore if set None(default value: int(time.time()))
    __update_time__ = 'update_time'             # it will be ignore if set None(default value: int(time.time()))
    columns = [                                 # table columns
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]

    # set time format of create_time and update_time
    # def fresh_timestamp(self):
    #     return datetime.datetime.now().strftime("%Y%m%d")
```


# Create

## One Data
``` python
ModelDemo().create({'name': "haha1", 'token_name': 'haha124'})
```

## Multi Data
``` python
ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name':"haha2", 'token_name': 'haha125'}])
```

## Get Lastid
``` python
id = ModelDemo().create({'name': "haha1", 'token_name': 'haha124'}).lastid()
```

# Update

## Update Data
``` python
ModelDemo().where('id', 1).update({'name':"hehe", 'token_name': 'hehe123'})
```

## Increment
``` python
ModelDemo().where('id', 1).increment('status')        #status increment by 1
ModelDemo().where('id', 1).increment('status', 5)     #status increment by 5
```

## Decrement
``` python
ModelDemo().where('id', 1).decrement('status')        #status decrement by 1
ModelDemo().where('id', 1).decrement('status', 5)     #status decrement by 5
```

# Delete
``` python
ModelDemo().where('id', 4).delete()
```

## Select

### Select One Data
``` python
# sql: select * from lh_test where id = 4 limit 1
data = ModelDemo().where('id', 4).first()
data = ModelDemo().where('id', '=', 4).first()
return data: {'id':4, 'name':...}
```

### Select Multi Data
``` python
# sql: select * from lh_test where id > 4 limit 5
data = ModelDemo().where('id', '>', 4).take(5).get()
return data: [{'id':5, 'name':...},{}...]
```

### Select Condition
``` python
# sql: select * from lh_test where id >= 4
data = ModelDemo().where('id', '>=', 4).get()

# sql: select * from lh_test where id > 4
data = ModelDemo().where('id', '>', 4).get()

# sql: select * from lh_test where id < 4
data = ModelDemo().where('id', '<', 4).get()

# sql: select * from lh_test where id <= 4
data = ModelDemo().where('id', '<=', 4).get()

# sql: select * from lh_test where id != 4
data = ModelDemo().where('id', '!=', 4).get()

# sql: select * from lh_test where id in (1,2)
data = ModelDemo().where('id', 'in', [1, 2]).get()

# sql: select * from lh_test where id not in (1,2)
data = ModelDemo().where('id', 'not in', [1, 2]).get()

# sql: select * from lh_test where id between (1,2)
data = ModelDemo().where('id', 'between', [1, 2]).get()

# sql: select * from lh_test where id not between (1,2)
data = ModelDemo().where('id', 'not between', [1, 2]).get()

# sql: select * from lh_test where name like '%Tether%'
data = ModelDemo().where('name', 'like', '%Tether%').get()

# sql: select * from lh_test where name not like '%Tether%'
data = ModelDemo().where('name', 'not like', '%Tether%').get()

# sql: select * from lh_test where `id`=62 or `name`='haha'
data = ModelDemo().where('id', 62).orwhere('name', 'haha').get()

# sql: select * from lh_test where `id`=62 or `name` like 'haha%'
data = ModelDemo().where('id', 62).orwhere('name', 'like', 'haha%').get()

# sql: select * from lh_test where `id`=62 or (`name` like 'haha%' and `create_time` < 1555123210)
data = ModelDemo().where('id', 62).orwhere([['name', 'like', 'haha%'], ['create_time', '<', 1555123210]]).get()

```

### Select Multi Condition
``` python
# sql:select * from lh_test where id=1 and name='hehe'
data = ModelDemo().where({'id': 1, 'name': 'hehe'}).get()

# sql:select * from lh_test where id=1 and name like 'hehe%'
data = ModelDemo().where('id', 1).where('name', 'like', 'hehe%').get()
```

### Select Order
``` python
# sql: select * from lh_test where `id` > 0 order by `id` desc,`status`
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status').get()
```

### Select Offset
``` python
# sql: select * from lh_test where id > 100 limit 5 offset 10
data = ModelDemo().where('id', '>', 100).offset(10).take(5).get()
```

### Search Colums
``` python
# sql: select `id`,`name` from lh_test limit 5
data = ModelDemo().select('id', 'name').take(5).get()

# 对应sql: select min(id) as minid from lh_test limit 1
data = ModelDemo().select('min(id) as minid').first()
```

### Select Groupby
``` python
# sql: select count(*) as num,`name` from lh_test group by `name`
data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()
```

### Original SQL
``` python
sql = 'select count(*) as num,name from lh_test group by name'
data = ModelDemo().execute(sql)
```

# Response
``` python
data = ModelDemo().where('id', '=', 1).select('id').first()                             # {'id':1}
data = ModelDemo().where('id', '=', 1).select('id').get()                               # [{'id':1}]
data = ModelDemo().where('id', 'in', [1,2,3]).select('id', 'name').lists('id')          # [1,2,3]
data = ModelDemo().where('id', 'in', [1,2]).select('id', 'name').lists(['id', 'name'])  # [[1,'name1'],[2,'name2']]
data = ModelDemo().select('id', 'name', 'status').data()                                # return pandas DataFrame
```

# Transaction
``` python
def demo():
    ModelDemo().where('id', 42).update({'name': "44", 'token_name': '444'})
    ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    return True
data = ModelDemo().transaction(demo)
```

# Database

``` python
set ModelDemo attribute as follow:
__database__ = 'test_db2'

set database in your code:
ModelDemo().database('test_db2').where('id', '>', 40).first()
```

# Log
``` python
set LOG_DIR in your .env file:
LOG_DIR=/home/logs/python/
```
