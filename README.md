# SimpySql

一个数据库orm, 目前支持`mysql`, `mongodb`

[mysql文档](./README_mysql.md)
, [mongo文档](./README_mongo.md)

# 安装
```
pip install simpysql
```

# 初始化
你需要在你的项目根目录下创建一个.env文件，内容如下:

``` python
[default]                                       #数据库配置名称(对应model.__database__)
DB_TYPE=mysql                                   #数据库类型 mysql 或者 mongo
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

## 操作实例

```python
ModelDemo.where('id', 4).select('id', 'name').take(5).get()
```

## 其他
欢迎志同道合的朋友一起参与本项目开发SQLServer、PostgreSQL开发, 联系方式: 490573621@qq.com
