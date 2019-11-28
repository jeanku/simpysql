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
    # update lh_test set name='hehe',token_name='haha4123',update_time=1559534994 where id=117
    data = ModelDemo('a').where('id', 1).update({'name': "hehe", 'token_name': 'haha4123',  'token_name1': 'haha4123'})

    # data = ModelDemo.where('id', 117).decrement('status')  # 字段自增1
    # data = ModelDemo.where('id', 117).decrement('status', 3)  # 字段自减3
    #
    # data = ModelDemo.where('id', 117).increment('status')  # 字段自增3
    # data = ModelDemo.where('id', 117).increment('status', 3)  # 字段自增3

    # replace into lh_test (`id`, `name`, `token_name`) values (136, 'hehe12', 'haha12')
    # data = ModelDemo.replace([{'id': 137, 'name': "hehe77", 'token_name': 'haha77'}, {'id': 138, 'name': "hehe11", 'token_name': 'haha11'}])  # 字段自增3

    # # 没有则添加， 有则更新
    # ModelDemo.where('name', 'hehe1234').create_or_update({'name': "hehe1234", 'token_name': "haha124"})

    exit(0)