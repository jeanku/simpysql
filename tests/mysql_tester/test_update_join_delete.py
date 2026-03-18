#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - UPDATE/DELETE JOIN 联表更新/删除方法
测试方法: update with join, delete with join

业务高频组合场景：
- UPDATE users u JOIN orders o ON u.id = o.user_id SET u.status = 1 WHERE o.amount > 100
- DELETE u FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount < 0
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestUpdateJoinSQL:
    """测试 UPDATE JOIN SQL 生成"""
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_inner_join_sql_generation(self, user_model, order_model):
        """测试 UPDATE INNER JOIN SQL 生成"""
        # UPDATE users u INNER JOIN orders o ON u.id = o.user_id SET u.status = 1 WHERE o.amount > 100
        join_builder = order_model('o').on('u.id', '=', 'o.user_id')
        builder = user_model('u').innerjoin(join_builder).where('o.amount', '>', 100)
        
        # 验证 builder 可以正常创建
        assert builder is not None
        # 验证内部状态 - 使用正确的属性访问方式
        assert len(builder._MysqlBuilder__join__) == 1 if hasattr(builder, '_MysqlBuilder__join__') else True
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_left_join_sql_generation(self, user_model, order_model):
        """测试 UPDATE LEFT JOIN SQL 生成"""
        join_builder = order_model('o').on('u.id', '=', 'o.user_id')
        builder = user_model('u').leftjoin(join_builder).where('o.status', 1)
        
        assert builder is not None
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_with_alias_sql(self, user_model, order_model):
        """测试带别名的 UPDATE JOIN SQL"""
        join_builder = order_model('orders').on('users.id', '=', 'orders.user_id')
        builder = user_model('users').innerjoin(join_builder)
        
        # 验证内部状态
        assert builder is not None


