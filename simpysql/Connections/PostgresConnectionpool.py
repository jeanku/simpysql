import psycopg2.pool


class Connectionpool():
    _pool = {}

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connectionpool, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def connection(self, pro_db_config, database):
        if self._pool.get(database, None) is None:
            self._pool[database] = psycopg2.pool.ThreadedConnectionPool(
                minconn=5,
                maxconn=50,
                **pro_db_config
            )

        return self._pool[database].getconn()


connectionpool = Connectionpool()
