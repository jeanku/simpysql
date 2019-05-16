## Install

Via pip

``` bash
 pip install hangsql
```


## Initialization
you need to create a .env file at your project root path (/home/project/.env), and content as follows: 
``` bash
[default]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db1
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
LOG_DIR=/home/logs/python/
```

## Create Model
Create your Model extend DBModel as follows:
``` bash
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from hangsql.DBModel import DBModel

class ModelDemo(DBModel):
    __basepath__ = '/home/project/'             # 项目根目录 (.env文件路径:/home/project/.env)
    __database__ = 'default'                    # 库名
    __tablename__ = 'lh_test'                   # 表名
    __create_time__ = 'create_time'             # 插入时间字段 如果该字段为None create_time则不会自动添加
    __update_time__ = 'update_time'             # 更新时间字段 如果该字段为None update_time则不会自动添加
    columns = [                                 # 数据库字段
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]
```

## Usage
# create
``` bash
#单个添加
ModelDemo().create({'name': "haha1", 'token_name': 'haha124'})
#多个添加
ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name':"haha2", 'token_name': 'haha125'}])
#获取添加数据自增ID
id = ModelDemo().create({'name': "haha1", 'token_name': 'haha124'}).lastid()
```

# update
``` bash
#单个更新
ModelDemo().where('id', 1).update({'name':"hehe", 'token_name': 'hehe123'})
#范围更新
ModelDemo().where('id', 'in', [1, 2, 3]).update({'name':"hehe", 'token_name': 'hehe123'})
#自增自增
ModelDemo().where('id', 1).increment('status')        #status自增1
ModelDemo().where('id', 1).increment('status', 5)     #status自增5
#自增自减
ModelDemo().where('id', 1).decrement('status')        #status自减1
ModelDemo().where('id', 1).decrement('status', 5)     #status自减5
```

# delete
``` bash
#单个删除
ModelDemo().where('id', 4).delete()
#范围删除
ModelDemo().where('id', '<', 10).delete()
```
