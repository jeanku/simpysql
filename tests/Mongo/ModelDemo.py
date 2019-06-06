#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

from tests.mysqlDemo.BaseModel import BaseModel

class ModelDemo1(BaseModel):

    __database__ = 'VnTrader_Log_Db'        # 表名

    __tablename__ = '20190226'    # 表名

    __create_time__ = None  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = None  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [             # 数据库字段
        '_id',
        'trustor',
        'asset_issuer',
        'asset_code',
        'limit',
        'asset_type',
        'transaction_id',
        'type',
        'trustee',
        'id',
        'source_account',
    ]

class ModelDemo2(BaseModel):

    __database__ = 'VnTrader_Log_Db'        # 表名

    __tablename__ = 'lh_test'    # 表名

    __create_time__ = 'create_time'  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [             # 数据库字段
        '_id',
        'name',
    ]

    # set time format of create_time and update_time
    # def fresh_timestamp(self):
    #     return datetime.datetime.now().strftime("%Y%m%d")


if __name__ == '__main__':

    # data = ModelDemo1().select('content', 'time', 'gateway').data()

    # select * from table where gateway = 'MAIN_ENGINE'
    # data = ModelDemo1().where({'gateway': 'MAIN_ENGINE'}).select('content', 'time', 'gateway').data()
    # data = ModelDemo1().where('gateway', 'MAIN_ENGINE').select('content', 'time', 'gateway').data()
    # data = ModelDemo1().where('gateway', '=', 'MAIN_ENGINE').select('content', 'time', 'gateway').data()
    #
    data = ModelDemo1().where('gateway', '=', 'MAIN_ENGINE').select('content', 'time', 'gateway').first()
    # data = ModelDemo1().where('gateway', '<=', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', '<', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', '>', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', '>=', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', '!=', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'in', ['MAIN_ENGINE', 'BITFINEX']).select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'not in', ['MAIN_ENGINE', 'BITFINEX']).select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'like', 'MAIN_ENGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'not like', 'BITFINEX').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'ilike', 'MAIN_eNGINE').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'not ilike', 'bITFINEX').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'like', 'ENGINE$').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'like', '^MAIN_').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'like', '^MAIN_ENGINE$').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('gateway', 'like', '^MAIN_ENGINE$').select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('time', 'between', ['14:08:38', '14:11:37']).select('content', 'time', 'gateway').get()
    # data = ModelDemo1().where('time', 'not between', ['14:11:38', '19:38:18']).select('content', 'time', 'gateway').get()
    # model = ModelDemo1().where({'gateway': 'BITFINEX'}).where('time', '>=', '19:38:').select('content', 'time', 'gateway').get()

    # skip
    # data = ModelDemo1().where({'gateway': 'BITFINEX'}).offset(4).select('content', 'time', 'gateway').data()

    # # sort
    # # data = ModelDemo2().orderby('update_time').data()           # update_time 正序
    # # data = ModelDemo2().orderby('update_time', 'asc').data()    # update_time 正序
    # # data = ModelDemo2().orderby('update_time', 'desc').data()   # update_time 倒叙
    #
    # # take|limit
    # # data = ModelDemo2().orderby('update_time', 'desc').take(4).data()  # 获取4条记录
    #
    # # or
    # data = ModelDemo2().where('update_time', '>=', 1559722499).whereor([{'name': 'haha1'}, ['name', 'haha3'], ('name', '=', 'haha2')]).data()  # 获取4条记录
    # data = ModelDemo2().where('update_time', '=', 1559722499).whereor({'name': 'haha1'}).whereor('name', 'haha3').data()  # 获取4条记录
    # data = ModelDemo2().where('token_name', 'size', 2).data()  # 获取4条记录


    # create
    # data = ModelDemo2().create({'name': 'haha3', 'token_name': 'BTC'})
    # data = ModelDemo2().create([{'name': 'haha', 'token_name': 'USDT'}, {'name': 'haha1', 'token_name': 'BTC'}])

    # update
    # data = ModelDemo2().where('name', 'ilike', 'haHa').update({'token_name': ['BTC14', '123']})
    # data = ModelDemo2().where('name', 'haha').update({'token_name': 'BTC111'})

    # delete
    # ModelDemo2().where('name', 'haha1').delete()

    # data = ModelDemo2().where('token_name', ['BTC14', '123']).data()
    # data = ModelDemo2().data()


    # print(data)
    # exit(0)

    pass