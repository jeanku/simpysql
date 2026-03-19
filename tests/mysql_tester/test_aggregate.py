#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 聚合函数方法
测试方法: count, max, min, avg, sum
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestCount:
    """测试 count() 方法"""
    
    @pytest.mark.aggregate
    def test_count_all(self, user_model):
        """测试统计所有记录"""
        result = user_model.count()
        assert result is not None
        assert isinstance(result, int)
    
    @pytest.mark.aggregate
    def test_count_with_condition(self, clean_users):
        """测试带条件的统计"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'CountTest{i}', 'email': f'count{i}@test.com', 'age': 20 + i, 'status': 1 if i < 3 else 0, 'score': 80.0})
        
        # 统计 status=1 的记录
        result = clean_users.where('status', 1).count()
        assert result == 3
    
    @pytest.mark.aggregate
    def test_count_empty_table(self, clean_users):
        """测试空表统计"""
        result = clean_users.count()
        assert result == 0
    
    @pytest.mark.aggregate
    def test_count_with_like(self, clean_users):
        """测试 LIKE 条件统计"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'CountLike_Test{i}', 'email': f'countlike{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'like', 'CountLike%').count()
        assert result == 3
    
    @pytest.mark.aggregate
    def test_count_with_in(self, clean_users):
        """测试 IN 条件统计"""
        # 插入测试数据
        for age in [20, 25, 30, 35, 40]:
            clean_users.create({'name': f'CountIn{age}', 'email': f'countin{age}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('age', 'in', [20, 25, 30]).count()
        assert result == 3
    
    @pytest.mark.aggregate
    def test_count_with_between(self, clean_users):
        """测试 BETWEEN 条件统计"""
        # 插入测试数据
        for age in [20, 25, 30, 35, 40]:
            clean_users.create({'name': f'CountBet{age}', 'email': f'countbet{age}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('age', 'between', [25, 35]).count()
        assert result == 3


class TestMax:
    """测试 max() 方法"""
    
    @pytest.mark.aggregate
    def test_max_id(self, clean_users):
        """测试最大 ID"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'MaxId{i}', 'email': f'maxid{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0 + i})
        
        result = clean_users.max('id')
        assert result is not None
        assert isinstance(result, int)
    
    @pytest.mark.aggregate
    def test_max_age(self, clean_users):
        """测试最大年龄"""
        # 插入测试数据
        ages = [20, 25, 30, 35, 40]
        for i, age in enumerate(ages):
            clean_users.create({'name': f'MaxAge{i}', 'email': f'maxage{i}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.max('age')
        assert result == 40
    
    @pytest.mark.aggregate
    def test_max_score(self, clean_users):
        """测试最大分数"""
        # 插入测试数据
        scores = [75.5, 80.0, 85.5, 90.0, 95.5]
        for i, score in enumerate(scores):
            clean_users.create({'name': f'MaxScore{i}', 'email': f'maxscore{i}@test.com', 'age': 25, 'status': 1, 'score': score})
        
        result = clean_users.max('score')
        assert float(result) == 95.5
    
    @pytest.mark.aggregate
    def test_max_with_condition(self, clean_users):
        """测试带条件的最大值"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'MaxCond{i}', 'email': f'maxcond{i}@test.com', 'age': 20 + i * 5, 'status': 1 if i < 3 else 0, 'score': 80.0})
        
        result = clean_users.where('status', 1).max('age')
        assert result == 30  # 20, 25, 30 中最大
    
    @pytest.mark.aggregate
    def test_max_empty_table(self, clean_users):
        """测试空表的最大值"""
        result = clean_users.max('age')
        assert result is None
    
    @pytest.mark.aggregate
    def test_max_invalid_column(self, clean_users):
        """测试无效列名"""
        with pytest.raises(Exception):
            clean_users.max('non_existent_column')


class TestMin:
    """测试 min() 方法"""
    
    @pytest.mark.aggregate
    def test_min_id(self, clean_users):
        """测试最小 ID"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'MinId{i}', 'email': f'minid{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = clean_users.min('id')
        assert result is not None
        assert isinstance(result, int)
    
    @pytest.mark.aggregate
    def test_min_age(self, clean_users):
        """测试最小年龄"""
        # 插入测试数据
        ages = [20, 25, 30, 35, 40]
        for i, age in enumerate(ages):
            clean_users.create({'name': f'MinAge{i}', 'email': f'minage{i}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.min('age')
        assert result == 20
    
    @pytest.mark.aggregate
    def test_min_score(self, clean_users):
        """测试最小分数"""
        # 插入测试数据
        scores = [75.5, 80.0, 85.5, 90.0, 95.5]
        for i, score in enumerate(scores):
            clean_users.create({'name': f'MinScore{i}', 'email': f'minscore{i}@test.com', 'age': 25, 'status': 1, 'score': score})
        
        result = clean_users.min('score')
        assert float(result) == 75.5
    
    @pytest.mark.aggregate
    def test_min_with_condition(self, clean_users):
        """测试带条件的最小值"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'MinCond{i}', 'email': f'mincond{i}@test.com', 'age': 20 + i * 5, 'status': 1 if i >= 2 else 0, 'score': 80.0})
        
        result = clean_users.where('status', 1).min('age')
        assert result == 30  # 30, 35, 40 中最小
    
    @pytest.mark.aggregate
    def test_min_empty_table(self, clean_users):
        """测试空表的最小值"""
        result = clean_users.min('age')
        assert result is None
    
    @pytest.mark.aggregate
    def test_min_invalid_column(self, clean_users):
        """测试无效列名"""
        with pytest.raises(Exception):
            clean_users.min('non_existent_column')


class TestAvg:
    """测试 avg() 方法"""
    
    @pytest.mark.aggregate
    def test_avg_age(self, clean_users):
        """测试平均年龄"""
        # 插入测试数据
        ages = [20, 25, 30, 35, 40]
        for i, age in enumerate(ages):
            clean_users.create({'name': f'AvgAge{i}', 'email': f'avgage{i}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.avg('age')
        # 平均值应该是 30
        assert result is not None
        assert abs(float(result) - 30.0) < 0.01
    
    @pytest.mark.aggregate
    def test_avg_score(self, clean_users):
        """测试平均分数"""
        # 插入测试数据
        scores = [80.0, 85.0, 90.0]
        for i, score in enumerate(scores):
            clean_users.create({'name': f'AvgScore{i}', 'email': f'avgscore{i}@test.com', 'age': 25, 'status': 1, 'score': score})
        
        result = clean_users.avg('score')
        # 平均值应该是 85.0
        assert result is not None
        assert abs(float(result) - 85.0) < 0.01
    
    @pytest.mark.aggregate
    def test_avg_with_condition(self, clean_users):
        """测试带条件的平均值"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'AvgCond{i}', 'email': f'avgcond{i}@test.com', 'age': 20 + i * 5, 'status': 1 if i < 3 else 0, 'score': 80.0})
        
        result = clean_users.where('status', 1).avg('age')
        # 20, 25, 30 的平均值是 25
        assert result is not None
        assert abs(float(result) - 25.0) < 0.01
    
    @pytest.mark.aggregate
    def test_avg_empty_table(self, clean_users):
        """测试空表的平均值"""
        result = clean_users.avg('age')
        assert result is None
    
    @pytest.mark.aggregate
    def test_avg_invalid_column(self, clean_users):
        """测试无效列名"""
        with pytest.raises(Exception):
            clean_users.avg('non_existent_column')


class TestSum:
    """测试 sum() 方法"""
    
    @pytest.mark.aggregate
    def test_sum_age(self, clean_users):
        """测试年龄总和"""
        # 插入测试数据
        ages = [20, 25, 30, 35, 40]
        for i, age in enumerate(ages):
            clean_users.create({'name': f'SumAge{i}', 'email': f'sumage{i}@test.com', 'age': age, 'status': 1, 'score': 80.0})
        
        result = clean_users.sum('age')
        # 总和应该是 150
        assert result is not None
        assert float(result) == 150.0
    
    @pytest.mark.aggregate
    def test_sum_score(self, clean_users):
        """测试分数总和"""
        # 插入测试数据
        scores = [80.0, 85.0, 90.0]
        for i, score in enumerate(scores):
            clean_users.create({'name': f'SumScore{i}', 'email': f'sumscore{i}@test.com', 'age': 25, 'status': 1, 'score': score})
        
        result = clean_users.sum('score')
        # 总和应该是 255.0
        assert result is not None
        assert abs(float(result) - 255.0) < 0.01
    
    @pytest.mark.aggregate
    def test_sum_with_condition(self, clean_users):
        """测试带条件的总和"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'SumCond{i}', 'email': f'sumcond{i}@test.com', 'age': 20 + i * 5, 'status': 1 if i < 3 else 0, 'score': 80.0})
        
        result = clean_users.where('status', 1).sum('age')
        # 20 + 25 + 30 = 75
        assert result is not None
        assert float(result) == 75.0
    
    @pytest.mark.aggregate
    def test_sum_empty_table(self, clean_users):
        """测试空表的总和"""
        result = clean_users.sum('age')
        assert result is None
    
    @pytest.mark.aggregate
    def test_sum_invalid_column(self, clean_users):
        """测试无效列名"""
        with pytest.raises(Exception):
            clean_users.sum('non_existent_column')


class TestAggregateCombined:
    """测试聚合函数组合使用"""
    
    @pytest.mark.aggregate
    def test_count_then_max(self, clean_users):
        """测试先 count 后 max"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'CountMax{i}', 'email': f'countmax{i}@test.com', 'age': 20 + i * 5, 'status': 1, 'score': 80.0 + i})
        
        count_result = clean_users.count()
        max_result = clean_users.max('age')
        
        assert count_result == 5
        assert max_result == 40
    
    @pytest.mark.aggregate
    def test_aggregate_with_groupby(self, clean_users):
        """测试聚合函数配合 GROUP BY"""
        # 插入测试数据
        for i in range(6):
            status = 1 if i < 3 else 0
            clean_users.create({'name': f'GroupAgg{i}', 'email': f'groupagg{i}@test.com', 'age': 20 + i, 'status': status, 'score': 80.0})
        
        # 使用 GROUP BY 和聚合
        result = clean_users.select('status', 'count(*) as cnt').groupby('status').get()
        assert len(result) == 2  # 两种 status
    
    @pytest.mark.aggregate
    def test_aggregate_with_having(self, clean_users):
        """测试聚合函数配合 HAVING"""
        # 插入测试数据
        for i in range(6):
            status = 1 if i < 4 else 0  # status=1 有4条, status=0 有2条
            clean_users.create({'name': f'HavingAgg{i}', 'email': f'havingagg{i}@test.com', 'age': 20 + i, 'status': status, 'score': 80.0})
        
        # 使用 HAVING 过滤
        result = clean_users.select('status', 'count(*) as cnt').groupby('status').having('cnt', '>', 2).get()
        # 只有 status=1 的组满足 count > 2
        assert len(result) == 1
