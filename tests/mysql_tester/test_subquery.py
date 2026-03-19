#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 子查询方法
测试方法: subquery, where 子查询
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestSubquery:
    """测试 subquery() 方法"""
    
    @pytest.mark.subquery
    def test_subquery_basic(self, user_model):
        """测试基本子查询"""
        # select id from (select * from users where id=1) as tmp
        submodel = user_model.where('id', '=', 1)
        sql = user_model.select('id').subquery(submodel).tosql()
        
        assert 'select' in sql.lower()
        assert 'from' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_alias(self, user_model):
        """测试带别名的子查询"""
        # select a.id from (select * from users) as a
        submodel = user_model.where('status', '=', 1)
        sql = user_model.select('a.id', 'a.name').subquery(submodel, 'a').tosql()
        
        assert 'as a' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_string_table(self, user_model):
        """测试字符串表名子查询"""
        sql = user_model.select('id').subquery('test_users', 't').tosql()
        
        assert 'as t' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_multiple(self, user_model):
        """测试多个子查询"""
        # select a.id from (subquery1) as a, (subquery2) as b
        submodel1 = user_model.where('status', '=', 1)
        submodel2 = user_model.where('age', '>', 25)
        
        sql = (user_model
               .select('a.id', 'a.name')
               .subquery(submodel1, 'a')
               .subquery(submodel2, 'b')
               .tosql())
        
        assert 'as a' in sql.lower()
        assert 'as b' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_where(self, user_model):
        """测试子查询配合 WHERE"""
        submodel = user_model.where('status', '=', 1)
        sql = (user_model
               .select('a.id', 'a.name')
               .subquery(submodel, 'a')
               .where('a.age', '>', 25)
               .tosql())
        
        assert 'where' in sql.lower()


class TestWhereSubquery:
    """测试 WHERE 子查询"""
    
    @pytest.mark.subquery
    def test_where_in_subquery(self, user_model):
        """测试 IN 子查询"""
        # select * from users where id in (select id from users where status=1)
        subquery = user_model.select('id').where('status', 1)
        sql = user_model.where('id', 'in', subquery).tosql()
        
        assert 'in' in sql.lower()
        assert 'select' in sql.lower()
    
    @pytest.mark.subquery
    def test_where_not_in_subquery(self, user_model):
        """测试 NOT IN 子查询"""
        subquery = user_model.select('id').where('status', 0)
        sql = user_model.where('id', 'not in', subquery).tosql()
        
        assert 'not in' in sql.lower()
    
    @pytest.mark.subquery
    def test_where_equals_subquery(self, user_model):
        """测试等于子查询"""
        # select * from users where id = (select max(id) from users)
        subquery = user_model.select('max(id) as id')
        sql = user_model.where('id', '=', subquery).tosql()
        
        assert '=' in sql
        assert 'select' in sql.lower()
    
    @pytest.mark.subquery
    def test_where_comparison_subquery(self, user_model):
        """测试比较运算符子查询"""
        subquery = user_model.select('avg(age) as avg_age')
        sql = user_model.where('age', '>', subquery).tosql()
        
        assert '>' in sql
        assert 'select' in sql.lower()


