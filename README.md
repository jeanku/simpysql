## Install

Via pip

``` bash
 pip install hangsql
```


# Initialization
you need to create a .env file at your project root path, and content as follows:
and .env file path is: /home/project/.env
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

# Usage
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
