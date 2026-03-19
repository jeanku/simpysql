#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试模型定义
所有测试用例共用的 Model 类
"""

import os
import sys
# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from simpysql.DBModel import DBModel


class BaseModel(DBModel):
    """基础模型类"""
    __basepath__ = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/'


class User(BaseModel):
    """用户模型 - 测试基本CRUD操作"""
    __tablename__ = 'test_users'
    __create_time__ = 'created_at'
    __update_time__ = 'updated_at'
    
    columns = [
        'id',
        'name',
        'email',
        'age',
        'status',
        'score',
        'created_at',
        'updated_at',
    ]


class Order(BaseModel):
    """订单模型 - 测试关联查询"""
    __tablename__ = 'test_orders'
    __create_time__ = 'created_at'
    __update_time__ = 'updated_at'
    
    columns = [
        'id',
        'user_id',
        'order_no',
        'amount',
        'status',
        'created_at',
        'updated_at',
    ]


class Product(BaseModel):
    """商品模型 - 测试关联查询"""
    __tablename__ = 'test_products'
    __create_time__ = 'created_at'
    __update_time__ = 'updated_at'
    
    columns = [
        'id',
        'name',
        'price',
        'stock',
        'status',
        'created_at',
        'updated_at',
    ]


class Article(BaseModel):
    """文章模型 - 测试LIKE搜索和文本操作"""
    __tablename__ = 'test_articles'
    __create_time__ = 'created_at'
    __update_time__ = 'updated_at'
    
    columns = [
        'id',
        'title',
        'content',
        'author_id',
        'view_count',
        'status',
        'created_at',
        'updated_at',
    ]
