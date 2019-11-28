#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Util.Config import config


class ConnectionFactory(object):
    _config = None

    def make(self, database, config_path):
        self.init_config(config_path)
        db_type = self.get_db_type(database)
        return self.create_connection(db_type, database)

    def init_config(self, config_path: str) -> None:
        if self._config is None:
            self._config = config.set_basepath(config_path)

    def get_db_type(self, database) -> str:
        config = self._config.items(database)
        return config.get('DB_TYPE', None)

    def create_connection(self, db_type, database: str):
        if db_type == 'mysql':
            from .MysqlConnection import MysqlConnection
            return MysqlConnection.instance(database, self.parse_config(database))
        elif db_type == 'mongodb':
            from .MongoConnection import MongoConnection
            return MongoConnection.instance(database, self.parse_config(database))
        elif db_type == 'sqlserver':
            from .SqlServerConnection import SqlServerConnection
            return SqlServerConnection.instance(database, self.parse_config(database))
        elif db_type == 'postgres':
            from .PostgresConnection import PostgresConnection
            return PostgresConnection.instance(database, self.parse_config(database))
        raise Exception('Unsupported driver {}'.format(database))

    def parse_config(self, database):
        return self._config.items(database)


connfactory = ConnectionFactory()
