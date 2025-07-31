#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import RoundRobinPolicy
from cassandra.cluster import Cluster
from cassandra.connection import ssl
import threading
import queue

class CassandraConnectionPool:
    def __init__(self, config):
        pool_size = int(config.get('POOL_SIZE', 1))
        self.hosts = config['DB_HOST'].split(",")
        self.keyspace = config['DB_KEYSPACE']
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size)
        self.username = config.get('DB_USER')
        self.password = config.get('DB_PASSWORD')
        self.cluster = None
        self._initialized = False
        self._lock = threading.Lock()
        self._config = config

    def _initialize_pool(self):
        if self._initialized:
            return
        auth_provider = None
        if self.username and self.password:
            auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)

        self.cluster = Cluster(
            contact_points=self.hosts,
            load_balancing_policy=RoundRobinPolicy(),
            auth_provider=auth_provider,
            port=int(self._config.get('DB_PORT', 9042)),
            ssl_options=self._get_ssl_options()
        )

        for _ in range(self.pool_size):
            session = self.cluster.connect(self.keyspace)
            self.pool.put(session)

        self._initialized = True

    def _get_ssl_options(self):
        ssl_options = None
        if self._config.get('SSL_CA_CERTS'):
            ssl_options = {
                'ca_certs': self._config['SSL_CA_CERTS'],
                'ssl_version': ssl.PROTOCOL_TLSv1_2,
                'certfile': self._config.get('SSL_CERTFILE'),
                'keyfile': self._config.get('SSL_KEYFILE')
            }
        return ssl_options

    def get_session(self):
        self._initialize_pool()
        session = self.pool.get()
        self.pool.put(session)
        return session

    def return_session(self, session):
        self.pool.put(session)

    def shutdown(self):
        if self.cluster:
            while not self.pool.empty():
                session = self.pool.get()
                session.shutdown()
            self.cluster.shutdown()