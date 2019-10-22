#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .Connection import Connection
from ..Util.Logger import logger
import pymongo


class MongoConnection(Connection):

    _connection = {}

    _instance = {}  # 一个库一个instance

    def __init__(self, database, config):
        if config.get('LOG_DIR', None) is not None:
            self._logger = logger.set_path(config.get('LOG_DIR', None))
        self._database = database
        self._config = config

    def get(self, builder):
        if builder.__groupby__.__len__() > 0:
            return self.groupby(builder)
        _select = dict(builder.__select__) if builder.__select__ else None
        model = self.db(builder._tablename()).find(builder.__where__, _select).skip(builder.__offset__).limit(builder.__limit__)
        if builder.__orderby__:
            model = model.sort(builder.__orderby__)
        return list(model)

    def groupby(self, builder):
        aggre = [builder.where_to_match(), builder.__groupby__]
        if builder.__orderby__.__len__() > 0:
            aggre.append(builder._compile_aggregate_orderby())
        if builder.__offset__ > 0:
            aggre.append(builder._compile_aggregate_offset())
        if builder.__limit__ > 0:
            aggre.append(builder._compile_aggregate_limit())
        aggre.append(builder._compile_aggregate_project())
        return self.db(builder._tablename()).aggregate(aggre)

    def create(self, builder, data):
        return self.db(builder._tablename()).insert(data)

    def update(self, builder, data, **kwargs):
        return self.db(builder._tablename()).update_many(builder.__where__, data, **kwargs)

    def delete(self, builder):
        return self.db(builder._tablename()).delete_many(builder.__where__)

    def db(self, tablename):
        return self.connect()[tablename]

    def count(self, builder):
        return self.db(builder._tablename()).find(builder.__where__).count()

    def connect(self):
        if self._connection.get(self._database, None) is None:
            config = self.parse_config(self._config)
            if config['user'] and config['password'] and config['authmechanism']:
                client = pymongo.MongoClient(host=config['host'], port=config['port'], username=config['user'], password=config['password'], authMechanism=config['authmechanism'])
            else:
                client = pymongo.MongoClient(host=config['host'], port=config['port'])
            self._connection[self._database] = client[config['db']]
        return self._connection[self._database]

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database, None) is None:
            cls._instance[database] = MongoConnection(database, config)
        return cls._instance.get(database, None)

    def parse_config(self, config):
        return {
            'host': config.get('DB_HOST', ''),
            'port': int(config.get('DB_PORT', '')),
            'user': config.get('DB_USER', None),
            'password': config.get('DB_PASSWORD', None),
            'db': config.get('DB_NAME', ''),
            'charset': config.get('DB_CHARSET', None),
            'authmechanism': config.get('DB_AUTHMECHANISM', None),
        }
