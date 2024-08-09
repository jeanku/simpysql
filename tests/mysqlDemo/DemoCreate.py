#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

from tests.mysqlDemo.BaseModel import BaseModel


class ModelDemo(BaseModel):
    __database__ = 'default'  # 表名

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
    # 插入
    # id = ModelDemo.create({'name': "haha1", 'token_name': "haha'124", "create_time": 1413510, "update_time": 1413510})
    # # 添加数据 并获取插入的自增ID
    # lastid = ModelDemo.create({'name': "haha1", 'token_name': "haha'125"}).lastid()
    # # print(lastid)
    # # #
    # # # # 批量插入
    # ModelDemo.create([{'name': "haha1", 'token_name': 'haha124'}, {'name': "haha2", 'token_name': 'haha125'}])
    # # insert into lh_test (`name`, `token_name`) values ('haha1', 'haha125'),('haha1', 'haha124')
    # ModelDemo.insert(['name', 'token_name'], [['haha1', 'haha125'], ['haha1', 'haha124']])
    #
    # #插入
    # ModelDemo.insert_on_duplicate({'id': 36, 'name': "haha10", 'token_name': "haha'128"})
    # ModelDemo.insert_on_duplicate({'name': "haha11", 'token_name': "haha'128"})

    # insert ignore into lh_test (`name`, `token_name`, `create_time`, `update_time`) values ('haha1', "haha'124", 1413510, 1413510),('haha2', "haha'125", 1413510, 1413510)
    ModelDemo.insert_ignore([{'name': "haha1", 'token_name': "haha'124", "create_time": 1413510, "update_time": 1413510}, {'name': "haha2", 'token_name': "haha'125", "create_time": 1413510, "update_time": 1413510}])
    pass
