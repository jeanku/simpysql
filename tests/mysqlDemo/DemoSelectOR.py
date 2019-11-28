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
    # select * from lh_test where id=62 or id=63
    data = ModelDemo.where('id', 62).orwhere('id', 63).get()
    data = ModelDemo.where('id', 62).orwhere('id', '=', 63).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).get()

    # select * from lh_test where id=62 or .. or ..
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', '>', 64).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', '>=', 64).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', '<', 64).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', '<=', 64).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', '!=', 64).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'in', [64, 65]).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'not in', (64, 65)).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'like', '64%').get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'not like', '64%').get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'between', (64, 65)).get()
    data = ModelDemo.where('id', 62).orwhere({'id': 63}).orwhere('id', 'not between', [64, 65]).get()

    # select * from lh_test where id=63 or id in (select id from lh_test where id in (56, 57))
    subquery = ModelDemo.select('id').where('id', 'in', [56, 57])
    data = ModelDemo.where('id', 63).orwhere('id', 'in', subquery).get()

    # select * from lh_test where id=62 or (id > 63 and id < 78)
    data = ModelDemo.where('id', 62).orwhere([['id', '>', 63], ('id', '<', 78)]).get()

    # select * from lh_test where id=62 or (id=63 and name='haha')
    data = ModelDemo.where('id', 62).orwhere({'id': 63, 'name': 'haha'}).get()

    # select * from lh_test where id=62 and ((id=63 and name='haha') or id < 78 or (id <= 75 and id >= 56))
    data = ModelDemo.where('id', 62).whereor([
        {'id': 63, 'name': 'haha'},
        ('id', '<', 78),
        [
            ['id', '<=', 75],
            ['id', '>=', 56],
        ]
    ]).get()

    print(data)
    exit(0)
