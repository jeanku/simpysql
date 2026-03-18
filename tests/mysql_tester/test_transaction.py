#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 事务方法
测试方法: transaction, transaction_wrapper
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestTransaction:
    """测试 transaction() 方法"""
    
    @pytest.mark.transaction
    def test_transaction_commit(self, clean_users):
        """测试事务提交"""
        def create_user():
            clean_users.create({'name': 'TransactionCommit', 'email': 'transcommit@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            return True
        
        result = clean_users.transaction(create_user)
        assert result is True
        
        # 验证数据已提交
        user = clean_users.where('name', 'TransactionCommit').first()
        assert user is not None
    
    @pytest.mark.transaction
    def test_transaction_rollback(self, clean_users):
        """测试事务回滚"""
        # 先插入一条数据
        clean_users.create({'name': 'BeforeRollback', 'email': 'before@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        def failed_operation():
            # 更新数据
            clean_users.where('name', 'BeforeRollback').update({'age': 100})
            # 然后抛出异常
            raise Exception('Intentional rollback test')
        
        # 事务应该捕获异常并回滚
        with pytest.raises(Exception):
            clean_users.transaction(failed_operation)
        
        # 验证数据已回滚
        user = clean_users.where('name', 'BeforeRollback').first()
        age = user['age'] if isinstance(user, dict) else user.age
        assert age == 25  # 应该是原始值，不是100
    
    @pytest.mark.transaction
    def test_transaction_multiple_operations(self, clean_users):
        """测试事务中多个操作"""
        def multiple_operations():
            clean_users.create({'name': 'MultiOp1', 'email': 'multi1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            clean_users.create({'name': 'MultiOp2', 'email': 'multi2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
            clean_users.where('name', 'MultiOp1').update({'age': 26})
            return True
        
        result = clean_users.transaction(multiple_operations)
        assert result is True
        
        # 验证所有操作都已提交
        count = clean_users.where('name', 'like', 'MultiOp%').count()
        assert count == 2
        
        user1 = clean_users.where('name', 'MultiOp1').first()
        age = user1['age'] if isinstance(user1, dict) else user1.age
        assert age == 26
    
    @pytest.mark.transaction
    def test_transaction_return_value(self, clean_users):
        """测试事务返回值"""
        def get_user_count():
            clean_users.create({'name': 'ReturnTest', 'email': 'return@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            return clean_users.count()
        
        result = clean_users.transaction(get_user_count)
        assert result >= 1
    
    @pytest.mark.transaction
    def test_transaction_with_closure(self, clean_users):
        """测试事务闭包捕获变量"""
        name = 'ClosureTest'
        
        def create_user_with_name():
            clean_users.create({'name': name, 'email': f'{name.lower()}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            return name
        
        result = clean_users.transaction(create_user_with_name)
        assert result == name


class TestTransactionWrapper:
    """测试 transaction_wrapper() 方法"""
    
    @pytest.mark.transaction
    def test_transaction_wrapper_commit(self, clean_users):
        """测试 transaction_wrapper 提交"""
        def create_user():
            clean_users.create({'name': 'WrapperCommit', 'email': 'wrapper@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            return True
        
        result = clean_users.transaction_wrapper(create_user)
        assert result is True
        
        # 验证数据已提交
        user = clean_users.where('name', 'WrapperCommit').first()
        assert user is not None
    
    @pytest.mark.transaction
    def test_transaction_wrapper_rollback(self, clean_users):
        """测试 transaction_wrapper 回滚"""
        def failed_operation():
            clean_users.create({'name': 'WrapperRollback', 'email': 'wrapper@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            raise Exception('Intentional rollback')
        
        with pytest.raises(Exception):
            clean_users.transaction_wrapper(failed_operation)
        
        # 验证数据已回滚
        user = clean_users.where('name', 'WrapperRollback').first()
        assert user is None or user == {}


class TestTransactionClassMethod:
    """测试类级别的 transaction 方法"""
    
    @pytest.mark.transaction
    def test_class_transaction_decorator(self, user_model):
        """测试类级别 transaction 方法存在"""
        # 验证类有 transaction 方法
        assert hasattr(user_model, 'transaction')


class TestTransactionExceptions:
    """测试事务异常处理"""
    
    @pytest.mark.transaction
    def test_transaction_with_division_error(self, clean_users):
        """测试事务中的除零错误"""
        def division_error():
            clean_users.create({'name': 'DivError', 'email': 'diverror@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            x = 1 / 0  # 除零错误
            return x
        
        with pytest.raises(Exception):
            clean_users.transaction(division_error)
        
        # 验证数据已回滚
        user = clean_users.where('name', 'DivError').first()
        assert user is None or user == {}
    
    @pytest.mark.transaction
    def test_transaction_with_key_error(self, clean_users):
        """测试事务中的键错误"""
        def key_error():
            clean_users.create({'name': 'KeyError', 'email': 'keyerror@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            d = {}
            return d['non_existent_key']  # 键错误
        
        with pytest.raises(Exception):
            clean_users.transaction(key_error)
        
        # 验证数据已回滚
        user = clean_users.where('name', 'KeyError').first()
        assert user is None or user == {}


class TestTransactionComplex:
    """测试复杂事务场景"""
    
    @pytest.mark.transaction
    def test_transaction_select_and_update(self, clean_users):
        """测试事务中的查询和更新操作"""
        def select_and_update():
            # 先插入
            clean_users.create({'name': 'SelectUpdate', 'email': 'selectupdate@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            # 查询
            user = clean_users.where('name', 'SelectUpdate').first()
            # 更新
            clean_users.where('name', 'SelectUpdate').update({'age': 30})
            return True
        
        result = clean_users.transaction(select_and_update)
        assert result is True
        
        # 验证最终状态
        user = clean_users.where('name', 'SelectUpdate').first()
        age = user['age'] if isinstance(user, dict) else user.age
        assert age == 30
    
    @pytest.mark.transaction
    def test_transaction_with_delete(self, clean_users):
        """测试事务中的删除操作"""
        # 先插入数据
        clean_users.create({'name': 'ToDelete', 'email': 'todelete@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        def delete_operation():
            clean_users.where('name', 'ToDelete').delete()
            return True
        
        result = clean_users.transaction(delete_operation)
        assert result is True
        
        # 验证数据已删除
        user = clean_users.where('name', 'ToDelete').first()
        assert user is None or user == {}
    
    @pytest.mark.transaction
    def test_transaction_partial_failure(self, clean_users, clean_orders):
        """测试部分失败的事务"""
        # 插入用户
        clean_users.create({'name': 'PartialFail', 'email': 'partial@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        user = clean_users.where('name', 'PartialFail').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        
        def partial_ops():
            # 创建订单
            clean_orders.create({'user_id': user_id, 'order_no': 'ORD001', 'amount': 100.00, 'status': 1})
            # 更新用户
            clean_users.where('id', user_id).update({'score': 90.0})
            # 失败
            raise Exception('Partial failure')
        
        with pytest.raises(Exception):
            clean_users.transaction(partial_ops)
        
        # 验证用户分数未更新
        user = clean_users.where('name', 'PartialFail').first()
        score = user['score'] if isinstance(user, dict) else user.score
        assert float(score) == 80.0
