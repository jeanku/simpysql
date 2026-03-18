#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - DELETE 删除方法
测试方法: delete
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestDelete:
    """测试 delete() 方法"""
    
    @pytest.mark.delete
    def test_delete_single_record(self, clean_users):
        """测试删除单条记录"""
        # 先插入测试数据
        clean_users.create({'name': 'DeleteTest', 'email': 'delete@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 确认数据存在
        before = clean_users.where('name', 'DeleteTest').first()
        assert before is not None
        
        # 删除数据
        result = clean_users.where('name', 'DeleteTest').delete()
        assert result is not None
        
        # 确认数据已删除
        after = clean_users.where('name', 'DeleteTest').first()
        assert after is None or after == {}
    
    @pytest.mark.delete
    def test_delete_with_id_condition(self, clean_users):
        """测试通过 ID 删除记录"""
        # 先插入测试数据并获取 ID
        clean_users.create({'name': 'DeleteById', 'email': 'delbyid@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        record = clean_users.where('name', 'DeleteById').first()
        record_id = record['id'] or record.id
        
        # 删除数据
        result = clean_users.where('id', record_id).delete()
        assert result is not None
        
        # 确认数据已删除
        after = clean_users.where('id', record_id).first()
        assert after is None or after == {}
    
    @pytest.mark.delete
    def test_delete_multiple_records(self, clean_users):
        """测试删除多条记录"""
        # 插入多条测试数据
        for i in range(5):
            clean_users.create({'name': f'DeleteMulti{i}', 'email': f'delmulti{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 确认数据存在
        before_count = clean_users.where('name', 'like', 'DeleteMulti%').count()
        assert before_count == 5
        
        # 删除所有匹配的记录
        result = clean_users.where('name', 'like', 'DeleteMulti%').delete()
        assert result is not None
        
        # 确认数据已删除
        after_count = clean_users.where('name', 'like', 'DeleteMulti%').count()
        assert after_count == 0
    
    @pytest.mark.delete
    def test_delete_with_multiple_conditions(self, clean_users):
        """测试多条件删除"""
        # 插入多条测试数据
        for i in range(3):
            clean_users.create({'name': f'DeleteCond{i}', 'email': f'delcond{i}@test.com', 'age': 20 + i * 10, 'status': 1, 'score': 80.0})
        
        # 删除特定条件的数据
        result = clean_users.where('name', 'like', 'DeleteCond%').where('age', '>', 25).delete()
        assert result is not None
        
        # 确认只有符合条件的数据被删除
        remaining = clean_users.where('name', 'like', 'DeleteCond%').get()
        assert len(remaining) == 1  # 只有 DeleteCond0 (age=20) 剩余
    
    @pytest.mark.delete
    def test_delete_with_in_condition(self, clean_users):
        """测试 IN 条件删除"""
        # 插入多条测试数据
        ids = []
        for i in range(3):
            clean_users.create({'name': f'DeleteIn{i}', 'email': f'delin{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            record = clean_users.where('name', f'DeleteIn{i}').first()
            ids.append(record['id'] or record.id)
        
        # 删除指定 ID 的数据
        result = clean_users.where('id', 'in', ids[:2]).delete()
        assert result is not None
        
        # 确认只有指定 ID 的数据被删除
        remaining = clean_users.where('name', 'like', 'DeleteIn%').count()
        assert remaining == 1
    
    @pytest.mark.delete
    def test_delete_non_existent_record(self, clean_users):
        """测试删除不存在的记录"""
        # 删除不存在的记录应该不报错
        result = clean_users.where('id', 999999).delete()
        # 返回值可能是 0 或 None
        assert result is not None or result == 0
    
    @pytest.mark.delete
    def test_delete_all_records(self, clean_users):
        """测试删除所有记录 (无 WHERE 条件)"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'DeleteAll{i}', 'email': f'delall{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 删除所有数据
        result = clean_users.where('1', '=', '1').delete()
        assert result is not None
        
        # 确认所有数据已删除
        count = clean_users.where('name', 'like', 'DeleteAll%').count()
        assert count == 0
    
    @pytest.mark.delete
    def test_delete_with_orwhere(self, clean_users):
        """测试 ORWHERE 条件删除"""
        # 插入测试数据
        clean_users.create({'name': 'DeleteOr1', 'email': 'delor1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'DeleteOr2', 'email': 'delor2@test.com', 'age': 30, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'KeepThis', 'email': 'keep@test.com', 'age': 35, 'status': 1, 'score': 80.0})
        
        # 删除满足 OR 条件的数据
        result = clean_users.where('name', 'DeleteOr1').orwhere('name', 'DeleteOr2').delete()
        assert result is not None
        
        # 确认只有符合条件的数据被删除
        remaining = clean_users.where('name', 'like', 'Delete%').orwhere('name', 'KeepThis').count()
        assert remaining == 1  # 只有 KeepThis 剩余


class TestDeleteSQL:
    """测试 DELETE SQL 生成"""
    
    @pytest.mark.delete
    def test_delete_sql_with_where(self, user_model):
        """测试带 WHERE 条件的 DELETE SQL"""
        # 验证 builder 可以正常创建
        builder = user_model.where('id', 1)
        assert builder is not None
    
    @pytest.mark.delete
    def test_delete_sql_with_multiple_conditions(self, user_model):
        """测试多条件 DELETE SQL"""
        builder = user_model.where('status', 0).where('age', '<', 18)
        assert builder is not None


class TestDeleteSafety:
    """测试删除安全性"""
    
    @pytest.mark.delete
    def test_delete_returns_affected_rows(self, clean_users):
        """测试删除返回影响行数"""
        # 插入测试数据
        clean_users.create({'name': 'AffectedRows', 'email': 'affected@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 删除并获取结果
        result = clean_users.where('name', 'AffectedRows').delete()
        # 结果应该表示影响的行数
        assert result is not None
    
    @pytest.mark.delete
    def test_delete_with_like_condition(self, clean_users):
        """测试 LIKE 条件删除"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'DeleteLike{i}_Test', 'email': f'dellike{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 使用 LIKE 删除
        result = clean_users.where('name', 'like', 'DeleteLike%_Test').delete()
        assert result is not None
        
        # 确认数据已删除
        count = clean_users.where('name', 'like', 'DeleteLike%').count()
        assert count == 0
    
    @pytest.mark.delete
    def test_delete_with_between_condition(self, clean_users):
        """测试 BETWEEN 条件删除"""
        # 插入测试数据
        for age in [20, 25, 30, 35, 40]:
            clean_users.create({'name': f'DeleteBetween{age}', 'email': f'delbet{age}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        # 删除年龄在 25-35 之间的数据
        result = clean_users.where('age', 'between', [25, 35]).delete()
        assert result is not None
        
        # 确认只有符合条件的数据被删除
        remaining = clean_users.where('name', 'like', 'DeleteBetween%').get()
        remaining_ages = [r['age'] if isinstance(r, dict) else r.age for r in remaining]
        assert 20 in remaining_ages
        assert 40 in remaining_ages
        assert 25 not in remaining_ages
        assert 30 not in remaining_ages
        assert 35 not in remaining_ages
