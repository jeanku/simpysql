#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - LOCK 锁方法
测试方法: lock_for_update, lock_for_share
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestLockForUpdate:
    """测试 lock_for_update() 方法"""
    
    @pytest.mark.lock
    def test_lock_for_update_sql(self, user_model):
        """测试 lock_for_update SQL 生成"""
        sql = user_model.lock_for_update().tosql()
        
        assert 'for update' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_for_update_with_where(self, clean_users):
        """测试带 WHERE 条件的 lock_for_update"""
        # 插入测试数据
        clean_users.create({'name': 'LockUpdateTest', 'email': 'lockupdate@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        sql = clean_users.where('name', 'LockUpdateTest').lock_for_update().tosql()
        
        assert 'for update' in sql.lower()
        assert 'where' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_for_update_returns_builder(self, user_model):
        """测试 lock_for_update 返回 builder"""
        builder = user_model.lock_for_update()
        
        assert builder is not None
        # 验证可以链式调用
        builder2 = builder.where('id', 1)
        assert builder2 is not None


class TestLockForShare:
    """测试 lock_for_share() 方法"""
    
    @pytest.mark.lock
    def test_lock_for_share_sql(self, user_model):
        """测试 lock_for_share SQL 生成"""
        sql = user_model.lock_for_share().tosql()
        
        assert 'lock in share mode' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_for_share_with_where(self, clean_users):
        """测试带 WHERE 条件的 lock_for_share"""
        # 插入测试数据
        clean_users.create({'name': 'LockShareTest', 'email': 'lockshare@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        sql = clean_users.where('name', 'LockShareTest').lock_for_share().tosql()
        
        assert 'lock in share mode' in sql.lower()
        assert 'where' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_for_share_returns_builder(self, user_model):
        """测试 lock_for_share 返回 builder"""
        builder = user_model.lock_for_share()
        
        assert builder is not None
        # 验证可以链式调用
        builder2 = builder.where('id', 1)
        assert builder2 is not None


class TestLockCombined:
    """测试锁组合使用"""
    
    @pytest.mark.lock
    def test_lock_for_update_with_limit(self, clean_users):
        """测试 lock_for_update 配合 LIMIT"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'LockUpdateLimit{i}', 'email': f'lockupdatelimit{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        sql = clean_users.where('name', 'like', 'LockUpdateLimit%').take(2).lock_for_update().tosql()
        
        assert 'for update' in sql.lower()
        assert 'limit 2' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_for_share_with_orderby(self, clean_users):
        """测试 lock_for_share 配合 ORDER BY"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'LockShareOrder{i}', 'email': f'lockshareorder{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        sql = clean_users.where('name', 'like', 'LockShareOrder%').orderby('id', 'desc').lock_for_share().tosql()
        
        assert 'lock in share mode' in sql.lower()
        assert 'order by' in sql.lower()
    
    @pytest.mark.lock
    def test_lock_methods_chainable(self, user_model):
        """测试锁方法可以链式调用"""
        builder = user_model.lock_for_update()
        
        # 验证可以继续链式调用其他方法
        builder2 = builder.where('id', 1).select('id', 'name')
        
        assert builder2 is not None
