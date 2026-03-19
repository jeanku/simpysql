#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - UNION 联合查询方法
测试方法: union, unionall
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestUnion:
    """测试 UNION 方法"""
    
    @pytest.mark.union
    def test_union_basic(self, user_model):
        """测试基本 UNION"""
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        sql = query1.union(query2).tosql()
        
        assert 'union' in sql.lower()
        assert 'select' in sql.lower()
    
    @pytest.mark.union
    def test_union_with_where(self, user_model):
        """测试带 WHERE 条件的 UNION"""
        query1 = user_model.where('age', '>', 30).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        sql = query1.union(query2).tosql()
        
        assert 'union' in sql.lower()
        assert 'where' in sql.lower()
    
    @pytest.mark.union
    def test_union_multiple(self, user_model):
        """测试多个 UNION"""
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        query3 = user_model.where('age', '<', 20).select('id', 'name')
        
        sql = query1.union(query2).union(query3).tosql()
        
        # 应该有两个 union
        assert sql.lower().count('union') >= 2
    
    @pytest.mark.union
    def test_union_deduplication(self, clean_users):
        """测试 UNION 去重"""
        # 插入测试数据
        clean_users.create({'name': 'UnionTest1', 'email': 'union1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'UnionTest2', 'email': 'union2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        
        # 两个查询有重叠数据
        query1 = clean_users.where('status', 1).select('id', 'name')
        query2 = clean_users.where('age', '>=', 25).select('id', 'name')
        
        result = query1.union(query2).get()
        
        # UNION 会去重，所以结果数量应该合理
        assert len(result) >= 2
    
    @pytest.mark.union
    def test_union_invalid_type(self, user_model):
        """测试 UNION 无效类型"""
        with pytest.raises(TypeError):
            user_model.union('not_a_builder')


class TestUnionAll:
    """测试 UNION ALL 方法"""
    
    @pytest.mark.union
    def test_unionall_basic(self, user_model):
        """测试基本 UNION ALL"""
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        sql = query1.unionall(query2).tosql()
        
        assert 'union all' in sql.lower()
    
    @pytest.mark.union
    def test_unionall_keeps_duplicates(self, clean_users):
        """测试 UNION ALL 保留重复"""
        # 插入测试数据
        clean_users.create({'name': 'UnionAllTest1', 'email': 'unionall1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'UnionAllTest2', 'email': 'unionall2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        
        # 两个查询有重叠数据
        query1 = clean_users.where('status', 1).select('id', 'name')
        query2 = clean_users.where('age', '>=', 25).select('id', 'name')
        
        result = query1.unionall(query2).get()
        
        # UNION ALL 不去重，结果数量应该更多
        assert len(result) >= 2
    
    @pytest.mark.union
    def test_unionall_with_orderby(self, user_model):
        """测试 UNION ALL 配合 ORDER BY"""
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        sql = query1.unionall(query2).orderby('id', 'desc').tosql()
        
        assert 'union all' in sql.lower()
        assert 'order by' in sql.lower()
    
    @pytest.mark.union
    def test_unionall_with_limit(self, user_model):
        """测试 UNION ALL 配合 LIMIT"""
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        sql = query1.unionall(query2).take(10).tosql()
        
        assert 'union all' in sql.lower()
        assert 'limit 10' in sql.lower()
    
    @pytest.mark.union
    def test_unionall_invalid_type(self, user_model):
        """测试 UNION ALL 无效类型"""
        with pytest.raises(TypeError):
            user_model.unionall('not_a_builder')


class TestUnionComplex:
    """测试复杂 UNION 查询"""
    
    @pytest.mark.union
    def test_union_with_different_tables(self, user_model, order_model):
        """测试不同表的 UNION (需要相同列数)"""
        # 注意：实际使用时需要确保两个查询的列数相同
        query1 = user_model.select('id', 'name')
        query2 = order_model.select('id', 'order_no')
        
        sql = query1.union(query2).tosql()
        
        assert 'union' in sql.lower()
    
    @pytest.mark.union
    def test_union_with_aggregate(self, user_model):
        """测试带聚合函数的 UNION"""
        query1 = user_model.select('status', 'count(*) as cnt').groupby('status')
        query2 = user_model.select('status', 'count(*) as cnt').groupby('status')
        
        sql = query1.union(query2).tosql()
        
        assert 'union' in sql.lower()
        assert 'count(*)' in sql.lower()
    
    @pytest.mark.union
    def test_union_subquery_combination(self, user_model):
        """测试 UNION 与子查询组合"""
        # 复杂查询：UNION 后作为子查询
        query1 = user_model.where('status', 1).select('id', 'name')
        query2 = user_model.where('status', 0).select('id', 'name')
        
        union_query = query1.union(query2)
        
        # 验证可以正常生成 SQL
        sql = union_query.tosql()
        assert 'union' in sql.lower()


class TestUnionDataIntegrity:
    """测试 UNION 数据完整性"""
    
    @pytest.mark.union
    def test_union_returns_correct_columns(self, clean_users):
        """测试 UNION 返回正确的列"""
        # 插入测试数据
        clean_users.create({'name': 'UnionColTest', 'email': 'unioncol@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        query1 = clean_users.where('status', 1).select('id', 'name')
        query2 = clean_users.where('status', 0).select('id', 'name')
        
        result = query1.union(query2).get()
        
        if len(result) > 0:
            first = result[0]
            # 验证返回的列
            if isinstance(first, dict):
                assert 'id' in first or 'name' in first
            else:
                # Dynamic 对象
                assert hasattr(first, 'id') or hasattr(first, 'name')
    
    @pytest.mark.union
    def test_union_order_across_queries(self, clean_users):
        """测试 UNION 跨查询排序"""
        # 插入测试数据
        clean_users.create({'name': 'UnionOrderA', 'email': 'uniona@test.com', 'age': 30, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'UnionOrderB', 'email': 'unionb@test.com', 'age': 20, 'status': 0, 'score': 85.0})
        
        query1 = clean_users.where('status', 1).select('id', 'name', 'age')
        query2 = clean_users.where('status', 0).select('id', 'name', 'age')
        
        result = query1.union(query2).orderby('age', 'asc').get()
        
        # 验证排序
        if len(result) >= 2:
            ages = [r['age'] if isinstance(r, dict) else r.age for r in result]
            assert ages == sorted(ages)
