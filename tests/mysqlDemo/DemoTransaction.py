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

    # 方法1:
    def demo():
        data = ModelDemo().where('id', 42).first()
        ModelDemo().where('id', 42).update({'name': "555", 'token_name': '555'})
        ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
        # raise Exception('haha')
        return data
    data = ModelDemo.transaction(demo)
    print(data)

    # 方法2:
    # @ModelDemo.transaction
    # def demo(id):
    #     data = ModelDemo.where('id', 43).first()
    #     ModelDemo.where('id', id).update({'name': "444", 'token_name': '444'})
    #     ModelDemo.where('id', 43).update({'name': "44", 'token_name': '444'})
    #     # raise Exception('haha')
    #     return data
    # data = demo(49)
    # print(data)

