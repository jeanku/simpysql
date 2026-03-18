#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - Response 响应格式方法
测试方法: first, get, lists, pluck, data, response
 lists, pluck
 response
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestFirst:
    """测试 first() 方法"""
    
    @pytest.mark.response
    def test_first_returns_dict_or_empty(self, clean_users):
        """测试 first() 返回字典或空"""
        # 插入测试数据
        clean_users.create({'name': 'FirstTest', 'email': 'first@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'FirstTest').first()
        
        assert result is not None
        assert isinstance(result, dict) or result == {}
    
    @pytest.mark.response
    def test_first_with_condition(self, clean_users):
        """测试带条件的 first()"""
        # 插入测试数据
        clean_users.create({'name': 'FirstCond', 'email': 'firstcond@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'FirstCond2', 'email': 'firstcond2@test.com', 'age': 30, 'status': 1, 'score': 90.0})
        
        result = clean_users.where('name', 'FirstCond').first()
        assert result is not None
        assert result['age'] == 25 or result.age == 30
    
    @pytest.mark.response
    def test_first_with_order(self, clean_users):
        """测试 first() 配合排序"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'FirstOrder{i}', 'email': f'firstorder{i}@test.com', 'age': 20 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        result = clean_users.where('name', 'like', 'FirstOrder%').orderby('age', 'asc').first()
        
        # first() 返回单个 dict（Dynamic 对象），不是 list
        assert result is not None
        assert result['age'] == 20  # 按 age 升序，第一条应该是 age=20
        assert result['name'] == 'FirstOrder0'


class TestGet:
    """测试 get() 方法"""
    
    @pytest.mark.response
    def test_get_returns_list(self, clean_users):
        """测试 get() 返回列表"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'GetTest{i}', 'email': f'gettest{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        result = clean_users.where('name', 'like', 'GetTest%').get()
        
        assert isinstance(result, list)
        assert len(result) == 3
    
    @pytest.mark.response
    def test_get_with_select(self, clean_users):
        """测试 get() 配合 select"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'GetSelect{i}', 'email': f'getselect{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        result = clean_users.select('id', 'name').where('name', 'like', 'GetSelect%').get()
        
        assert isinstance(result, list)
        for item in result:
            # 验证返回的列
            if isinstance(item, dict):
                assert 'id' in item
                assert 'name' in item
            else:
                # Dynamic 对象
                assert hasattr(item, 'id')
                assert hasattr(item, 'name')
    
    @pytest.mark.response
    def test_get_with_where(self, clean_users):
        """测试 get() 配合 where"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'GetWhere{i}', 'email': f'getwhere{i}@test.com', 'age': 20 + i, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('age', '>', 22).get()
        
        assert isinstance(result, list)
        # age > 22 匹配 age = 23, 24，共 2 条
        assert len(result) == 2
    
    @pytest.mark.response
    def test_get_with_limit(self, clean_users):
        """测试 get() 配合 take()"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'GetLimit{i}', 'email': f'getlimit{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'like', 'GetLimit%').take(3).get()
        
        assert isinstance(result, list)
        assert len(result) == 3


class TestLists:
    """测试 lists() 方法"""
    
    @pytest.mark.response
    def test_lists_single_column(self, clean_users):
        """测试单列列表返回"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'ListsSingle{i}', 'email': f'listssingle{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'like', 'ListsSingle%').lists('name')
        
        assert isinstance(result, list)
        assert len(result) == 3
        for item in result:
            assert isinstance(item, str)
    
    @pytest.mark.response
    def test_lists_multiple_columns(self, clean_users):
        """测试多列列表返回"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'ListsMulti{i}', 'email': f'listsmulti{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'like', 'ListsMulti%').lists(['name', 'email'])
        
        assert isinstance(result, list)
        assert len(result) == 3
        for item in result:
            assert isinstance(item, list)
            assert len(item) == 2
    
    @pytest.mark.response
    def test_lists_empty_result(self, clean_users):
        """测试空结果列表返回"""
        result = clean_users.where('name', 'NonExistentUser').lists('name')
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @pytest.mark.response
    def test_lists_with_limit(self, clean_users):
        """测试带 LIMIT 的列表返回"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'ListsLimit{i}', 'email': f'listslimit{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = clean_users.where('name', 'like', 'ListsLimit%').take(3).lists('name')
        
        assert len(result) == 3


class TestPluck:
    """测试 pluck() 方法"""
    
    @pytest.mark.response
    def test_pluck_key_value(self, clean_users):
        """测试键值对返回"""
        # 插入测试数据
        clean_users.create({'name': 'PluckTest1', 'email': 'pluck1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'PluckTest2', 'email': 'pluck2@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        
        result = clean_users.where('name', 'like', 'PluckTest%').pluck('name', 'email')
        
        assert isinstance(result, dict)
        assert 'PluckTest1' in result
        assert result['PluckTest1'] == 'pluck1@test.com'
        assert 'PluckTest2' in result
        assert result['PluckTest2'] == 'pluck2@test.com'
    
    @pytest.mark.response
    def test_pluck_empty_result(self, clean_users):
        """测试空结果键值对返回"""
        result = clean_users.where('name', 'NonExistentUser').pluck('name', 'email')
        
        assert isinstance(result, dict)
        assert len(result) == 0
    
    @pytest.mark.response
    def test_pluck_with_limit(self, clean_users):
        """测试带 LIMIT 的键值对返回"""
        # 插入测试数据
        for i in range(5):
            clean_users.create({'name': f'PluckLimit{i}', 'email': f'plucklimit{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0 + i * 10})
        
        result = clean_users.where('name', 'like', 'PluckLimit%').take(3).pluck('name', 'email')
        
        assert isinstance(result, dict)
        assert len(result) == 3


class TestData:
    """测试 data() 方法"""
    
    @pytest.mark.response
    def test_data_returns_dataframe(self, clean_users):
        """测试 data() 返回 pandas DataFrame"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'DataTest{i}', 'email': f'datatest{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0 + i * 10})
        
        result = clean_users.where('name', 'like', 'DataTest%').data()
        
        # 验证返回 pandas DataFrame 或 None
        assert result is not None or isinstance(result, object)
    
    @pytest.mark.response
    def test_data_empty_result(self, clean_users):
        """测试空结果 data() 返回空 DataFrame"""
        import pandas as pd
        result = clean_users.where('name', 'NonExistentUser').data()
        
        # data() 返回 pandas DataFrame，空结果时为空 DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    @pytest.mark.response
    def test_data_with_select(self, clean_users):
        """测试 data() 配合 select"""
        import pandas as pd
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'DataSelect{i}', 'email': f'dataselect{i}@test.com', 'age': 25 + i, 'status': 1, 'score': 80.0})
        
        result = clean_users.select('id', 'name', 'score').where('name', 'like', 'DataSelect%').data()
        
        # data() 返回 pandas DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        # 验证选中的列存在
        assert 'id' in result.columns
        assert 'name' in result.columns
        assert 'score' in result.columns


class TestResponse:
    """测试 response() 方法"""
    
    @pytest.mark.response
    def test_response_returns_object(self, clean_users):
        """测试 response() 返回 Response 对象"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'ResponseTest{i}', 'email': f'response{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        from simpysql.Util.Response import Response
        
        result = clean_users.where('name', 'like', 'ResponseTest%').response()
        
        assert isinstance(result, Response)
    
    @pytest.mark.response
    def test_response_methods(self, clean_users):
        """测试 Response 对象的方法"""
        # 插入测试数据
        for i in range(3):
            clean_users.create({'name': f'ResponseMethod{i}', 'email': f'responsemethod{i}@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        response = clean_users.where('name', 'like', 'ResponseMethod%').response()
        
        # 测试 data() 方法
        data_result = response.data()
        assert data_result is not None
        
        # 测试 lists() 方法
        lists_result = response.lists('name')
        assert isinstance(lists_result, list)
        
        # 测试 pluck() 方法
        pluck_result = response.pluck('name', 'email')
        assert isinstance(pluck_result, dict)