class TestSubqueryDataIntegrity:
    """测试子查询数据完整性"""
    
    @pytest.mark.subquery
    def test_subquery_returns_correct_data(self, clean_users):
        """测试子查询返回正确数据"""
        # 插入测试数据
        clean_users.create({'name': 'SubqueryTest1', 'email': 'sub1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'SubqueryTest2', 'email': 'sub2@test.com', 'age': 30, 'status': 0, 'score': 85.0})
        
        # 使用子查询
        subquery = clean_users.select('id').where('status', 1)
        result = clean_users.where('id', 'in', subquery).get()
        
        # 验证结果
        for r in result:
            status = r['status'] if isinstance(r, dict) else r.status
            assert status == 1
    
    @pytest.mark.subquery
    def test_subquery_with_aggregate(self, clean_users):
        """测试子查询配合聚合函数"""
        # 插入测试数据
        clean_users.create({'name': 'SubAgg1', 'email': 'subagg1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        clean_users.create({'name': 'SubAgg2', 'email': 'subagg2@test.com', 'age': 35, 'status': 1, 'score': 85.0})
        
        # 使用聚合子查询
        avg_age = clean_users.avg('age')
        result = clean_users.where('age', '>', avg_age).get()
        
        for r in result:
            age = r['age'] if isinstance(r, dict) else r.age
            assert age > avg_age


class TestSubqueryComplex:
    """测试复杂子查询"""
    
    @pytest.mark.subquery
    def test_subquery_with_join(self, user_model, order_model):
        """测试子查询配合 JOIN"""
        subquery = (user_model('a')
                    .where('a.status', 1)
                    .leftjoin(order_model('b').on('a.id', '=', 'b.user_id'))
                    .select('a.id', 'a.name'))
        
        sql = user_model.select('id').subquery(subquery, 'sub').tosql()
        
        assert 'left join' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_orderby_limit(self, user_model):
        """测试子查询配合 ORDER BY 和 LIMIT"""
        submodel = user_model.where('status', 1).orderby('id', 'desc').take(10)
        sql = user_model.select('id').subquery(submodel, 'top_users').tosql()
        
        assert 'order by' in sql.lower()
        assert 'limit' in sql.lower()
    
    @pytest.mark.subquery
    def test_nested_subquery(self, user_model):
        """测试嵌套子查询"""
        # 内层子查询
        inner_subquery = user_model.where('status', 1).select('id')
        
        # 外层使用内层子查询
        sql = user_model.where('id', 'in', inner_subquery).select('id', 'name').tosql()
        
        assert 'select' in sql.lower()
        assert 'in' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_groupby(self, user_model):
        """测试子查询配合 GROUP BY"""
        submodel = (user_model
                    .select('status', 'count(*) as cnt')
                    .groupby('status')
                    .having('cnt', '>', 1))
        
        sql = user_model.select('status').subquery(submodel, 'grouped').tosql()
        
        assert 'group by' in sql.lower()
        assert 'having' in sql.lower()


class TestSubqueryFromClause:
    """测试 FROM 子句子查询"""
    
    @pytest.mark.subquery
    def test_from_subquery_single(self, user_model):
        """测试单个 FROM 子查询"""
        submodel = user_model.where('status', 1)
        sql = user_model.select('id').subquery(submodel, 'active_users').tosql()
        
        # 验证子查询被正确嵌入
        assert 'from' in sql.lower()
    
    @pytest.mark.subquery
    def test_from_subquery_with_alias_access(self, user_model):
        """测试 FROM 子查询别名访问"""
        submodel = user_model.where('id', '>=', 1)
        sql = (user_model
               .select('a.id', 'a.name')
               .subquery(submodel, 'a')
               .where('a.status', 1)
               .tosql())
        
        assert 'as a' in sql.lower()
        assert 'where' in sql.lower()


class TestSubqueryEdgeCases:
    """测试子查询边界情况"""
    
    @pytest.mark.subquery
    def test_empty_subquery(self, clean_users):
        """测试空子查询结果"""
        # 使用不会匹配任何记录的子查询
        subquery = clean_users.select('id').where('name', 'NonExistentUser')
        result = clean_users.where('id', 'in', subquery).get()
        
        assert len(result) == 0
    
    @pytest.mark.subquery
    def test_subquery_with_orwhere(self, user_model):
        """测试子查询配合 ORWHERE"""
        subquery = user_model.select('id').where('status', 1)
        sql = user_model.where('id', 'in', subquery).orwhere('age', '>', 50).tosql()
        
        assert 'in' in sql.lower()
        assert 'or' in sql.lower()
    
    @pytest.mark.subquery
    def test_subquery_with_whereor(self, user_model):
        """测试子查询配合 WHEREOR"""
        subquery = user_model.select('id').where('status', 0)
        sql = user_model.where('id', 'in', subquery).whereor([{'age': 25}, {'age': 30}]).tosql()
        
        assert 'in' in sql.lower()
        assert 'or' in sql.lower()
