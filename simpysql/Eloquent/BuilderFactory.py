#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Util.Config import config


class BuilderFactory(object):
    _config = None

    def make(self, model, alias=None):
        self.init_config(model.__basepath__)
        database = model.__database__ if hasattr(model,
                                                 '__database__') and model.__database__ is not None else 'default'
        return self.create_builder(model, self.get_db_type(database), alias)

    def init_config(self, config_path: str) -> None:
        if self._config is None:
            self._config = config.set_basepath(config_path)

    def get_db_type(self, database) -> str:
        config = self._config.items(database)
        return config.get('DB_TYPE', None)

    def create_builder(self, model, db_type, alias):
        if db_type == 'mysql':
            from ..Eloquent.MysqlBuilder import MysqlBuilder
            return MysqlBuilder(model, alias)
        elif db_type == 'mongodb':
            from ..Eloquent.MongoBuilder import MongoBuilder
            return MongoBuilder(model)
        elif db_type == 'sqlserver':
            from ..Eloquent.SqlServerBuilder import SqlServerBuilder
            return SqlServerBuilder(model, alias)
        elif db_type == 'postgres':
            from ..Eloquent.PostgresBuilder import PostgresBuilder
            return PostgresBuilder(model, alias)
        raise Exception('Unsupported driver {}'.format(db_type))


builderfactory = BuilderFactory()
