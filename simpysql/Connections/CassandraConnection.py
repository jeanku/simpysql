#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Connection import Connection
from ..Util.Logger import logger
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import NoHostAvailable
from cassandra.policies import RoundRobinPolicy
from cassandra.connection import ssl
import threading


class CassandraConnection(Connection):
    _connection = {}
    _instance = {}
    _lock = threading.Lock()

    def __init__(self, database, config):
        self._logger = None
        if config.get('LOG_DIR', None) is not None:
            self._logger = logger.set_path(config['LOG_DIR'])
        self._database = database
        self._config = config

    def execute(self, sql):
        self.log(sql)
        return self.connect().execute(sql)

    def connect(self):
        if self._connection.get(self._database) is None:
            with self._lock:
                if self._connection.get(self._database) is None:
                    auth_provider = PlainTextAuthProvider(
                        username=self._config['DB_USER'],
                        password=self._config['DB_PASSWORD']
                    )

                    ssl_options = None
                    if self._config.get('SSL_CA_CERTS'):
                        ssl_options = {
                            'ca_certs': self._config['SSL_CA_CERTS'],
                            'ssl_version': ssl.PROTOCOL_TLSv1_2,
                            'certfile': self._config.get('SSL_CERTFILE'),
                            'keyfile': self._config.get('SSL_KEYFILE')
                        }

                    try:
                        cluster = Cluster(
                            self._config['DB_HOST'].split(","),
                            port=int(self._config.get('DB_PORT', 9042)),
                            auth_provider=auth_provider,
                            load_balancing_policy=RoundRobinPolicy(),
                            ssl_options=ssl_options
                        )
                        session = cluster.connect()
                        session.set_keyspace(self._config['DB_KEYSPACE'])
                        self._connection[self._database] = session
                    except NoHostAvailable as e:
                        if self._logger:
                            self._logger.error(f"Could not connect to Cassandra: {e}")
                        raise
        return self._connection[self._database]

    @classmethod
    def instance(cls, database, config):
        if cls._instance.get(database) is None:
            with cls._lock:
                if cls._instance.get(database) is None:
                    cls._instance[database] = CassandraConnection(database, config)
        return cls._instance[database]