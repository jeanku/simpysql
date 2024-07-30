# SimpySql

# 安装
```
pip install simpysqls

# 安装cassandra依赖
pip install cassandra-driver
```

# 初始化
你需要在你的项目根目录下创建一个.env文件，内容如下:

``` python
[kasplex]           # 数据库配置
DB_TYPE=cassandra
DB_HOST=127.0.0.1
DB_PORT=9042
DB_USER=user
DB_PASSWORD=password
DB_CHARSET=utf8mb4
DB_KEYSPACE=keyspace_name
SSL_CERTFILE=
SSL_CA_CERTS=/Users/jemes/Documents/ssh-key/sf-***-cert.crt
SSL_KEYFILE=
LOG_DIR=/var/Log/
```

# 创建表model

创建数据库model 并继承simpysql.DBModel:

``` python

#!/usr/bin/python
# -*- coding: UTF-8 -*-

from simpysql.DBModel import DBModel
import os

class BaseModel(DBModel):
    __basepath__ = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/'
    
    
    
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from simpysql.DBModel import DBModel

class ModelDemo(BaseModel):

    __database__ = "community"

    __tablename__ = 'tx'  # 表名

    # __create_time__ =   # 插入时间字段 如果该字段为None create_time则不会自动添加

    # __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        'from_addr',
        'to_addr',
        'hash_code',
        'amount',
        'height',
    ]
```


# Create
``` python
    # sql: insert into tx ("from_addr", "to_addr", "hash_code", "amount", "height") values ('qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d3', 'cy3dfs9dc3w7lm9rq0zs76vf959mmrp3', 'hashcode22', 104, 86400)
    ModelDemo.create({
        'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d3",
        'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp3",
        'hash_code': 'hashcode22',
        'amount': 104,
        'height': 86400,
    })

    # 添加多个数据
    ModelDemo.create([{
        'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
        'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp",
        'hash_code': 'hashcode22',
        'amount': 100,
        'height': 86400,
    },{
        'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1",
        'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp1",
        'hash_code': 'hashcode',
        'amount': 100,
        'height': 86400,
    }])
```


# Update
``` python
# sql: update tx set "amount"=999 where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2' and "hash_code"='hashcode'
ModelDemo.where("from_addr", "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2").where("hash_code", "hashcode").update({"amount": 999})
ModelDemo.where({
    "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2",
    "hash_code": "hashcode"
}).update({"amount": 998})
```

# Delete
``` python
    # sql: delete from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1' and "hash_code"='hashcode'
    ModelDemo.where({
        "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1",
        "hash_code": "hashcode"
    }).delete()
```

## Select
``` python
# select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2'
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2").get()

# 查询 select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2' and "hash_code"='hashcode' limit 1
data = ModelDemo.where({
    "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2",
    "hash_code": "hashcode"
}).first() 
    

# 排序(order by)
# sql: select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d' order by "hash_code" limit 10
data = ModelDemo.where({
    "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
}).take(10).orderby("hash_code").get()

# sql: select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d' order by "hash_code" desc limit 10
data = ModelDemo.where({
    "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
}).take(10).orderby("hash_code", "desc").get()

# 取数量(limit m)
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d").take(1).get()  # 取一条 并返回list
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d").take(5).get()  # 取5条 并返回list

# 检索字段(select columns)
# sql: select "hash_code","from_addr" from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' limit 2
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").select("hash_code", "from_addr").take(2).get()

 
# 聚合查询
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").count()
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").max('id')
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").min('id')
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").avg('id')
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").sum('id')

# 判断记录是否存在 return: True/False 
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").exist()
    
# 原生sql
sql = "select * from tx where \"from_addr\"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' order by \"hash_code\" ASC limit 5"
data = ModelDemo.execute(sql)

# 数据返回
# select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' limit 5
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").take(5).lists("hash_code")  
# data: ['00b76e75611a363589dc3ba8ee01f5a4', '074e1583d26c7f78975c848c3b1923c5', '0cf0b24ffed5c27ef7bb2ee9637c0d46', '18beff6d825dfd6ef0d832e2383f645f', '290c7aff72cfb174fa711358998930d1']

2024-07-30 14:14:19,945 【INFO】【sql】:select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' limit 2
data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").take(2).pluck("hash_code", "amount")
# data: {'00b76e75611a363589dc3ba8ee01f5a4': 103.0999984741211, '074e1583d26c7f78975c848c3b1923c5': 117.0999984741211}    
```

# Log日志
``` python
在.env 文件中设置LOG_DIR属性即可:
LOG_DIR=/home/logs/python/
```
