# SimpySql

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


# Create
``` python
# insert into lh_test (`name`, `token_name`, `create_time`, `update_time`) values ('haha1', "haha'124", 1559553176, 1559553176)
ModelDemo().create({'name': "haha1", 'token_name': "haha'124"})

lastid = ModelDemo().create({'name': "haha1", 'token_name': "haha'125"}).lastid()

# multi create
ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name': "haha2", 'token_name': 'haha125'}])

# insert into lh_test (`name`, `token_name`) values ('haha1', 'haha125'),('haha1', 'haha124')
ModelDemo().insert(['name', 'token_name'], [['haha1', 'haha125'], ['haha1', 'haha124']])
```


# Update
``` python
# update lh_test set name='hehe',token_name='haha4123',update_time=1559534994 where id=117
ModelDemo().where('id', 117).update({'name': "hehe", 'token_name': 'haha4123'})

data = ModelDemo().where('id', 117).decrement('status')     # status decrease by 1
data = ModelDemo().where('id', 117).decrement('status', 3)  # status decrease by 3

data = ModelDemo().where('id', 117).increment('status')     # status increase by 1
data = ModelDemo().where('id', 117).increment('status', 3)  # status increase by 3
```

# Delete
``` python
ModelDemo().where('id', 4).delete()
```

## Select
``` python
# select * from lh_test where id=117
data = ModelDemo().where('id', 117).get()
data = ModelDemo().where({'id': 117}).get()
data = ModelDemo().where('id', '=', 117).get()

 # >=, >, <.<=, !=, like, not in, in, not between, between, like, not like
data = ModelDemo().where('id', '>=', 21026).get()
data = ModelDemo().where('id', '>', 21026).get()
data = ModelDemo().where('id', '<', 21026).get()
data = ModelDemo().where('id', '<=', 21026).get()
data = ModelDemo().where('id', '!=', 21026).get()
data = ModelDemo().where('id', 'in', ['21026', '21027']).get()
data = ModelDemo().where('id', 'not in', [21026, 21027, 4283]).get()
data = ModelDemo().where('id', 'between', [21026, 21027]).get()
data = ModelDemo().where('id', 'not between', [21026, 21027]).get()
data = ModelDemo().where('name', 'like', 'Tether%').get()
data = ModelDemo().where('name', 'not like', 'Tether%').get()

# 多条件查询
# select * from lh_test where `id`=1 and `name`='hehe' and `token_name`='hehe123' and `id` > 0
data = ModelDemo().where({'id': 1, 'name': 'hehe', 'token_name': 'hehe123'}).where('id', '>', 0).get()

# 排序(order by)
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()  # 正序
data = ModelDemo().where('id', '>', 0).orderby('id').get()  # 正序
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()  # 倒序
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status', 'asc').get()  # 多个字段排序

# 取数量(limit m)
data = ModelDemo().where('id', '>', 0).take(1).get()  # 取一条 并返回list
data = ModelDemo().where('id', '>', 0).take(5).get()  # 取5条 并返回list

# 偏移量(offset m)
data = ModelDemo().where('id', '>', 0).offset(10).take(5).get()  # 偏移量为1， 取5条 并返回list

# 检索字段(select columns)
data = ModelDemo().select('id', 'name').take(5).get()  # select `id`,`name` from lh_test limit 5
data = ModelDemo().select('min(id) as minid').get()  # select min(id) as minid from lh_test limit 1
data = ModelDemo().select('max(id) as maxid').get()  # select max(id) as maxid from lh_test limit 1
data = ModelDemo().select(
    'from_unixtime(create_time) as time').get()  # select from_unixtime(create_time) as time from lh_test
data = ModelDemo().select('count(distinct id)').get()  # select count(distinct id) from lh_test

# groupby
# select count(*) as num,name from lh_test group by name
data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()
# select count(*) as num,name,token_name from lh_test group by name,token_name
data = ModelDemo().select('count(*) as num', 'name', 'token_name').groupby('name', 'token_name').get()
# select count(*) as num from lh_test group by left(name, 4)
data = ModelDemo().select('count(*) as num').groupby('left(name, 4)').get()

# having
# select count(*) as num,name from lh_test group by name having num = 2
data = ModelDemo().select('count(*) as num', 'name').groupby('name').having('num', 2).get()
# select name from lh_test having left(name, 4) = 'haha'
data = ModelDemo().select('name').having('left(name, 4)', '=', 'haha').get()

# 锁 lock (共享所和排他锁)
# select * from lh_test limit 1 for update
data = ModelDemo().lock_for_update().get()
# select * from lh_test lock in share mode
data = ModelDemo().lock_for_share().get()

# 聚合查询
data = ModelDemo('a').where('id', '>', 163).count()
data = ModelDemo('a').where('id', '>', 63).max('id')
data = ModelDemo('a').where('id', '>', 63).min('id')
data = ModelDemo('a').where('id', '>', 63).avg('id')
data = ModelDemo('a').where('id', '>', 63).sum('id')

# 判断记录是否存在 return: True/False 
data = ModelDemo('a').where('id', '>', 63).exist()
    
# 原生sql
data = ModelDemo().execute('select count(*) as num,`name` from lh_test group by name')

# 表名设置别名
# select a.name,a.token_name from lh_test as a where id=62
data = ModelDemo('a').select('a.name', 'a.token_name').where('id', 62).get()
```

