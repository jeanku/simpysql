#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 pytest 配置文件
定义测试夹具和钩子函数
"""

import pytest
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.mysql_tester.models import User, Order, Product, Article


# =====================================================
# 测试夹具 (Fixtures)
# =====================================================

@pytest.fixture
def user_model():
    """用户模型夹具"""
    return User


@pytest.fixture
def order_model():
    """订单模型夹具"""
    return Order


@pytest.fixture
def product_model():
    """商品模型夹具"""
    return Product


@pytest.fixture
def article_model():
    """文章模型夹具"""
    return Article


@pytest.fixture
def clean_users(user_model):
    """清理用户表并重置自增ID"""
    # 测试前清理
    user_model.execute('TRUNCATE TABLE test_users')
    yield user_model
    # 测试后清理
    user_model.execute('TRUNCATE TABLE test_users')


@pytest.fixture
def clean_orders(order_model):
    """清理订单表并重置自增ID"""
    order_model.execute('TRUNCATE TABLE test_orders')
    yield order_model
    order_model.execute('TRUNCATE TABLE test_orders')


@pytest.fixture
def clean_products(product_model):
    """清理商品表并重置自增ID"""
    product_model.execute('TRUNCATE TABLE test_products')
    yield product_model
    product_model.execute('TRUNCATE TABLE test_products')


@pytest.fixture
def clean_articles(article_model):
    """清理文章表并重置自增ID"""
    article_model.execute('TRUNCATE TABLE test_articles')
    yield article_model
    article_model.execute('TRUNCATE TABLE test_articles')


@pytest.fixture
def sample_user_data():
    """示例用户数据"""
    return {
        'name': '测试用户',
        'email': 'test@example.com',
        'age': 25,
        'status': 1,
        'score': 85.5
    }


@pytest.fixture
def sample_order_data():
    """示例订单数据"""
    return {
        'user_id': 1,
        'order_no': 'TEST001',
        'amount': 199.99,
        'status': 0
    }


@pytest.fixture
def sample_product_data():
    """示例商品数据"""
    return {
        'name': '测试商品',
        'price': 99.99,
        'stock': 100,
        'status': 1
    }


@pytest.fixture
def sample_article_data():
    """示例文章数据"""
    return {
        'title': '测试文章标题',
        'content': '这是测试文章的内容...',
        'author_id': 1,
        'view_count': 0,
        'status': 1
    }


@pytest.fixture
def batch_user_data():
    """批量用户数据"""
    return [
        {'name': '用户A', 'email': 'a@test.com', 'age': 20, 'status': 1, 'score': 80.0},
        {'name': '用户B', 'email': 'b@test.com', 'age': 25, 'status': 1, 'score': 85.0},
        {'name': '用户C', 'email': 'c@test.com', 'age': 30, 'status': 0, 'score': 90.0},
    ]


# =====================================================
# pytest 钩子函数
# =====================================================

def pytest_configure(config):
    """pytest 配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "select: 测试 SELECT 查询相关方法"
    )
    config.addinivalue_line(
        "markers", "where: 测试 WHERE 条件查询方法"
    )
    config.addinivalue_line(
        "markers", "create: 测试 INSERT 插入方法"
    )
    config.addinivalue_line(
        "markers", "update: 测试 UPDATE 更新方法"
    )
    config.addinivalue_line(
        "markers", "delete: 测试 DELETE 删除方法"
    )
    config.addinivalue_line(
        "markers", "aggregate: 测试聚合函数方法"
    )
    config.addinivalue_line(
        "markers", "join: 测试 JOIN 关联查询方法"
    )
    config.addinivalue_line(
        "markers", "union: 测试 UNION 联合查询方法"
    )
    config.addinivalue_line(
        "markers", "subquery: 测试子查询方法"
    )
    config.addinivalue_line(
        "markers", "transaction: 测试事务方法"
    )
    config.addinivalue_line(
        "markers", "response: 测试响应格式方法"
    )
    config.addinivalue_line(
        "markers", "lock: 测试锁方法"
    )
    config.addinivalue_line(
        "markers", "state: 测试状态污染"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试"
    )


def pytest_collection_modifyitems(config, items):
    """测试收集修改钩子"""
    # 为没有标记的测试添加默认标记
    for item in items:
        if not list(item.iter_markers()):
            item.add_marker(pytest.mark.mysql)
