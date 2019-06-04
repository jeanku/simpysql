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


if __name__ == '__main__':

    model = ModelDemo1().select('content', 'time', 'gateway').data()
    # model = ModelDemo1().where({'gateway': 'BITFINEX'}).where('time', '>=', '19:38:').select('content', 'time', 'gateway').get()
    print(model)
    exit(0)
    #
    # data = ModelDemo2().where('time', '>', '2019-05-01 00:17:30').take(5).get()
    # print(data)
    # exit(0)
    # return list(self.db.event.find({"status": "running", "expire_time": {"$lt": "14:08:38"}}))

    # [longhash_mongo]
    # DB_TYPE = mongodb
    # DB_HOST = 47.96.228.84
    # DB_PORT = 27017
    # DB_NAME = data_service
    # DB_USER = root
    # DB_PASSWORD = longhash123!
    #
    # @  # QAZ
    #
    #
    # DB_CHARSET = utf8mb4

    # myclient = pymongo.MongoClient(host='47.96.228.84', port=27017, username='root', password='longhash123!@#QAZ',authMechanism='SCRAM-SHA-1')
    # myclient = pymongo.MongoClient('121.196.217.75', 27017)
    # # myclient['data_service'].authenticate('root', 'longhash123!@#QAZ')
    # # print(myclient['data_service']['tron_wallet_transfer'].find_one())
    # data = myclient['VnTrader_Log_Db']["20190226"].find().limit(5).sort("time", pymongo.DESCENDING)
    # # print(data)
    # for index in data:
    #     print(index)

    #     print(index)

    # data = ModelDemo3().select('blockNumber').where('blockNumber', -1).orderby('blockNumber', 'desc').take(10).lists('blockNumber')
    # print(data)
    # exit(0)
    # pass