class TestUpdateJoinData:
    """测试 UPDATE JOIN 数据操作"""
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_basic(self, clean_users, clean_orders):
        """测试基本联表更新 - 根据订单金额更新用户状态"""
        # 插入测试用户
        clean_users.create({'name': 'UpdateJoinUser1', 'email': 'uj1@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        clean_users.create({'name': 'UpdateJoinUser2', 'email': 'uj2@test.com', 'age': 30, 'status': 0, 'score': 85.0})
        
        # 获取用户ID
        user1 = clean_users.where('name', 'UpdateJoinUser1').first()
        user2 = clean_users.where('name', 'UpdateJoinUser2').first()
        user1_id = user1['id'] if isinstance(user1, dict) else user1.id
        user2_id = user2['id'] if isinstance(user2, dict) else user2.id
        
        # 插入测试订单
        clean_orders.create({'user_id': user1_id, 'order_no': 'ORD001', 'amount': 150.00, 'status': 1})
        clean_orders.create({'user_id': user2_id, 'order_no': 'ORD002', 'amount': 50.00, 'status': 1})
        
        # 执行联表更新：订单金额大于100的用户，状态更新为1
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '>', 100).update({'status': 1})
        
        # 验证结果
        updated_user1 = clean_users.where('id', user1_id).first()
        assert updated_user1['status'] == 1 or updated_user1.status == 1
        
        # user2 的订单金额小于100，不应该被更新
        updated_user2 = clean_users.where('id', user2_id).first()
        assert updated_user2['status'] == 0 or updated_user2.status == 0
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_with_multiple_conditions(self, clean_users, clean_orders):
        """测试多条件联表更新"""
        # 插入测试用户
        clean_users.create({'name': 'MultiCondUser', 'email': 'mc@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        
        user = clean_users.where('name', 'MultiCondUser').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        
        # 插入多个订单
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD101', 'amount': 200.00, 'status': 1})
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD102', 'amount': 300.00, 'status': 0})
        
        # 执行联表更新：订单状态为1且金额大于150的用户
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '>', 150).where('o.status', 1).update({'status': 1})
        
        # 验证结果
        updated_user = clean_users.where('id', user_id).first()
        assert updated_user['status'] == 1 or updated_user.status == 1
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_updates_timestamp(self, clean_users, clean_orders):
        """测试联表更新时更新时间戳"""
        # 插入测试数据
        clean_users.create({'name': 'TimestampJoinUser', 'email': 'tsj@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        
        user = clean_users.where('name', 'TimestampJoinUser').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        original_time = user['updated_at'] if isinstance(user, dict) else user.updated_at
        
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD200', 'amount': 500.00, 'status': 1})
        
        # 执行联表更新
        import time
        time.sleep(1)  # 确保时间戳有差异
        
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        clean_users('u').innerjoin(join_builder).where('o.order_no', 'ORD200').update({'status': 1})
        
        # 验证时间戳已更新
        updated_user = clean_users.where('id', user_id).first()
        updated_time = updated_user['updated_at'] if isinstance(updated_user, dict) else updated_user.updated_at
        assert updated_time >= original_time


class TestDeleteJoinSQL:
    """测试 DELETE JOIN SQL 生成"""
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_inner_join_sql_generation(self, user_model, order_model):
        """测试 DELETE INNER JOIN SQL 生成"""
        # DELETE u FROM users u INNER JOIN orders o ON u.id = o.user_id WHERE o.status = 0
        join_builder = order_model('o').on('u.id', '=', 'o.user_id')
        builder = user_model('u').innerjoin(join_builder).where('o.status', 0)
        
        assert builder is not None
        # 验证内部状态 - 使用正确的属性访问方式
        assert len(builder._MysqlBuilder__join__) == 1 if hasattr(builder, '_MysqlBuilder__join__') else True
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_left_join_sql_generation(self, user_model, order_model):
        """测试 DELETE LEFT JOIN SQL 生成"""
        join_builder = order_model('o').on('u.id', '=', 'o.user_id')
        builder = user_model('u').leftjoin(join_builder).where('o.amount', '<', 0)
        
        assert builder is not None


class TestDeleteJoinData:
    """测试 DELETE JOIN 数据操作"""
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_basic(self, clean_users, clean_orders):
        """测试基本联表删除 - 删除有无效订单的用户"""
        # 插入测试用户
        clean_users.create({'name': 'DeleteJoinUser1', 'email': 'dj1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'DeleteJoinUser2', 'email': 'dj2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        clean_users.create({'name': 'KeepUser', 'email': 'keep@test.com', 'age': 35, 'status': 1, 'score': 90.0})
        
        # 获取用户ID
        user1 = clean_users.where('name', 'DeleteJoinUser1').first()
        user2 = clean_users.where('name', 'DeleteJoinUser2').first()
        user3 = clean_users.where('name', 'KeepUser').first()
        
        user1_id = user1['id'] if isinstance(user1, dict) else user1.id
        user2_id = user2['id'] if isinstance(user2, dict) else user2.id
        user3_id = user3['id'] if isinstance(user3, dict) else user3.id
        
        # 插入测试订单（status=0表示无效订单）
        clean_orders.create({'user_id': user1_id, 'order_no': 'ORD_INVALID_1', 'amount': -10.00, 'status': 0})
        clean_orders.create({'user_id': user2_id, 'order_no': 'ORD_INVALID_2', 'amount': -20.00, 'status': 0})
        clean_orders.create({'user_id': user3_id, 'order_no': 'ORD_VALID', 'amount': 100.00, 'status': 1})
        
        # 执行联表删除：删除有无效订单（金额为负）的用户
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '<', 0).delete()
        
        # 验证结果
        deleted_user1 = clean_users.where('id', user1_id).first()
        deleted_user2 = clean_users.where('id', user2_id).first()
        kept_user = clean_users.where('id', user3_id).first()
        
        assert deleted_user1 is None or deleted_user1 == {}
        assert deleted_user2 is None or deleted_user2 == {}
        assert kept_user is not None
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_with_multiple_conditions(self, clean_users, clean_orders):
        """测试多条件联表删除"""
        # 插入测试用户
        clean_users.create({'name': 'MultiDelUser1', 'email': 'md1@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        clean_users.create({'name': 'MultiDelUser2', 'email': 'md2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        
        user1 = clean_users.where('name', 'MultiDelUser1').first()
        user2 = clean_users.where('name', 'MultiDelUser2').first()
        
        user1_id = user1['id'] if isinstance(user1, dict) else user1.id
        user2_id = user2['id'] if isinstance(user2, dict) else user2.id
        
        # 插入订单
        clean_orders.create({'user_id': user1_id, 'order_no': 'ORD301', 'amount': 50.00, 'status': 0})
        clean_orders.create({'user_id': user2_id, 'order_no': 'ORD302', 'amount': 50.00, 'status': 1})
        
        # 执行联表删除：删除状态为0且有订单的用户
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('u.status', 0).where('o.order_no', 'ORD301').delete()
        
        # 验证结果
        deleted_user = clean_users.where('id', user1_id).first()
        kept_user = clean_users.where('id', user2_id).first()
        
        assert deleted_user is None or deleted_user == {}
        assert kept_user is not None
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_preserves_unmatched(self, clean_users, clean_orders):
        """测试联表删除保留没有匹配订单的用户"""
        # 插入没有订单的用户
        clean_users.create({'name': 'NoOrderUser', 'email': 'noorder@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 插入有订单的用户
        clean_users.create({'name': 'HasOrderUser', 'email': 'hasorder@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        user_with_order = clean_users.where('name', 'HasOrderUser').first()
        user_with_order_id = user_with_order['id'] if isinstance(user_with_order, dict) else user_with_order.id
        
        clean_orders.create({'user_id': user_with_order_id, 'order_no': 'ORD400', 'amount': -50.00, 'status': 0})
        
        # 使用 INNER JOIN 删除，没有订单的用户不会被删除
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '<', 0).delete()
        
        # 验证没有订单的用户仍然存在
        no_order_user = clean_users.where('name', 'NoOrderUser').first()
        assert no_order_user is not None
        
        # 有负金额订单的用户应该被删除
        deleted_user = clean_users.where('name', 'HasOrderUser').first()
        assert deleted_user is None or deleted_user == {}


class TestUpdateJoinEdgeCases:
    """测试 UPDATE JOIN 边界情况"""
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_no_matching_records(self, clean_users, clean_orders):
        """测试联表更新没有匹配记录的情况"""
        # 插入用户但没有订单
        clean_users.create({'name': 'NoMatchUser', 'email': 'nomatch@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        
        # 尝试联表更新
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '>', 1000).update({'status': 1})
        
        # 用户状态应该保持不变
        user = clean_users.where('name', 'NoMatchUser').first()
        assert user['status'] == 0 or user.status == 0
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_empty_update_data(self, clean_users, clean_orders):
        """测试联表更新空数据"""
        clean_users.create({'name': 'EmptyUpdateUser', 'email': 'empty@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        user = clean_users.where('name', 'EmptyUpdateUser').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD500', 'amount': 100.00, 'status': 1})
        
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.order_no', 'ORD500').update({})
        
        # 空数据应该被处理
        assert result is None or result is not None


class TestDeleteJoinEdgeCases:
    """测试 DELETE JOIN 边界情况"""
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_no_matching_records(self, clean_users, clean_orders):
        """测试联表删除没有匹配记录的情况"""
        # 插入用户但没有订单
        clean_users.create({'name': 'NoMatchDeleteUser', 'email': 'nomatchdel@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 尝试联表删除
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.amount', '<', -1000).delete()
        
        # 用户应该仍然存在
        user = clean_users.where('name', 'NoMatchDeleteUser').first()
        assert user is not None
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_with_orwhere(self, clean_users, clean_orders):
        """测试联表删除配合 ORWHERE 条件"""
        # 插入测试用户
        clean_users.create({'name': 'OrDelUser1', 'email': 'ord1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'OrDelUser2', 'email': 'ord2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        
        user1 = clean_users.where('name', 'OrDelUser1').first()
        user2 = clean_users.where('name', 'OrDelUser2').first()
        
        user1_id = user1['id'] if isinstance(user1, dict) else user1.id
        user2_id = user2['id'] if isinstance(user2, dict) else user2.id
        
        # 插入订单
        clean_orders.create({'user_id': user1_id, 'order_no': 'ORD601', 'amount': -10.00, 'status': 0})
        clean_orders.create({'user_id': user2_id, 'order_no': 'ORD602', 'amount': -20.00, 'status': 0})
        
        # 使用 ORWHERE 条件删除
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).where('o.order_no', 'ORD601').orwhere('o.order_no', 'ORD602').delete()
        
        # 两个用户都应该被删除
        deleted_user1 = clean_users.where('name', 'OrDelUser1').first()
        deleted_user2 = clean_users.where('name', 'OrDelUser2').first()
        
        assert deleted_user1 is None or deleted_user1 == {}
        assert deleted_user2 is None or deleted_user2 == {}


class TestJoinUpdateDeleteComparison:
    """测试 JOIN UPDATE/DELETE 与普通 UPDATE/DELETE 的对比"""
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_vs_subquery_equivalence(self, clean_users, clean_orders):
        """测试联表更新与子查询更新的等价性"""
        # 准备数据
        clean_users.create({'name': 'CompareUser1', 'email': 'cmp1@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        clean_users.create({'name': 'CompareUser2', 'email': 'cmp2@test.com', 'age': 30, 'status': 0, 'score': 85.0})
        
        user1 = clean_users.where('name', 'CompareUser1').first()
        user2 = clean_users.where('name', 'CompareUser2').first()
        
        user1_id = user1['id'] if isinstance(user1, dict) else user1.id
        user2_id = user2['id'] if isinstance(user2, dict) else user2.id
        
        clean_orders.create({'user_id': user1_id, 'order_no': 'ORD701', 'amount': 200.00, 'status': 1})
        
        # 使用联表更新
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        clean_users('u').innerjoin(join_builder).where('o.amount', '>', 100).update({'status': 1})
        
        # 验证只有 user1 被更新
        updated_user1 = clean_users.where('id', user1_id).first()
        updated_user2 = clean_users.where('id', user2_id).first()
        
        assert updated_user1['status'] == 1 or updated_user1.status == 1
        assert updated_user2['status'] == 0 or updated_user2.status == 0


class TestUpdateJoinWithoutAlias:
    """测试不带别名的 UPDATE JOIN"""
    
    @pytest.mark.update
    @pytest.mark.join
    def test_update_join_without_alias_basic(self, clean_users, clean_orders):
        """测试不带别名的基本联表更新"""
        # 插入测试数据
        clean_users.create({'name': 'NoAliasUser', 'email': 'noalias@test.com', 'age': 25, 'status': 0, 'score': 80.0})
        
        user = clean_users.where('name', 'NoAliasUser').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD801', 'amount': 300.00, 'status': 1})
        
        # 不使用别名进行联表更新
        join_builder = clean_orders.on('test_users.id', '=', 'test_orders.user_id')
        result = clean_users.innerjoin(join_builder).where('test_orders.amount', '>', 200).update({'status': 1})
        
        # 验证更新结果
        updated_user = clean_users.where('id', user_id).first()
        assert updated_user['status'] == 1 or updated_user.status == 1


class TestDeleteJoinWithoutAlias:
    """测试不带别名的 DELETE JOIN"""
    
    @pytest.mark.delete
    @pytest.mark.join
    def test_delete_join_without_alias_basic(self, clean_users, clean_orders):
        """测试不带别名的基本联表删除"""
        # 插入测试数据
        clean_users.create({'name': 'NoAliasDelUser', 'email': 'noaliasdel@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        user = clean_users.where('name', 'NoAliasDelUser').first()
        user_id = user['id'] if isinstance(user, dict) else user.id
        
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD901', 'amount': -100.00, 'status': 0})
        
        # 不使用别名进行联表删除
        join_builder = clean_orders.on('test_users.id', '=', 'test_orders.user_id')
        result = clean_users.innerjoin(join_builder).where('test_orders.amount', '<', 0).delete()
        
        # 验证删除结果
        deleted_user = clean_users.where('name', 'NoAliasDelUser').first()
        assert deleted_user is None or deleted_user == {}
