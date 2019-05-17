# hangsql

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
- [FAQ](#faq)
- [To Do](#to-do)


# Installation

```
pip install hangsql
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
LOG_DIR=/home/logs/python/

[test_db2]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db2
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
LOG_DIR=/home/logs/python/
```

## Create Model
Create your Model extend DBModel as follows:

``` python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from hangsql.DBModel import DBModel

class ModelDemo(DBModel):
    __basepath__ = '/home/project/'             # 项目根目录 (.env文件路径:/home/project/.env)
    #__database__ = 'default'                   # 库名
    __tablename__ = 'lh_test'                   # 表名
    __create_time__ = 'create_time'             # 插入时间字段 如果该字段为None create_time则不会自动添加 默认值当前时间戳(单位:秒)
    __update_time__ = 'update_time'             # 更新时间字段 如果该字段为None update_time则不会自动添加 默认值当前时间戳(单位:秒)
    columns = [                                 # 数据库字段
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]

    # 获取时间格式(如果想修改create_time, update_time 时间格式，重写该方法即可)
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
``` bash
ModelDemo().where('id', 4).delete()
```

## Select

#单个查询
``` bash
# 对应sql: select * from lh_test where id = 4 limit 1
data = ModelDemo().where('id', 4).first()
data = ModelDemo().where('id', '=', 4).first()

# 对应sql: select * from lh_test where id > 4 limit 1
data = ModelDemo().where('id', '>', 4).first()

单个查询返回格式: {...}
```

#多个查询
``` bash
# 对应sql: select * from lh_test where id >= 4
data = ModelDemo().where('id', '>=', 4).get()

# 对应sql: select * from lh_test where id > 4
data = ModelDemo().where('id', '>', 4).get()

# 对应sql: select * from lh_test where id < 4
data = ModelDemo().where('id', '<', 4).get()

# 对应sql: select * from lh_test where id <= 4
data = ModelDemo().where('id', '<=', 4).get()

# 对应sql: select * from lh_test where id != 4
data = ModelDemo().where('id', '!=', 4).get()

# 对应sql: select * from lh_test where id in (1,2)
data = ModelDemo().where('id', 'in', [1, 2]).get()

# 对应sql: select * from lh_test where id not in (1,2)
data = ModelDemo().where('id', 'not in', [1, 2]).get()

# 对应sql: select * from lh_test where id between (1,2)
data = ModelDemo().where('id', 'between', [1, 2]).get()

# 对应sql: select * from lh_test where id not between (1,2)
data = ModelDemo().where('id', 'not between', [1, 2]).get()

# 对应sql: select * from lh_test where name like '%Tether%'
data = ModelDemo().where('name', 'like', '%Tether%').get()

# 对应sql: select * from lh_test where name not like '%Tether%'
data = ModelDemo().where('name', 'not like', '%Tether%').get()

多个查询返回格式: [{...}, {...}, {...}...]
```

# 多条件查询
``` bash
#对应sql:select * from lh_test where id=1 and name='hehe'
data = ModelDemo().where({'id': 1, 'name': 'hehe'}).get()
data = ModelDemo().where('id', 1).where('name', 'hehe').get()
```
# 排序
``` bash
#正序
#对应sql: select * from lh_test where id > 0 order by id
data = ModelDemo().where('id', '>', 0).orderby('id').get()
data = ModelDemo().where('id', '>', 0).orderby('id', 'asc').get()

#倒序
#对应sql: select * from lh_test where id > 0 order by id desc
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()

#多字段排序
#对应sql: select * from lh_test where `id` > 0 order by `id` desc,`status`
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status', 'asc').get()
```

# 取数量
``` bash
# 对应sql: select * from lh_test where id > 0 limit 1
data = ModelDemo().where('id', '>', 0).first()         #返回字典
data = ModelDemo().where('id', '>', 0).take(1).get()   #返回列表

# 对应sql: select * from lh_test where id > 0 limit 5
data = ModelDemo().where('id', '>', 0).take(5).get()
```

# 偏移量
``` bash
# 对应sql: select * from lh_test where id > 100 limit 5 offset 10
data = ModelDemo().where('id', '>', 100).offset(10).take(5).get()
```

# 检索字段
``` bash
# 对应sql: select `id`,`name` from lh_test limit 5
data = ModelDemo().select('id', 'name').take(5).get()

# 对应sql: select min(id) as minid from lh_test limit 1
data = ModelDemo().select('min(id) as minid').first()
```

# groupby
``` bash
# 对应sql: select count(*) as num,`name` from lh_test group by `name`
data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()
```

# 原生sql
``` bash
sql = 'select count(*) as num,name from lh_test group by name'
data = ModelDemo().execute(sql)
```

# 返回结果
``` bash
data = ModelDemo().where('id', 'in', [1,2,3]).select('id', 'name').lists('id')          # [1,2,3]
data = ModelDemo().where('id', 'in', [1,2]).select('id', 'name').lists(['id', 'name'])  # [[1,'name1'],[2,'name2']]
data = ModelDemo().select('id', 'name', 'status').data()                                # 返回pandas DataFrame
```

# 事务
``` bash
def demo():       #事务闭包
    ModelDemo().where('id', 42).update({'name': "44", 'token_name': '444'})
    ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    return True
data = ModelDemo().transaction(demo)
```

# 切换数据库
``` bash
使用.env中默认的default数据库:
    不设置ModelDemo类中的__database__属性 或者 在ModelDemo类中设置__database__='default'
使用.env中test_db2数据库:
    在ModelDemo类中设置__database__='test_db2'

代码中动态设置数据库:
ModelDemo().database('test_db2').where('id', '>', 40).first()
```

# 数据库日志
``` bash
开启:
    在.env中配置LOG_DIR:
    LOG_DIR=你的日志路径
    例如LOG_DIR=/home/logs/python/  就是把日志记录在/home/logs/python/20190520.log文件中(每天产生一个文件)
关闭:
    在.env中配置中删除LOG_DIR配置
    在.env中配置中注释掉LOG_DIR配置(前加#号)， 例如: #LOG_DIR=/home/logs/python/
```





## Authors

* ** -- ** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
