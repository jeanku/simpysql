## Install

Via pip

``` bash
 pip install hangsql
```


# initialization
you need to create a .env file at your project root path, and content as follows:
``` bash
[default]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db1
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
LOG_DIR=/home/logs/python/

[other_db]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=test_db2
DB_USER=root
DB_PASSWORD=123456
DB_CHARSET=utf8mb4
LOG_DIR=/home/logs/python/
```
