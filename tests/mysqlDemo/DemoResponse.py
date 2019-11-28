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
    # 返回单条数据 dict: {'id': 50}
    data = ModelDemo.where('id', '>=', 50).select('id').first()

    # 返回单条数据 list: [{'id': 50}]
    data = ModelDemo.where('id', '>=', 50).select('id').take(1).get()

    # 返回单条数据 list: [50 55 56 57 58]
    data = ModelDemo.where('id', '>=', 50).take(5).lists('id')

    # 返回单条数据 list: [[50, 'haha'] [55, 'haha'] [56, 'haha'] [57, 'haha'] [58, 'haha']]
    data = ModelDemo.where('id', '>=', 50).take(5).lists(['id', 'name'])

    # 返回pandas dataFrame / None
    data = ModelDemo.where('id', '>=', 50).take(5).data()

    print(data)
    exit(0)
