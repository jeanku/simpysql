@[toc]
# SimpySql
基于pymysql的轻量级mysql ORM

# 简单实例
```python
ModelDemo().where('id', 4).select('id', 'name').take(5).get()
```

# 安装
```python
pip install simpysql
```

# 初始化
您需要在项目根路径处创建一个.env文件，内容如下：

```python
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

## 创建 Model
创建数据库Model并继承DBModel，如下所示：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from simpysql.DBModel import DBModel

class ModelDemo(DBModel):
    __basepath__ = '/home/project/'             # .env文件路径
    #__database__ = 'default'                   # 默认数据库default
    __tablename__ = 'lh_test'                   # 表名
    __create_time__ = 'create_time'             # 插入时间字段(没有则填None,自动填充,默认当前时间戳(秒))
    __update_time__ = 'update_time'             # 更新时间字段(没有则填None,自动填充,默认当前时间戳(秒))
    columns = [                                 # 数据库字段
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]

    # 如想改写create_time & update_time默认时间格式，就重写该方法
    # def fresh_timestamp(self):
    #     return datetime.datetime.now().strftime("%Y%m%d")
```


# 数据添加

## 添加单条数据
```python
ModelDemo().create({'name': "haha1", 'token_name': 'haha124'})
```

## 添加多条数据
```python
ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name':"haha2", 'token_name': 'haha125'}])
```

## 获取插入的自增ID
```python
id = ModelDemo().create({'name': "haha1", 'token_name': 'haha124'}).lastid()
```

# 更新

## 更新数据
```python
ModelDemo().where('id', 1).update({'name':"hehe", 'token_name': 'hehe123'})
```

## 自增
```python
ModelDemo().where('id', 1).increment('status')        #status increment by 1
ModelDemo().where('id', 1).increment('status', 5)     #status increment by 5
```

## 自减
```python
ModelDemo().where('id', 1).decrement('status')        #status decrement by 1
ModelDemo().where('id', 1).decrement('status', 5)     #status decrement by 5
```

# 删除
```python
ModelDemo().where('id', 4).delete()
```

## 查询

### 查询单条数据(first)
```python
# sql: select * from lh_test where id = 4 limit 1
data = ModelDemo().where('id', 4).first()
data = ModelDemo().where('id', '=', 4).first()
return data: {'id':4, 'name':...}
```

### 查询多条数据(get)
```python
# sql: select * from lh_test where id > 4 limit 5
data = ModelDemo().where('id', '>', 4).take(5).get()
return data: [{'id':5, 'name':...},{}...]
```

###  条件查询
```python
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

### 多添件查询
```python
# sql:select * from lh_test where id=1 and name='hehe'
data = ModelDemo().where({'id': 1, 'name': 'hehe'}).get()

# sql:select * from lh_test where id=1 and name like 'hehe%'
data = ModelDemo().where('id', 1).where('name', 'like', 'hehe%').get()
```

### 排序
```python
# sql: select * from lh_test where `id` > 0 order by `id` desc,`status`
data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status').get()
```

### 偏移
```python
# sql: select * from lh_test where id > 100 limit 5 offset 10
data = ModelDemo().where('id', '>', 100).offset(10).take(5).get()
```

### 自定义查询字段
```python
# sql: select `id`,`name` from lh_test limit 5
data = ModelDemo().select('id', 'name').take(5).get()

# 对应sql: select min(id) as minid from lh_test limit 1
data = ModelDemo().select('min(id) as minid').first()
```

### 分组 group by
```python
# sql: select count(*) as num,name from lh_test group by name
data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()
```

### Having查询
```python
# sql: select count(*) as num,name from lh_test group by name having num > 2
data = ModelDemo().select('count(*) as num', 'name').groupby('name').having('num', '>', 2).get()
```

### 字查询
```python
# sql: select * from lh_test where id=(select max(id) from lh_test) limit 1
data = ModelDemo().where('id', ModelDemo().select('max(id)')).first()

# sql:select * from lh_test where id in (select max(id) from lh_test where id <= 50)
data = ModelDemo().where('id', 'in', ModelDemo().where('id', '<=', 50).select('id')).get()
```

### tablename 别名
```python
# sql: select a.id,a.name from lh_test as a limit 1
data = ModelDemo('a').select('a.id', 'a.name').first()
```

### join查询
```python
# 【left join】sql: select a.id,b.name from lh_test as a left join lh_test as b on a.id = b.id where a.id=42
data = ModelDemo('a').where('a.id', 42).leftjoin(ModelDemo('b').on('a.id', '=', 'b.id')).select('a.id', 'b.name').get()

# 【right join】sql: select a.id,b.name from lh_test as a right join lh_test as b on a.id = b.id where a.id=42
data = ModelDemo('a').where('a.id', 42).rightjoin(ModelDemo('b').on('a.id', '=', 'b.id')).select('a.id', 'b.name').get()

# 【inner join】sql: select a.id,b.name from lh_test as a inner join lh_test as b on a.id = b.id where a.id=42
data = ModelDemo('a').where('a.id', 42).innerjoin(ModelDemo('b').on('a.id', '=', 'b.id')).select('a.id', 'b.name').get()
```

### Union查询
```python
# 【union all】sql: (select * from lh_test where id=42) union all (select * from lh_test where id=58)
data = ModelDemo().where('id', 42).unionall(ModelDemo().where('id', '=', 58)).get()

# 【union】sql: (select * from lh_test where id=42) union (select * from lh_test where id=58)
data = ModelDemo().where('id', 42).union(ModelDemo().where('id', '=', 58)).get()
```

### 原生SQL
```python
sql = 'select count(*) as num,name from lh_test group by name'
data = ModelDemo().execute(sql)
```

# 返回数据格式
```python
data = ModelDemo().where('id', '=', 1).select('id').first()                             # {'id':1}
data = ModelDemo().where('id', '=', 1).select('id').get()                               # [{'id':1}]
data = ModelDemo().where('id', 'in', [1,2,3]).select('id', 'name').lists('id')          # [1,2,3]
data = ModelDemo().where('id', 'in', [1,2]).select('id', 'name').lists(['id', 'name'])  # [[1,'name1'],[2,'name2']]
data = ModelDemo().select('id', 'name', 'status').data()                                # return pandas DataFrame
```

# 数据库事务
```python
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

# 多库切换

```python
在model中设置__database__属性为 .env中的数据库配置名称
__database__ = 'test_db2'

在代码中设置
ModelDemo().database('test_db2').where('id', '>', 40).first()
```

# 数据库日志
```python
在 .env 文件中开启LOG_DIR设置捷即可:
LOG_DIR=/home/logs/python/
```