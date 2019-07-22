#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Connection import Connection
from functools import wraps
from ..Util.Logger import logger
import pymssql


class SqlServerConnection(Connection):
    _connection = {}

    _instance = {}  # 一个库一个instance

    def __init__(self, database, config):
        if config.get('LOG_DIR', None) is not None:
            self._logger = logger.set_path(config.get('LOG_DIR', None))
        self._database = database
        self._config = config

    def execute(self, sql):
        self.log(sql)
        cursor = self.connect().cursor(as_dict=True)
        cursor.execute(sql)
        data = cursor.fetchall()
        if not hasattr(self, '_transaction'):
            self.connect().commit()
        cursor.close()
        return data

    def transaction(self, callback):
        try:
            self.start()
            result = callback()
            self.connect().commit()
            self.end()
            return result
        except Exception as e:
            self.connect().rollback()
            self.end()
            raise e

    def transaction_wrapper(self, callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            try:
                self.start()
                result = callback(*args, **kwargs)
                self.connect().commit()
                self.end()
                return result
            except Exception as e:
                self.connect().rollback()
                self.end()
                raise e

        return wrapper

    def connect(self):
        if self._connection.get(self._database, None) is None:
            config = self.parse_config(self._config)
            self._connection[self._database] = pymssql.connect(config['host'], config['user'], config['password'], config['db'])
        return self._connection[self._database]

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database, None) is None:
            cls._instance[database] = SqlServerConnection(database, config)
        return cls._instance.get(database, None)

    def start(self):
        self._transaction = True

    def end(self):
        del self._transaction

    def parse_config(self, config):
        return {
            'host': config.get('DB_HOST', ''),
            'port': int(config.get('DB_PORT', '')),
            'user': config.get('DB_USER', ''),
            'password': config.get('DB_PASSWORD', ''),
            'db': config.get('DB_NAME', ''),
            'charset': config.get('DB_CHARSET', ''),
        }
