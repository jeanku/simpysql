#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

import time

from tests.mysqlDemo.BaseModel import BaseModel
import asyncio

class ModelDemo(BaseModel):

    __database__ = "community"

    __tablename__ = 'tx'  # 表名

    # __create_time__ =   # 插入时间字段 如果该字段为None create_time则不会自动添加

    # __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        'from_addr',
        'to_addr',
        'hash_code',
        'amount',
        'height',
    ]

class ModelDemo1(BaseModel):

    __database__ = "kasplex"

    __tablename__ = 'teststtoken'  # 表名

    # __create_time__ =   # 插入时间字段 如果该字段为None create_time则不会自动添加

    # __update_time__ = 'update_time'  # 更新时间字段 如果该字段为None create_time则不会自动添加

    columns = [  # 数据库字段
        'prefix2',
        'tick',
    ]


if __name__ == '__main__':

    # 添加单个数据
    # sql: insert into tx ("from_addr", "to_addr", "hash_code", "amount", "height") values ('qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d3', 'cy3dfs9dc3w7lm9rq0zs76vf959mmrp3', 'hashcode22', 104, 86400)
    # ModelDemo.create({
    #     'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d3",
    #     'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp3",
    #     'hash_code': 'hashcode22',
    #     'amount': 104,
    #     'height': 86400,
    # })

    # 添加多个数据
    # data = ModelDemo.create([{
    #     'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
    #     'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp",
    #     'hash_code': 'hashcode22',
    #     'amount': 100,
    #     'height': 86400,
    # },{
    #     'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1",
    #     'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp1",
    #     'hash_code': 'hashcode',
    #     'amount': 100,
    #     'height': 86400,
    # },{
    #     'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1",
    #     'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp2",
    #     'hash_code': 'hashcode',
    #     'amount': 102,
    #     'height': 86400,
    # }, {
    #     'from_addr': "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2",
    #     'to_addr': "cy3dfs9dc3w7lm9rq0zs76vf959mmrp2",
    #     'hash_code': 'hashcode',
    #     'amount': 103,
    #     'height': 86400,
    # }])

    # update
    # sql: update tx set "amount"=999 where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2' and "hash_code"='hashcode'
    # data = ModelDemo.where("from_addr", "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2").where("hash_code", "hashcode").update({"amount": 999})
    # data = ModelDemo.where({
    #     "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2",
    #     "hash_code": "hashcode"
    # }).update({"amount": 998})

    # delete
    # sql: delete from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1' and "hash_code"='hashcode'
    # data = ModelDemo.where({
    #     "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d1",
    #     "hash_code": "hashcode"
    # }).delete()

    # 查询 select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2' and "hash_code"='hashcode' limit 1
    # data = ModelDemo.where({
    #     "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d221",
    #     "hash_code": "hashcode"
    # }).get()

    # sql: select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2'
    # data = ModelDemo.where({
    #     "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
    # }).get()

    # sql: select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d' order by "hash_code" limit 10
    # data = ModelDemo.where({
    #     "from_addr": "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d",
    # }).take(10).orderby("hash_code").get()

    # select
    # sql: select "hash_code","from_addr" from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' limit 2
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").select("hash_code", "from_addr").take(2).get()

    # sql = 'select * from tx where "from_addr"=\'qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp\' order by "hash_code" ASC limit 5'
    # data = ModelDemo.execute(sql)


    # select * from lh_test where id=62 or id=63
    # select * from tx where "from_addr"='qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp' limit 5
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").take(5).lists("hash_code")

    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").take(2).pluck("hash_code", "amount")
    # print(data)
    # exit(0)
    # data = ModelDemo.where('from_addr', '>', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").allow_filtering().pluck("hash_code", "amount")
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").count()
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").count()


    # data = ModelDemo1.where('prefix2', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").take(1).get()
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").where("hash_code", "420223c3d63356b2073ce588dd9d3159").get()
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").where("hash_code", "420223c3d63356b2073ce588dd9d3159").get()
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").where("hash_code", "420223c3d63356b2073ce588dd9d3159").get()
    # data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").where("hash_code", "420223c3d63356b2073ce588dd9d3159").get()

    # print("1", data)
    # data = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp"]).select("from_addr as name")
    # data2 = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d2"]).select("from_addr as name")
    # ModelDemo.batch([data, data2])
    # print(data)
    # exit(0)
    # from datetime import datetime
    # start_time = datetime.now()
    # for i in range(10000 ):
    #     data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").select("from_addr as name").first()
    #     print(data)
    #
    # end_time = datetime.now()
    #
    # execution_time = end_time - start_time
    # print(f"Execution time: {execution_time}")

    from multiprocessing import Pool
    import time


    def worker(num):
        """模拟一个耗时的任务"""
        print(f"Worker {num} started")
        time.sleep(2)  # 模拟耗时操作
        # for i in range(2500):
        #     data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").select(
        #         "from_addr as name").first()
        #     print(data)
        print(f"Worker {num} finished")
        return f"Result from worker {num}"


    with Pool(processes=4) as pool:
        # 使用map函数并行处理任务
        results = pool.map(worker, range(10))

        # 输出每个工作进程的结果
    for result in results:
        print(result)


    # async def async_run(p):
    #     data = await ModelDemo.where('from_addr', p).async_get()
    #     print(data)

    # p = ['qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp', 'qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp', 'qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp', 'qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp']
    # def callback(rows):
    #     for row in rows:
    #         print("row:", dict(row._asdict()))
    #
    # def error_callback(err):
    #     print("error", err)
    #
    # async def run():
    #     m1 = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp"])
    #     m2 = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d"]).select("from_addr as name")
    #     m3 = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d3"]).select("from_addr as name")
    #     m4 = ModelDemo.where('from_addr', "in", ["qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9d4"]).select("from_addr as name")
    #     await ModelDemo.excute_async([m1, m2, m3, m4], callback, error_callback)
    #
    # #
    # asyncio.run(run())
    # time.sleep(10)
    # print(1123123)
    # asyncio.run(run())
    # # print("2", data)
    # exit(0)
