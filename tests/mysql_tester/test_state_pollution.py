#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 状态污染测试
测试 Query Builder 实例复用时的状态污染问题
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestFirstStatePollution:
    """测试 first() 方法状态污染"""
    
    @pytest.mark.state
    def test_first_pollutes_limit(self, clean_users):
        """测试 first() 是否污染 __limit__ 状态"""
        # 插入测试数据
        clean_users.create({'name': 'FirstPollution', 'email': 'firstpollution@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 获取 builder 实例
        builder = clean_users.where('name', 'FirstPollution')
        
        # 记录原始 limit 状态
        original_limit = builder.__limit__
        
        # 调用 first()
        result = builder.first()
        
        # 验证 limit 已恢复
        assert builder.__limit__ == original_limit
        
        # 验证再次调用 get() 时 limit 仍然是 None
        result2 = builder.get()
        assert builder.__limit__ is None
    
    @pytest.mark.state
    def test_first_returns_empty_dict(self, clean_users):
        """测试 first() 空结果返回空字典"""
        result = clean_users.where('name', 'NonExistentFirst').first()
        
        # 验证返回空字典或 None
        assert result == {} or result is None


class TestCountStatePollution:
    """测试 count() 方法状态污染"""
    
    @pytest.mark.state
    def test_count_pollutes_select(self, clean_users):
        """测试 count() 是否污染 __select__ 状态"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'CountPollution{i}', 'email': f'countpollution{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 获取 builder 实例
        builder = clean_users.where('name', 'like', 'CountPollution%')
        
        # 记录原始 select 状态
        original_select = builder.__select__
        
        # 调用 count()
        result = builder.count()
        
        # 验证 select 已恢复
        assert builder.__select__ == original_select
        
        # 验证再次调用 get() 时 select 仍然是原始
        result2 = builder.get()
        assert builder.__select__ == original_select


class TestMaxStatePollution:
    """测试 max() 方法状态污染"""
    
    @pytest.mark.state
    def test_max_pollutes_select(self, clean_users):
        """测试 max() 是否污染 __select__ 状态"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'MaxPollution{i}', 'email': f'maxpollution{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        # 获取 builder 实例
        builder = clean_users.where('name', 'like', 'MaxPollution%')
        
        # 记录原始 select 状态
        original_select = builder.__select__
        
        # 调用 max()
        result = builder.max('id')
        
        # 验证 select 已恢复
        assert builder.__select__ == original_select
        
        # 验证再次调用 get() 时 select 仍然是原始
        result2 = builder.get()
        assert builder.__select__ == original_select


class TestExistStatePollution:
    """测试 exist() 方法状态污染"""
    
    @pytest.mark.state
    def test_exist_pollutes_limit(self, clean_users):
        """测试 exist() 是否污染 __limit__ 状态"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'ExistPollution{i}', 'email': f'existpollution{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 获取 builder 实例
        builder = clean_users.where('name', 'like', 'ExistPollution%')
        
        # 记录原始 limit 状态
        original_limit = builder.__limit__
        
        # 调用 exist()
        result = builder.exist()
        
        # 验证 limit 已恢复
        assert builder.__limit__ == original_limit
        
        # 验证再次调用 get() 时 limit 仍然是 None
        result2 = builder.get()
        assert builder.__limit__ is None


class TestAggregateStatePollution:
    """测试聚合方法状态污染"""
    
    @pytest.mark.state
    def test_aggregate_methods_pollution(self, clean_users):
        """测试聚合方法是否污染状态"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'AggregatePollution{i}', 'email': f'aggregatepollution{i}@test.com', 'age': 20 + i, 'status': 1, 'score': 70.0 + i * 10})
        
        # 获取 builder 实例
        builder = clean_users.where('name', 'like', 'AggregatePollution%')
        
        # 记录原始 select 状态
        original_select = builder.__select__
        
        # 调用 count()
        count_result = builder.count()
        
        # 调用 max()
        max_result = builder.max('id')
        
        # 调用 min()
        min_result = builder.min('id')
        
        # 调用 avg()
        avg_result = builder.avg('age')
        
        # 调用 sum()
        sum_result = builder.sum('score')
        
        # 验证 select 已恢复
        assert builder.__select__ == original_select
        
        # 验证再次调用 get() 时 select 仍然是原始
        result = builder.get()
        assert builder.__select__ == original_select


class TestBuilderReusability:
    """测试 Builder 实例可复用"""
    
    @pytest.mark.state
    def test_builder_can_be_reused(self, clean_users):
        """测试 Builder 实例可以复用"""
        # 插入测试数据
        clean_users.create({'name': 'Reusable1', 'email': 'reusable@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 创建第一个 builder
        builder1 = clean_users.where('name', 'Reusable1')
        
        # 创建第二个 builder (复用第一个)
        builder2 = clean_users.where('name', 'Reusable1')
        
        # 验证两个 builder 是独立的实例
        assert builder1 is not builder2
        
        # 验证第一个 builder 的查询正常
        result1 = builder1.first()
        assert result1 is not None
        
        # 验证第二个 builder 的查询正常
        result2 = builder2.first()
        assert result2 is not None
        
        # 验证两个 builder 不互相影响
        assert result1['name'] == 'Reusable1'
        assert result2['name'] == 'Reusable1'


class TestWhereStatePollution:
    """测试 where 条件状态污染"""
    
    @pytest.mark.state
    def test_where_conditions_isolated(self, clean_users):
        """测试 where 条件在不同 builder 之间是隔离的"""
        # 插入测试数据
        clean_users.create({'name': 'WhereIsolation1', 'email': 'whereisolation1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'WhereIsolation2', 'email': 'whereisolation2@test.com', 'age': 30, 'status': 1, 'score': 90.0})
        
        # 创建第一个 builder 带 where 条件
        builder1 = clean_users.where('name', 'WhereIsolation1')
        
        # 创建第二个 builder 带不同的 where 条件
        builder2 = clean_users.where('name', 'WhereIsolation2')
        
        # 验证第一个 builder 返回正确的记录
        result1 = builder1.first()
        assert result1['name'] == 'WhereIsolation1'
        
        # 验证第二个 builder 返回正确的记录
        result2 = builder2.first()
        assert result2['name'] == 'WhereIsolation2'


class TestSelectStatePollution:
    """测试 select 字段状态污染"""
    
    @pytest.mark.state
    def test_select_fields_isolated(self, clean_users):
        """测试 select 字段在不同 builder 之间是隔离的"""
        # 插入测试数据
        clean_users.create({'name': 'SelectIsolation', 'email': 'selectisolation@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 创建第一个 builder 选择特定字段
        builder1 = clean_users.select('name', 'email').where('name', 'SelectIsolation')
        
        # 创建第二个 builder 选择不同字段
        builder2 = clean_users.select('id', 'age').where('name', 'SelectIsolation')
        
        # 验证第一个 builder 返回正确的字段
        result1 = builder1.first()
        assert 'name' in result1
        assert 'email' in result1
        
        # 验证第二个 builder 返回正确的字段
        result2 = builder2.first()
        assert 'id' in result2
        assert 'age' in result2


class TestOrderByStatePollution:
    """测试 orderby 状态污染"""
    
    @pytest.mark.state
    def test_orderby_isolated(self, clean_users):
        """测试 orderby 在不同 builder 之间是隔离的"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'OrderIsolation{i}', 'email': f'orderisolation{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        # 创建第一个 builder 按 age 升序
        builder1 = clean_users.where('name', 'like', 'OrderIsolation%').orderby('age', 'asc')
        
        # 创建第二个 builder 按 age 降序
        builder2 = clean_users.where('name', 'like', 'OrderIsolation%').orderby('age', 'desc')
        
        # 验证第一个 builder 返回升序结果
        result1 = builder1.get()
        assert result1[0]['age'] <= result1[1]['age']
        
        # 验证第二个 builder 返回降序结果
        result2 = builder2.get()
        assert result2[0]['age'] >= result2[1]['age']


class TestLimitOffsetStatePollution:
    """测试 limit/offset 状态污染"""
    
    @pytest.mark.state
    def test_limit_offset_isolated(self, clean_users):
        """测试 limit/offset 在不同 builder 之间是隔离的"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'LimitOffset{i}', 'email': f'limitoffset{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0})
        
        # 创建第一个 builder 带 limit 2
        builder1 = clean_users.where('name', 'like', 'LimitOffset%').take(2)
        
        # 创建第二个 builder 带 limit 3
        builder2 = clean_users.where('name', 'like', 'LimitOffset%').take(3)
        
        # 验证第一个 builder 返回 2 条记录
        result1 = builder1.get()
        assert len(result1) == 2
        
        # 验证第二个 builder 返回 3 条记录
        result2 = builder2.get()
        assert len(result2) == 3
    
    @pytest.mark.state
    def test_offset_isolated(self, clean_users):
        """测试 offset 在不同 builder 之间是隔离的"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'OffsetTest{i}', 'email': f'offsettest{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0})
        
        # 创建第一个 builder 带 offset 0
        builder1 = clean_users.where('name', 'like', 'OffsetTest%').orderby('id', 'asc').offset(0).take(2)
        
        # 创建第二个 builder 带 offset 2
        builder2 = clean_users.where('name', 'like', 'OffsetTest%').orderby('id', 'asc').offset(2).take(2)
        
        # 验证结果不同
        result1 = builder1.get()
        result2 = builder2.get()
        
        # 两个结果集应该不同（因为 offset 不同）
        if result1 and result2:
            assert result1[0]['id'] != result2[0]['id']


class TestGroupByHavingStatePollution:
    """测试 groupby/having 状态污染"""
    
    @pytest.mark.state
    def test_groupby_having_isolated(self, clean_users):
        """测试 groupby/having 在不同 builder 之间是隔离的"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'GroupByTestA{i}', 'email': f'groupbytesta{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
            clean_users.create({'name': f'GroupByTestB{i}', 'email': f'groupbytestb{i}@test.com', 'age': 30, 'status': 1, 'score': 90.0})
        
        # 创建第一个 builder 按 age 分组
        builder1 = clean_users.select('age').where('name', 'like', 'GroupByTest%').groupby('age')
        
        # 验证分组结果
        result1 = builder1.get()
        assert len(result1) >= 1  # 至少有一个年龄组
