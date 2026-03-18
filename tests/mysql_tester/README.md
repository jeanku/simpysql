# simpysql MySQL 测试套件

本测试套件用于测试 simpysql 库的所有 MySQL 相关方法。

## 测试环境要求

- Python 3.6+
- pytest
- pymysql
- pandas (可选，用于 data() 方法)
- python-dotenv

- MySQL 数据库

## 安装

1. 安装依赖:
```bash
pip install pytest pymysql pandas python-dotenv
```

2. 配置数据库连接:
   复制 `.env.example` 为 `.env` 并修改数据库配置:
   ```bash
   cp .env.example . .env
   ```

3. 初始化测试数据库:
   执行 `sql/init_tables.sql` 脚本创建测试表和初始数据
   ```bash
   mysql -u root -p < your_mysql_test_db < sql/init_tables.sql
   ```

## 运行测试

```bash
# 运行所有测试
pytest -v --tb=short

# 运行特定测试文件
pytest tests/mysqlDemo/test_select.py
pytest tests/mysqlDemo/test_where.py
pytest tests/mysqlDemo/test_create.py
pytest tests/mysqlDemo/test_update.py
pytest tests/mysqlDemo/test_delete.py
pytest tests/mysqlDemo/test_aggregate.py
pytest tests/mysqlDemo/test_join.py
pytest tests/mysqlDemo/test_union.py
pytest tests/mysqlDemo/test_subquery.py
pytest tests/mysqlDemo/test_transaction.py
pytest tests/mysqlDemo/test_response.py
pytest tests/mysqlDemo/test_lock.py
pytest tests/mysqlDemo/test_state_pollution.py

# 运行带标记的测试
pytest -v -m select tests/mysqlDemo/test_select.py
pytest -v -m where tests/mysqlDemo/test_where.py
pytest -v -m create tests/mysqlDemo/test_create.py
pytest -v -m update tests/mysqlDemo/test_update.py
pytest -v -m delete tests/mysqlDemo/test_delete.py
pytest -v -m aggregate tests/mysqlDemo/test_aggregate.py
pytest -v -m join tests/mysqlDemo/test_join.py
pytest -v -m union tests/mysqlDemo/test_union.py
pytest -v -m subquery tests/mysqlDemo/test_subquery.py
pytest -v -m transaction tests/mysqlDemo/test_transaction.py
pytest -v -m response tests/mysqlDemo/test_response.py
pytest -v -m lock tests/mysqlDemo/test_lock.py
pytest -v -m state tests/mysqlDemo/test_state_pollution.py

# 运行快速测试
pytest -v -n --tb=short tests/mysqlDemo/test_select.py
pytest -v -n --tb=short tests/mysqlDemo/test_where.py

# 只运行状态污染测试
pytest -v -n --tb=short tests/mysqlDemo/test_state_pollution.py
```

