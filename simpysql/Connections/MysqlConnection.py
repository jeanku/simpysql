#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .MysqlConnectionpool import connectionpool
from .Connection import Connection
from functools import wraps
from ..Util.Logger import logger
import threading  # 引入 threading 解决事务的线程安全问题


class MysqlConnection(Connection):
    _instance = {}

    def __init__(self, database, config):
        if config.get('LOG_DIR', None) is not None:
            self._logger = logger.set_path(config.get('LOG_DIR', None))
        self._database = database
        self._config = config
        # 使用 threading.local 保证每个线程拥有独立的事务连接标识
        self._local = threading.local()

    # 获取一个新的连接池连接
    def _get_pool_connection(self):
        return connectionpool.connection(self.parse_config(self._config), self._database)

    def execute(self, sql, cursorclass=None):
        self.log(sql)

        # 判断当前线程是否在事务中，如果在，复用事务连接；如果不在，从池里拿新连接
        in_transaction = getattr(self._local, 'transaction_conn', None) is not None
        conn = self._local.transaction_conn if in_transaction else self._get_pool_connection()

        try:
            cursor = conn.cursor(cursor=cursorclass)
            affected_rows = cursor.execute(sql)

            # 区分查询与修改的返回值 (上一轮的修复)
            if sql.strip().lower().startswith(('select', 'show', 'desc', 'explain')):
                data = cursor.fetchall()
            else:
                data = affected_rows

            # 非事务状态下，单条语句执行完立即 commit
            if not in_transaction:
                conn.commit()

            cursor.close()
            return data

        finally:
            # 如果不在事务中，用完立刻归还（关闭）连接
            if not in_transaction:
                conn.close()

    def transaction(self, callback):
        # 事务开始前，从连接池获取一个专属连接，并绑定到当前线程
        conn = self._get_pool_connection()
        self._local.transaction_conn = conn
        try:
            result = callback()
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            # 事务结束，解绑线程变量，并归还连接给连接池
            conn.close()
            self._local.transaction_conn = None

    def transaction_wrapper(self, callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            conn = self._get_pool_connection()
            self._local.transaction_conn = conn
            try:
                result = callback(*args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()
                self._local.transaction_conn = None

        return wrapper

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database, None) is None:
            cls._instance[database] = MysqlConnection(database, config)
        return cls._instance.get(database, None)

    def parse_config(self, config):
        return {
            'host': config.get('DB_HOST', ''),
            'port': int(config.get('DB_PORT', '')),
            'user': config.get('DB_USER', ''),
            'password': config.get('DB_PASSWORD', ''),
            'db': config.get('DB_NAME', ''),
            'charset': config.get('DB_CHARSET', ''),
        }
