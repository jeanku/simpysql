#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .CassandraConnectionpool import CassandraConnectionPool
from cassandra.query import SimpleStatement
from cassandra.query import BatchStatement
from .Connection import Connection
from ..Util.Logger import logger
import threading


class CassandraConnection(Connection):
    _connection_pool = None
    _instance = {}
    _lock = threading.Lock()

    def __init__(self, database, config):
        self._logger = None
        if config.get('LOG_DIR', None) is not None:
            self._logger = logger.set_path(config['LOG_DIR'])
        self._database = database
        self._config = config
        if CassandraConnection._connection_pool is None:
            self._connection_pool = CassandraConnectionPool(config)

    def execute(self, sql):
        self.log(sql)
        rows = self.connect().execute(sql)
        return [dict(row._asdict()) for row in rows]

    async def execute_async(self, sqls, callback=None, error_callback=None):
        for sql in sqls:
            statement = SimpleStatement(sql)
            future = self.connect().execute_async(statement)
            future.add_callbacks(callback, error_callback)

    def execute_batch(self, sqls):
        batch = BatchStatement()
        for sql in sqls:
            self.log("batch sql:{}".format(sql))
            batch.add(sql, ())
        rows = self.connect().execute(batch)
        return [dict(row._asdict()) for row in rows]

    def connect(self):
        return self._connection_pool.get_session()

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database) is None:
            with cls._lock:
                if cls._instance.get(database) is None:
                    cls._instance[database] = CassandraConnection(database, config)
        return cls._instance[database]