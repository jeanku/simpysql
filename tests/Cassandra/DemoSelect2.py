#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""model类"""

__author__ = ''

import time

from tests.mysqlDemo.BaseModel import BaseModel
from multiprocessing import Pool
from datetime import datetime

class ModelDemo(BaseModel):

    __database__ = "community"

    __tablename__ = 'tx'  # 表名

    columns = [  # 数据库字段
        'from_addr',
        'to_addr',
        'hash_code',
        'amount',
        'height',
    ]

class DynamicPoolManager:
    def __init__(self, processes):
        self.pool = Pool(processes=processes)

    def submit_task(self, func, *args):
        """提交任务到进程池"""
        return self.pool.apply_async(func, args=args)

    def close(self):
        """关闭进程池"""
        self.pool.close()
        self.pool.join()

def worker(num):
    """模拟一个耗时的任务"""
    print(f"Worker {num} started")
    r = []
    for i in range(2):
        data = ModelDemo.where('from_addr', "qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp").select(
            "from_addr as name").first()
        r.append(data)
    print(f"Worker {num} finished")
    return r

def main():
    # 创建进程池管理器
    pool_manager = DynamicPoolManager(processes=2)

    async_results = []

    for i in range(1):
        async_result = pool_manager.submit_task(worker, i)
        async_results.append(async_result)

    # 获取结果
    results = [async_result.get() for async_result in async_results]
    print(f"Results: {results}")

    for _ in range(20):
        print("sleeping  ........................ \n\n\n\n\n\n")
        for i in range(1):
            async_result = pool_manager.submit_task(worker, i)
            async_results.append(async_result)

            # 获取结果
        results = [async_result.get() for async_result in async_results]
        print(f"Results222222: {results}")


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time}")


