# SimpySql

# 安装
```
pip install simpysql
```

# 初始化
你需要在你的项目根目录下创建一个.env文件，内容如下:

``` python
[default]                                       #数据库配置名称(对应model.__database__)
DB_TYPE=mysql                                   #数据库类型 mysql 或者 mongodb
DB_HOST=127.0.0.1                               #数据库IP                          
DB_PORT=3306                                    #端口
DB_NAME=test_db1                                #库名
DB_USER=root                                    #账号
DB_PASSWORD=123456                              #密码
DB_CHARSET=utf8mb4                              #数据库编码
LOG_DIR=/home/logs/python/                      #开启日志， 日志路径: /home/logs/python/

[test_db2]                                      #其他的库
DB_TYPE=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db2
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
#LOG_DIR=/home/logs/python/                     #关闭日志
```

# 创建表model

创建数据库model 并继承simpysql.DBModel:

``` python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from simpysql.DBModel import DBModel

class ModelDemo(DBModel):
    
    __basepath__ = '/home/project/'             # .env 文件路径
    #__database__ = 'default'                   # 库选择， 没有该属性，则默认default库
    __tablename__ = 'lh_test'                   # table name
    __create_time__ = 'create_time'             # 自动添加创建时间字段create_time(精确到秒)， 设置为None或者删除该属性，则不自动添加 
    __update_time__ = 'update_time'             # 自动更新时间字段update_time(精确到秒)， 设置为None或者删除该属性，则不自动更新
    columns = [                                 # table columns
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]

    # 可以通过该方法设置自动添加时间字段的格式
    # def fresh_timestamp(self):
    #     return datetime.datetime.now().strftime("%Y%m%d")
```


# Create
``` python
# 插入单条数据
data =ModelDemo.create({'name': 'haha1', 'token_name': 'BTC'})
# 插入多条数据
data =ModelDemo.create([{'name': 'haha', 'token_name': 'USDT'}, {'name': 'haha1', 'token_name': 'BTC'}])
```


# Update
``` python
# update
data =ModelDemo.where('name', 'ilike', 'haHa').update({'token_name': ['BTC14', '123']})
data =ModelDemo.where('name', 'haha').update({'token_name': 'BTC111'})
```

# Delete
``` python
# delete
ModelDemo().where('name', 'haha1').delete()
```

## Select
``` python
# select 'content', 'time', 'gateway' from table where gateway = 'MAIN_ENGINE'
data =ModelDemo.where({'gateway': 'MAIN_ENGINE'}).select('content', 'time', 'gateway').data()
data =ModelDemo.where('gateway', 'MAIN_ENGINE').select('content', 'time', 'gateway').data()
data =ModelDemo.where('gateway', '=', 'MAIN_ENGINE').select('content', 'time', 'gateway').data()


data =ModelDemo.where('gateway', '=', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', '<=', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', '<', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', '>', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', '>=', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', '!=', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', 'in', ['MAIN_ENGINE', 'BITFINEX']).get()
data =ModelDemo.where('gateway', 'not in', ['MAIN_ENGINE', 'BITFINEX']).get()
data =ModelDemo.where('gateway', 'like', 'MAIN_ENGINE').get()
data =ModelDemo.where('gateway', 'not like', 'BITFINEX').get()
data =ModelDemo.where('gateway', 'ilike', 'MAIN_eNGINE').get()       # like 不区分大小写
data =ModelDemo.where('gateway', 'not ilike', 'bITFINEX').get()      # not like 不区分大小写
data =ModelDemo.where('gateway', 'like', 'ENGINE$').get()            # 以'ENGINE'结尾的 like查询    
data =ModelDemo.where('gateway', 'like', '^MAIN_').get()             # 以'MAIN_'开头的 like查询
data =ModelDemo.where('gateway', 'like', '^MAIN_ENGINE$').get()      #gateway='MAIN_ENGINE' 
data =ModelDemo.where('time', 'between', ['14:08:38', '14:11:37']).get()
data =ModelDemo.where('time', 'not between', ['14:11:38', '19:38:18']).get()
data =ModelDemo.where({'gateway': 'BITFINEX'}).where('time', '>=', '19:38:').get()       #多条件查询

# skip|offset
# data =ModelDemo.where({'gateway': 'BITFINEX'}).offset(4).get()

# sort
data = ModelDemo2().orderby('update_time').get()           # update_time 正序
data = ModelDemo2().orderby('update_time', 'asc').get()    # update_time 正序
data = ModelDemo2().orderby('update_time', 'desc').get()   # update_time 倒叙

# take|limit
data = ModelDemo2().orderby('update_time', 'desc').take(4).get()  # 获取4条记录

# or
# {'$and': [{'update_time': {'$gte': 1559722499}}], '$or': [{'name': 'haha1'}, {'name': 'haha3'}, {'name': 'haha2'}]}
data = ModelDemo2().where('update_time', '>=', 1559722499).whereor([{'name': 'haha1'}, ['name', 'haha3'], ('name', '=', 'haha2')]).get()
# {'$and': [{'update_time': 1559722499}], '$or': [{'name': 'haha1'}, {'name': 'haha3'}]}
data = ModelDemo2().where('update_time', '>=', 1559722499).whereor({'name': 'haha1'}).whereor('name', 'haha3').get()
```

# Response
``` python
# 返回单条数据 dict: {'id': 50}
data =ModelDemo.where('id', '>=', 50).select('id').first()
print(data)          # {'id': 50}
print(data.id)       # 50
print(data['id'])    # 50

# 返回数据 list: [{'id': 50}]
data =ModelDemo.where('id', '>=', 50).select('id').take(1).get()
print(data)                                 # [{'id': 50}]
print([index.id for index in data])         # [50]
print([index['id'] for index in data])      # [50]

# 返回数据 list: [50, 55, 56, 57, 58]
data =ModelDemo.where('id', '>=', 50).take(5).lists('id')

# 返回数据 list: [[50, 'haha'], [55, 'haha'], [56, 'haha'], [57, 'haha'], [58, 'haha']]
data =ModelDemo.where('id', '>=', 50).take(5).lists(['id', 'name'])

# 返回数据 key-value: {'14:08:38': 'MAIN_ENGINE', '14:11:37': 'MAIN_ENGINE', ...}
data = ModelDemo1().select('content', 'time', 'gateway').take(10).pluck('time', 'gateway')

# 返回pandas dataFrame / None
data =ModelDemo.where('id', '>=', 1150).take(5).data()
```
