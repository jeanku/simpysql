#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

from tests.Sqlserver.BaseModel import BaseModel


class ModelDemo(BaseModel):
    __tablename__ = 'zz_user'  # 表名

    __database__ = 'sqlserver'

    __create_time__ = 'create_time'  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        'id',
        'name',
        'token_name',
        'age',
        'create_time',
        'update_time',
    ]


if __name__ == '__main__':

    # select * from lh_test where id=117
    # data = ModelDemo().where('id', '>=', 4).get()
    # data = ModelDemo().where({'id': 5}).get()
    # data = ModelDemo().where('id', '=', 5).get()

    # # >=, >, <.<=, !=, like, not in, in, not between, between, like, not like
    # data = ModelDemo().where('id', '>=', 4).get()
    # data = ModelDemo().where('id', '>', 4).get()
    # data = ModelDemo().where('id', '<', 4).get()
    # data = ModelDemo().where('id', '<=', 4).get()
    # data = ModelDemo().where('id', '!=', 4).get()
    # data = ModelDemo().where('id', 'in', ['4', '5']).get()
    # data = ModelDemo().where('id', 'not in', [4, 5, 6]).get()
    # data = ModelDemo().where('id', 'between', [3, 5]).get()
    # data = ModelDemo().where('id', 'not between', [4, 6]).get()
    # data = ModelDemo().where('name', 'like', 'Tether%').get()
    # data = ModelDemo().where('name', 'not like', 'Tether%').get()
    #
    # # 多条件查询
    # select * from lh_test where `id`=1 and `name`='hehe' and `token_name`='hehe123' and `id` > 0
    # data = ModelDemo().where({'id': 4, 'name': 'name'}).where('id', '>', 0).get()
    #
    # # 排序(order by)
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()  # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id').get()  # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()  # 倒序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('name', 'asc').get()  # 多个字段排序
    #
    # # 取数量(limit m)
    # data = ModelDemo().where('id', '>', 0).take(1).get()  # 取一条 并返回list
    # data = ModelDemo().where('id', '>', 0).take(5).get()  # 取5条 并返回list
    #
    # # 偏移量(offset m)
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').offset(10).take(5).get()  # 偏移量为1， 取5条 并返回list
    #
    # # 检索字段
    # data = ModelDemo().select('id', 'name').take(5).get()  # select `id`,`name` from lh_test limit 5
    # data = ModelDemo().select('min(id) as minid').get()  # select min(id) as minid from zz_user
    # data = ModelDemo().select('max(id) as maxid').get()  # select max(id) as maxid from zz_user
    # data = ModelDemo().select('distinct id').get()  # select select distinct id from zz_user
    #
    # # groupby
    # select count(*) as num,name from zz_user group by name
    # data = ModelDemo().select('count(*) as num', 'name').groupby('name').get()
    # # select count(*) as num,name,token_name from zz_user group by name,token_name
    # data = ModelDemo().select('count(*) as num', 'name', 'token_name').groupby('name', 'token_name').get()
    # # select count(*) as num from lh_test group by left(name, 4)
    # data = ModelDemo().select('count(*) as num').groupby('left(name, 4)').get()
    #
    # # having
    # # select count(*) as num,name from lh_test group by name having num = 2
    # data = ModelDemo().having('name', 'name12').get()
    # todo
    # # select name from lh_test having left(name, 4) = 'haha'
    # data = ModelDemo().select('name').having('left(name, 4)', '=', 'haha').get()
    #
    # # 聚合查询
    data = ModelDemo('a').where('id', '>', 0).count()
    data = ModelDemo('a').where('id', '>', 0).max('id')
    data = ModelDemo('a').where('id', '>', 0).min('id')
    data = ModelDemo('a').where('id', '>', 0).avg('id')
    data = ModelDemo('a').where('id', '>', 0).sum('id')
    #
    # # 判断记录是否存在
    data = ModelDemo('a').where('id', '>', 0).exist()
    #
    # # 锁(共享所和排他锁)
    # # select * from lh_test limit 1 for update
    # data = ModelDemo().lock_for_update().get()
    # # select * from lh_test lock in share mode
    # data = ModelDemo().lock_for_share().get()
    #
    # # 原生sql
    # data = ModelDemo().execute('select count(*) as num,`name` from lh_test group by name')
    #
    # # 表名设置别名
    # # select a.name,a.token_name from lh_test as a where id=62
    data = ModelDemo('a').select('a.name', 'a.token_name').where('id', 4).get()

    print(data)
    exit(0)
