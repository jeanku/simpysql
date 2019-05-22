#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from .Connectionpool import connectionpool
from .Logger import logger
from .Config import config
from functools import wraps


class Connection(object):
    _connection = {}

    _logger = False

    def execute(self, sql, cursorclass=None):
        self.log(sql)
        # exit(0)
        cursor = self.connect().cursor(cursor=cursorclass)
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
            pro_db_config = self.config()
            self._connection[self._database] = connectionpool.connection(pro_db_config, self._database)
        return self._connection[self._database]

    def set_config(self, path, database='default'):
        config.set_basepath(path)
        self._database = database

    def set_database(self, database):
        self._database = database

    def config(self):
        data = config.items(self._database)
        return {
            'host': data.get('DB_HOST', ''),
            'port': int(data.get('DB_PORT', '')),
            'user': data.get('DB_USER', ''),
            'password': data.get('DB_PASSWORD', ''),
            'db': data.get('DB_NAME', ''),
            'charset': data.get('DB_CHARSET', ''),
        }

    def start(self):
        self._transaction = True

    def end(self):
        del self._transaction

    def log(self, sql):
        if self._logger:
            self._logger.info('【sql】:{}'.format(sql))
        else:
            path = config.items(self._database).get('LOG_DIR', None)
            if path is not None:
                self._logger = logger.set_path(path)
                self._logger.info('【sql】:{}'.format(sql))


connection = Connection()
