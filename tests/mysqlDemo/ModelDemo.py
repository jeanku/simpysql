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

    __database__ = 'longhash_mongo'         # 表名

    __tablename__ = 'tron_wallet_transfer' # 表名

    __create_time__ = None  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = None  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [             # 数据库字段
        '_id',
        'amount',
        'time',
        'type',
        'transferFromAddress',
        'transferToAddress',
        'transactionHash',
    ]

class ModelDemo3(BaseModel):

    __database__ = 'longhash_parity'         # 表名

    __tablename__ = 'USDT' # 表名

    __create_time__ = None  # 插入时间字段 如果该字段为None create_time则不会自动添加

    __update_time__ = None  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        '_id',
        'blockNumber',
        'value',
        'from',
        'to',
        'transactionHash',
    ]

if __name__ == '__main__':
    # 插入
    # ModelDemo().create({'name': "haha1", 'token_name': "haha'124"})
    # lastid = ModelDemo().create({'name': "haha1", 'token_name': "haha'124"}).lastid()
    # print(lastid)
    # 批量插入
    # ModelDemo().create([{'name': "haha1", 'token_name': 'haha124'}, {'name':"haha2", 'token_name': 'haha125'}])

    # 更新
    # data = {'name':"hehe", 'token_name': 'haha"\"\'124'}
    # print(data.__str__())
    # ModelDemo().where('id', 42).update(data)
    # print("123")
    # exit(0)
    # data = ModelDemo().where('id', 1).decrement('status', 3)                     #字段自增1
    # data = ModelDemo().where('id', 1).increment('status', 3)                  #字段自增3
    # data = ModelDemo().where('id', 1).decrement('status', 3)                  #字段自减3

    # 删除
    # data = ModelDemo().where('id', 4).delete()
    # 查询[精确查询]
    # data = ModelDemo().where('id', '>', 1).first()
    # data = ModelDemo().where('id', '=', 21026).first()

    # 按ID 范围查询
    # data = ModelDemo().where('id', '>=', 21026).get()
    # data = ModelDemo().where('id', '>', 21026).get()
    # data = ModelDemo().where('id', '<', 21026).get()
    # data = ModelDemo().where('id', '<=', 21026).get()
    # data = ModelDemo().where('id', '!=', 21026).get()
    # data = ModelDemo().where('id', 'in', [21026, 21027]).get()
    # data = ModelDemo().where('id', 'not in', [21026, 21027, 4283]).get()
    # data = ModelDemo().where('id', 'between', [21026, 21027]).get()
    # data = ModelDemo().where('id', 'not between', [21026, 21027]).get()
    # data = ModelDemo().where('name', 'like', 'Tether').first()
    # data = ModelDemo().where('name', 'not like', 'Tether').first()

    # 多条件查询
    # select * from lh_test where `id`=1 and `name`='hehe' and `token_name`='hehe123' and `id` > 0
    # data = ModelDemo().where({'id': 1, 'name': 'hehe', 'token_name': 'hehe123'}).where('id', '>', 0).get()

    # 排序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()          # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id').get()                    # 正序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').get()          # 倒序
    # data = ModelDemo().where('id', '>', 0).orderby('id', 'desc').orderby('status', 'asc').get()   # 多个字段排序

    # 取数量
    # data = ModelDemo().where('id', '>', 0).first()              # 取一条 并返回字典
    # data = ModelDemo().where('id', '>', 0).take(1).get()        # 取一条 并返回list
    # data = ModelDemo().where('id', '>', 0).take(5).get()        # 取5条 并返回list

    # 偏移量
    # data = ModelDemo().where('id', '>', 0).offset(10).take(5).get()        # 偏移量为1， 取5条 并返回list

    # 检索字段
    # data = ModelDemo().select('id', 'name').take(5).get()        # select `id`,`name` from lh_test limit 5
    # data = ModelDemo().select('min(id) as minid').first()        # select min(id) as minid from lh_test limit 1
    # data = ModelDemo().select('max(id) as maxid').first()        # select max(id) as maxid from lh_test limit 1

    # 返回list
    # data = ModelDemo().select('id', 'name', 'status').lists(['id', 'name'])   # select `id`,`name` from lh_test limit 5
    # data = ModelDemo().select('id', 'name', 'status').data()
    # data = ModelDemo().select('min(id) as minid').first()        # select min(id) as minid from lh_test limit 1

    # groupby
    # select count(*) as num,`name` from lh_test group by `name`
    # data = ModelDemo().select('count(*) as num', 'name').groupby('name').having('num', '>', 2).get()
    # data = ModelDemo().select('distinct(id) as id').lists('id')

    # 原生sql
    # data = ModelDemo().execute('select count(*) as num,`name` from lh_test group by `name`')
    # data = ModelDemo().get()

    # 事务
    # def demo():
    #     data = ModelDemo().where('id', 42).first()
    #     ModelDemo().where('id', 42).update({'name': "555", 'token_name': '555'})
    #     # ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    #     # raise Exception('haha')
    #     return data
    #
    # data = ModelDemo().transaction(demo)
    # print(data)

    # @ModelDemo.transaction
    # def demo(id):
    #     data = ModelDemo().where('id', 42).first()
    #     ModelDemo().where('id', id).update({'name': "444", 'token_name': '444'})
    #     ModelDemo().where('id', 43).update({'name': "44", 'token_name': '444'})
    #     # raise Exception('haha')
    #     return data
    #
    # print(demo(49))

    # data = ModelDemo().database('icoape').where('id', '>', 40).first()
    # print(data)
    # data = ModelDemo().where('id', 62).orwhere({'name': 'haha'}).get()
    # data = ModelDemo().where('id', 1).whereor([{'name': 'haha', 'token_name': 123}, ('token_name', 'like', 'hahe%'), [
    #     ['name', '=', '123'], ['token_name', '=', 333]
    # ]]).get()
    #
    # print(data)
    # exit(0)

    # data = ModelDemo().where('id', 42).orwhere([('name', 'haha%'), ['token_name', '444444'], ['token_name', '!=', '444444']]).orwhere({'id': 43}).get()
    # # data = ModelDemo().where('id', 42).orwhere({'name': 'haha%', 'token_name': '444444'}).get()
    # print(len({'name': 'haha%', 'token_name': '444444'}))
    # print(data)
    # exit(0)
    # print(ModelDemo().lock_for_update().first())
    # print(ModelDemo('a').select('a.id', 'a.name').first())
    # print(ModelDemo('a').select('a.id').take(1).lists('id'))
    # data = ModelDemo('a').where('id', 'in', ModelDemo().where('id', '<=', 50).select('id')).get()

    # data = ModelDemo('a').where('a.id', 42).innerjoin(ModelDemo('b').on('a.id', '=', 'b.id')).select('a.id', 'b.name').get()

    # data = ModelDemo().where('id', 42).union(ModelDemo().where('id', '=', 58)).first()
    # print(data)
    # exit(0)
    # data = ModelDemo().select('id').subquery(ModelDemo().where('id', '=', 42)).get()
    # data = ModelDemo().subquery(
    #     ModelDemo('a').where('a.id', '>=', 58).leftjoin(ModelDemo('b').on('a.id', '=', 'b.id')).select('a.*').orderby('a.id', 'desc').take(2), 'a')\
    #     .where('a.id', '<=', 60).orderby('id', 'desc').get()

    # data = ModelDemo().subquery(ModelDemo('a').where('a.id', '>=', 58), 'a').get()

    # data = ModelDemo('a').where('a.id', '<=', 42).select('a.id', 'b.name').leftjoin(ModelDemo('b').on('a.id', '=', 'b.id')) \
    #     .unionall(ModelDemo().where('id', '=', 58).select('id', 'name').orderby('id', 'desc'))\
    #     .take(5).get()

    # data = ModelDemo().where('id', 10).first()

    # print(data)
    # def change(string):
    #     list_str = string.split('.', 1)
    #     return '.'.join(["`{}`".format(i) if i == list_str[-1] else i for i in list_str])
    #
    # data = ModelDemo('a').first()
    # print(data)
    # model2 = ModelDemo().database('icoape').first()
    # print(model2)
    #
    # print(model1.where('a.id', '>', 43).select('a.id').first())
    # print(model2.first())

    # data = ModelDemo('a').where('FROM_UNIXTIME(create_time, "%Y%m%d%H")', 2019042912).first()

    # data = ModelDemo().having('FROM_UNIXTIME(create_time, "%Y%m%d%H")', 2019042912).offset(1).first()
    # data = ModelDemo().where('create_time', "123").lists('id')
    # print(data)
    # exit(0)
    # subquery1 = ModelDemo('a').where('FROM_UNIXTIME(a.create_time, "%Y%m%d%H")', '=', 2019042913)
    # data = subquery1.leftjoin(
    #     ModelDemo('b').on('a.name', '=', 'b.name').on('a.token_name', '=', 'b.token_name')) \
    #     .where('FROM_UNIXTIME(b.create_time, "%Y%m%d%H")', '=', 2019042912) \
    #     .select('*').data()
    # print(data)
    # model = ModelDemo1()\
    #     .where({'gateway': 'BITFINEX'}).where('time', '>=', '19:38:').select('content', 'time', 'gateway').data()
    # print(model)
    # exit(0)
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
    pass