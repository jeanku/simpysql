#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - SELECT 查询相关方法
测试方法: select, get, first, take, offset, orderby, groupby, having, tosql
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestSelect:
    """测试 SELECT 查询方法"""
    
    @pytest.mark.select
    def test_select_all(self, user_model):
        """测试查询所有字段 (SELECT *)"""
        sql = user_model.tosql()
        assert 'select * from' in sql.lower()
        assert 'test_users' in sql.lower()
    
    @pytest.mark.select
    def test_select_specific_columns(self, user_model):
        """测试选择特定字段"""
        sql = user_model.select('id', 'name', 'email').tosql()
        assert 'select`id`,`name`,`email`' in sql.lower().replace(' ', '')
    
    @pytest.mark.select
    def test_select_single_column(self, user_model):
        """测试选择单个字段"""
        sql = user_model.select('name').tosql()
        assert '`name`' in sql.lower()
    
    @pytest.mark.select
    def test_select_with_alias(self, user_model):
        """测试表别名"""
        sql = user_model('a').select('a.id', 'a.name').tosql()
        assert 'as a' in sql.lower()
        assert 'a.id' in sql.lower() or '`a`.`id`' in sql.lower()
    
    @pytest.mark.select
    def test_select_with_expression(self, user_model):
        """测试使用表达式选择字段"""
        sql = user_model.select('count(*) as total').tosql()
        assert 'count(*) as total' in sql.lower()
    
    @pytest.mark.select
    def test_select_with_function(self, user_model):
        """测试使用函数选择字段"""
        sql = user_model.select('max(id) as max_id').tosql()
        assert 'max(id)' in sql.lower()
    
    @pytest.mark.select
    def test_select_distinct(self, user_model):
        """测试 DISTINCT 查询"""
        sql = user_model.select('distinct(name)').tosql()
        assert 'distinct' in sql.lower()


