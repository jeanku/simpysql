#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

from tests.mysqlDemo.BaseModel import BaseModel


class ModelDemo(BaseModel):

    __tablename__ = 'lh_test'  # 表名

    __create_time__ = 'create_time'  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]


if __name__ == '__main__':
    ''''''
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
    submodel1 = ModelDemo().where('id', '<=', 62)
    submodel2 = ModelDemo().where('id', '>=', 42)
    data = ModelDemo().select('a.id', 'a.name').subquery(submodel1, 'a').subquery('lh_test', 'b').subquery(submodel2, 'c')\
        .where('a.id', 'b.id').where('a.id', 'c.id').where('a.id', '>', '45').take(5).get()

    print(data)
    exit(0)
    pass