### Select or
``` python
# select * from lh_test where id=62 or id=63
data = ModelDemo().where('id', 62).orwhere('id', 63).get()
data = ModelDemo().where('id', 62).orwhere('id', '=', 63).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).get()

# select * from lh_test where id=62 or .. or ..
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', '>', 64).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', '>=', 64).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', '<', 64).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', '<=', 64).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', '!=', 64).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'in', [64, 65]).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'not in', (64, 65)).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'like', '64%').get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'not like', '64%').get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'between', (64, 65)).get()
data = ModelDemo().where('id', 62).orwhere({'id': 63}).orwhere('id', 'not between', [64, 65]).get()

# select * from lh_test where id=63 or id in (select id from lh_test where id in (56, 57))
subquery = ModelDemo().select('id').where('id', 'in', [56, 57])
data = ModelDemo().where('id', 63).orwhere('id', 'in', subquery).get()

# select * from lh_test where id=62 or (id > 63 and id < 78)
data = ModelDemo().where('id', 62).orwhere([['id', '>', 63], ('id', '<', 78)]).get()

# select * from lh_test where id=62 or (id=63 and name='haha')
data = ModelDemo().where('id', 62).orwhere({'id': 63, 'name': 'haha'}).get()

# select * from lh_test where id=62 and ((id=63 and name='haha') or id < 78 or (id <= 75 and id >= 56))
data = ModelDemo().where('id', 62).whereor([
    {'id': 63, 'name': 'haha'},
    ('id', '<', 78),
    [
        ['id', '<=', 75],
        ['id', '>=', 56],
    ]
]).get()
```

# Select 关联查询
``` python
# in/not in 子查询
# select * from lh_test where id in (select id from lh_test where id in (56, 57))
subquery = ModelDemo().select('id').where('id', 'in', [56, 57])
data = ModelDemo().where('id', 'in', subquery).get()
data = ModelDemo().where('id', 'not in', subquery).get()

# 子查询
# select * from lh_test where id=(select max(id) as id from lh_test where id <= 60)
subquery = ModelDemo().select('max(id) as id').where('id', '=', 60)
data = ModelDemo().where('id', '=', subquery).get()

# left join
# select a.id,b.name from lh_test as a left join lh_test as b on a.id = b.id where a.id=42
joinmodel = ModelDemo('b').on('a.id', '=', 'b.id')
data = ModelDemo('a').where('a.id', 42).leftjoin(joinmodel).select('a.id', 'b.name').get()

# right join
# select a.id,b.name from lh_test as a right join lh_test as b on a.id = b.id where a.id=42
joinmodel = ModelDemo('b').on('a.id', '=', 'b.id')
data = ModelDemo('a').where('a.id', 42).rightjoin(joinmodel).select('a.id', 'b.name').get()

# inner join
# select a.id,b.name from lh_test as a inner join lh_test as b on a.id = b.id where a.id=42
joinmodel = ModelDemo('b').on('a.id', '=', 'b.id')
data = ModelDemo('a').where('a.id', 42).join(joinmodel).select('a.id', 'b.name').get()
data = ModelDemo('a').where('a.id', 42).innerjoin(joinmodel).select('a.id', 'b.name').get()

# union / union all
data = ModelDemo().where('id', 62).union(ModelDemo().where('id', '=', 58)).get()
data = ModelDemo().where('id', 62).unionall(ModelDemo().where('id', '=', 58)).get()

# subquery
# select id from (select * from lh_test where id=42) as tmp
submodel = ModelDemo().where('id', '=', 42)
data = ModelDemo().select('id').subquery(submodel).get()

# 子查询查询别名
# select a.id,a.name from (select * from lh_test where id=42) as a
submodel = ModelDemo().where('id', '=', 42)
data = ModelDemo().select('a.id', 'a.name').subquery(submodel, 'a').get()

# 多个子查询查询
# select a.id,a.name from lh_test as a,(select * from lh_test where id >= 42) as b where a.id=b.id and a.id > '45' limit 5
submodel = ModelDemo().where('id', '>=', 42)
data = ModelDemo().select('a.id', 'a.name').subquery('lh_test', 'a').subquery(submodel, 'b')\
    .where('a.id', 'b.id').where('a.id', '>', '45').take(5).get()
```

# 返回结果
``` python
# 返回单条数据 dict: {'id': 50}
data = ModelDemo().where('id', '>=', 50).select('id').first()

# 返回数据 list: [{'id': 50}]
data = ModelDemo().where('id', '>=', 50).select('id').take(1).get()

# 返回数据 list: [50, 55, 56, 57, 58]
data = ModelDemo().where('id', '>=', 50).take(5).lists('id')

# 返回数据 list: [[50, 'haha'], [55, 'haha'], [56, 'haha'], [57, 'haha'], [58, 'haha']]
data = ModelDemo().where('id', '>=', 50).take(5).lists(['id', 'name'])

# 返回pandas dataFrame / None
data = ModelDemo().where('id', '>=', 1150).take(5).data()
```

# 数据库事务
``` python
方法1:
def demo():
    ModelDemo().where('id', 42).update({'name': "44", 'token_name': '444'})
    ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    return True
data = ModelDemo().transaction(demo)

方法2:
@ModelDemo.transaction
def demo(id):
    ModelDemo().where('id', id).update({'name': "44", 'token_name': '111'})
    ModelDemo().where('id', 43).update({'name': "44", 'token_name': '111'})
    # raise Exception('haha')
    return True
demo(42)
```

# 切换数据库

``` python
在model中通过__database__设置数据库:
__database__ = 'test_db2'

在使用时设置数据库:
ModelDemo().database('test_db2').where('id', '>', 40).first()
```

# Log日志
``` python
在.env 文件中设置LOG_DIR属性即可:
LOG_DIR=/home/logs/python/
```