class TestGetAndFirst:
    """测试 get() 和 first() 方法"""
    
    @pytest.mark.select
    def test_get_returns_list(self, user_model):
        """测试 get() 返回列表"""
        result = user_model.get()
        assert isinstance(result, list)
    
    @pytest.mark.select
    def test_first_returns_dict_or_empty(self, user_model):
        """测试 first() 返回字典或空"""
        result = user_model.first()
        # first() 返回 Dynamic 对象或空字典
        assert result is not None or result == {}
    
    @pytest.mark.select
    def test_first_with_condition(self, user_model):
        """测试带条件的 first()"""
        # 先插入测试数据
        user_model.create({'name': 'FirstTest', 'email': 'first@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = user_model.where('name', 'FirstTest').first()
        assert result is not None
        assert result['name'] == 'FirstTest' or result.name == 'FirstTest'
    
    @pytest.mark.select
    def test_get_with_take(self, user_model):
        """测试 get() 配合 take() 限制数量"""
        # 插入多条数据
        for i in range(5):
            user_model.create({'name': f'TakeTest{i}', 'email': f'take{i}@test.com', 'age': 20 + i, 'status': 1, 'score': 80.0 + i})
        
        result = user_model.where('name', 'like', 'TakeTest%').take(3).get()
        assert len(result) == 3


class TestTakeAndOffset:
    """测试 take() 和 offset() 方法"""
    
    @pytest.mark.select
    def test_take_positive_number(self, user_model):
        """测试 take() 正数"""
        sql = user_model.take(5).tosql()
        assert 'limit 5' in sql.lower()
    
    @pytest.mark.select
    def test_take_invalid_number(self, user_model):
        """测试 take() 无效数字"""
        with pytest.raises(Exception):
            user_model.take(0)
        
        with pytest.raises(Exception):
            user_model.take(-1)
    
    @pytest.mark.select
    def test_offset_positive_number(self, user_model):
        """测试 offset() 正数"""
        sql = user_model.offset(10).tosql()
        assert 'offset 10' in sql.lower()
    
    @pytest.mark.select
    def test_offset_invalid_number(self, user_model):
        """测试 offset() 无效数字"""
        with pytest.raises(Exception):
            user_model.offset(0)
        
        with pytest.raises(Exception):
            user_model.offset(-1)
    
    @pytest.mark.select
    def test_take_with_offset(self, user_model):
        """测试 take() 配合 offset()"""
        sql = user_model.take(5).offset(10).tosql()
        assert 'limit 5' in sql.lower()
        assert 'offset 10' in sql.lower()


class TestOrderBy:
    """测试 orderby() 方法"""
    
    @pytest.mark.select
    def test_orderby_default_asc(self, user_model):
        """测试默认升序排序"""
        sql = user_model.orderby('id').tosql()
        assert 'order by' in sql.lower()
        assert 'desc' not in sql.lower()
    
    @pytest.mark.select
    def test_orderby_desc(self, user_model):
        """测试降序排序"""
        sql = user_model.orderby('id', 'desc').tosql()
        assert 'order by' in sql.lower()
        assert 'desc' in sql.lower()
    
    @pytest.mark.select
    def test_orderby_asc_explicit(self, user_model):
        """测试显式升序排序"""
        sql = user_model.orderby('id', 'asc').tosql()
        assert 'order by' in sql.lower()
    
    @pytest.mark.select
    def test_orderby_multiple_columns(self, user_model):
        """测试多字段排序"""
        sql = user_model.orderby('status', 'desc').orderby('id', 'asc').tosql()
        assert 'order by' in sql.lower()
        # 验证多个排序字段


class TestGroupBy:
    """测试 groupby() 方法"""
    
    @pytest.mark.select
    def test_groupby_single_column(self, user_model):
        """测试单字段分组"""
        sql = user_model.select('status', 'count(*) as cnt').groupby('status').tosql()
        assert 'group by' in sql.lower()
        assert '`status`' in sql.lower()
    
    @pytest.mark.select
    def test_groupby_multiple_columns(self, user_model):
        """测试多字段分组"""
        sql = user_model.select('status', 'age', 'count(*) as cnt').groupby('status', 'age').tosql()
        assert 'group by' in sql.lower()
    
    @pytest.mark.select
    def test_groupby_with_function(self, user_model):
        """测试使用函数分组"""
        sql = user_model.select('left(name, 1) as first_letter', 'count(*) as cnt').groupby('left(name, 1)').tosql()
        assert 'group by' in sql.lower()


class TestHaving:
    """测试 having() 方法"""
    
    @pytest.mark.select
    def test_having_with_two_params(self, user_model):
        """测试 having() 两个参数 (默认等于)"""
        sql = user_model.select('status', 'count(*) as cnt').groupby('status').having('cnt', 5).tosql()
        assert 'having' in sql.lower()
        assert '=' in sql
    
    @pytest.mark.select
    def test_having_with_three_params(self, user_model):
        """测试 having() 三个参数"""
        sql = user_model.select('status', 'count(*) as cnt').groupby('status').having('cnt', '>', 2).tosql()
        assert 'having' in sql.lower()
        assert '>' in sql
    
    @pytest.mark.select
    def test_having_invalid_params(self, user_model):
        """测试 having() 无效参数"""
        with pytest.raises(Exception):
            user_model.having('column').tosql()


class TestToSql:
    """测试 tosql() 方法"""
    
    @pytest.mark.select
    def test_tosql_returns_string(self, user_model):
        """测试 tosql() 返回字符串"""
        sql = user_model.tosql()
        assert isinstance(sql, str)
    
    @pytest.mark.select
    def test_tosql_complex_query(self, user_model):
        """测试复杂查询的 SQL 生成"""
        sql = (user_model('a')
               .select('a.id', 'a.name')
               .where('a.status', 1)
               .where('a.age', '>', 18)
               .orderby('a.id', 'desc')
               .take(10)
               .offset(5)
               .tosql())
        
        assert 'select' in sql.lower()
        assert 'from' in sql.lower()
        assert 'where' in sql.lower()
        assert 'order by' in sql.lower()
        assert 'limit' in sql.lower()
        assert 'offset' in sql.lower()


class TestExecute:
    """测试 execute() 原生SQL方法"""
    
    @pytest.mark.select
    def test_execute_select(self, user_model):
        """测试执行原生 SELECT SQL"""
        result = user_model.execute('SELECT 1 as num')
        assert result is not None
    
    @pytest.mark.select
    def test_execute_with_response(self, user_model):
        """测试 execute() 返回 Response 对象"""
        from simpysql.Util.Response import Response
        result = user_model.execute('SELECT 1 as num')
        # execute 返回 Response 对象
        assert hasattr(result, 'data') or hasattr(result, 'tolist')


class TestDatabase:
    """测试 database() 切换数据库方法"""
    
    @pytest.mark.select
    def test_database_method(self, user_model):
        """测试切换数据库"""
        # 注意：这个测试需要确保目标数据库存在
        builder = user_model.database('default')
        assert builder is not None  # 返回 builder 实例支持链式调用
