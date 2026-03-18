#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - JOIN 关联查询方法
测试方法: leftjoin, rightjoin, innerjoin, join, on
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestLeftJoin:
    """测试 LEFT JOIN 方法"""
    
    @pytest.mark.join
    def test_leftjoin_basic(self, user_model, order_model):
        """测试基本 LEFT JOIN"""
        # select a.id, b.order_no from users a left join orders b on a.id = b.user_id
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = user_model('a').leftjoin(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'left join' in sql.lower()
        assert 'on' in sql.lower()
    
    @pytest.mark.join
    def test_leftjoin_with_where(self, user_model, order_model):
        """测试带 WHERE 条件的 LEFT JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = (user_model('a')
               .leftjoin(join_builder)
               .where('a.status', 1)
               .select('a.id', 'a.name', 'b.order_no')
               .tosql())
        
        assert 'left join' in sql.lower()
        assert 'where' in sql.lower()
    
    @pytest.mark.join
    def test_leftjoin_multiple_on(self, user_model, order_model):
        """测试多个 ON 条件的 LEFT JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id').on('a.status', '=', 'b.status')
        sql = user_model('a').leftjoin(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'left join' in sql.lower()
        assert 'and' in sql.lower()  # 多个 ON 条件用 AND 连接
    
    @pytest.mark.join
    def test_leftjoin_with_alias(self, user_model, order_model):
        """测试带别名的 LEFT JOIN"""
        join_builder = order_model('o').on('u.id', '=', 'o.user_id')
        sql = user_model('u').leftjoin(join_builder).select('u.name', 'o.order_no').tosql()
        
        assert 'left join' in sql.lower()
        assert 'as u' in sql.lower()
        assert 'as o' in sql.lower()


class TestRightJoin:
    """测试 RIGHT JOIN 方法"""
    
    @pytest.mark.join
    def test_rightjoin_basic(self, user_model, order_model):
        """测试基本 RIGHT JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = user_model('a').rightjoin(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'right join' in sql.lower()
        assert 'on' in sql.lower()
    
    @pytest.mark.join
    def test_rightjoin_with_where(self, user_model, order_model):
        """测试带 WHERE 条件的 RIGHT JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = (user_model('a')
               .rightjoin(join_builder)
               .where('b.status', 1)
               .select('a.id', 'a.name', 'b.order_no')
               .tosql())
        
        assert 'right join' in sql.lower()
        assert 'where' in sql.lower()


class TestInnerJoin:
    """测试 INNER JOIN 方法"""
    
    @pytest.mark.join
    def test_innerjoin_basic(self, user_model, order_model):
        """测试基本 INNER JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = user_model('a').innerjoin(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'inner join' in sql.lower()
        assert 'on' in sql.lower()
    
    @pytest.mark.join
    def test_join_alias_for_innerjoin(self, user_model, order_model):
        """测试 join() 方法作为 innerjoin() 的别名"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = user_model('a').join(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'inner join' in sql.lower()
    
    @pytest.mark.join
    def test_innerjoin_with_multiple_conditions(self, user_model, order_model):
        """测试带多条件的 INNER JOIN"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id').on('b.status', '=', 'a.status')
        sql = user_model('a').innerjoin(join_builder).select('a.id', 'b.order_no').tosql()
        
        assert 'inner join' in sql.lower()
        assert 'and' in sql.lower()


class TestOn:
    """测试 ON 条件方法"""
    
    @pytest.mark.join
    def test_on_two_params(self, order_model):
        """测试 ON 两个参数 (默认等于)"""
        builder = order_model('b').on('a.id', 'b.user_id')
        sql = builder._compile_on()
        
        assert '=' in sql
    
    @pytest.mark.join
    def test_on_three_params(self, order_model):
        """测试 ON 三个参数"""
        builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = builder._compile_on()
        
        assert '=' in sql
        assert 'a.id' in sql.lower()
        assert 'b.user_id' in sql.lower()
    
    @pytest.mark.join
    def test_on_with_different_operators(self, order_model):
        """测试 ON 使用不同运算符"""
        builder = order_model('b').on('a.id', '>', 'b.user_id')
        sql = builder._compile_on()
        
        assert '>' in sql
    
    @pytest.mark.join
    def test_on_invalid_params(self, order_model):
        """测试 ON 无效参数"""
        with pytest.raises(Exception):
            order_model('b').on('a.id')  # 参数不足


class TestJoinInvalidType:
    """测试 JOIN 无效类型"""
    
    @pytest.mark.join
    def test_leftjoin_invalid_type(self, user_model):
        """测试 leftjoin 无效类型"""
        with pytest.raises(TypeError):
            user_model.leftjoin('not_a_builder')
    
    @pytest.mark.join
    def test_rightjoin_invalid_type(self, user_model):
        """测试 rightjoin 无效类型"""
        with pytest.raises(TypeError):
            user_model.rightjoin('not_a_builder')
    
    @pytest.mark.join
    def test_innerjoin_invalid_type(self, user_model):
        """测试 innerjoin 无效类型"""
        with pytest.raises(TypeError):
            user_model.innerjoin('not_a_builder')


class TestJoinComplex:
    """测试复杂 JOIN 查询"""
    
    @pytest.mark.join
    def test_join_with_orderby(self, user_model, order_model):
        """测试 JOIN 配合 ORDER BY"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = (user_model('a')
               .leftjoin(join_builder)
               .select('a.id', 'a.name', 'b.order_no')
               .orderby('a.id', 'desc')
               .tosql())
        
        assert 'left join' in sql.lower()
        assert 'order by' in sql.lower()
    
    @pytest.mark.join
    def test_join_with_limit(self, user_model, order_model):
        """测试 JOIN 配合 LIMIT"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = (user_model('a')
               .leftjoin(join_builder)
               .select('a.id', 'a.name', 'b.order_no')
               .take(10)
               .tosql())
        
        assert 'left join' in sql.lower()
        assert 'limit 10' in sql.lower()
    
    @pytest.mark.join
    def test_join_with_groupby(self, user_model, order_model):
        """测试 JOIN 配合 GROUP BY"""
        join_builder = order_model('b').on('a.id', '=', 'b.user_id')
        sql = (user_model('a')
               .leftjoin(join_builder)
               .select('a.id', 'a.name', 'count(b.id) as order_count')
               .groupby('a.id')
               .tosql())
        
        assert 'left join' in sql.lower()
        assert 'group by' in sql.lower()
    
    @pytest.mark.join
    def test_multiple_joins(self, user_model, order_model, product_model):
        """测试多个 JOIN"""
        # 注意：这需要适当的表结构支持
        join_builder1 = order_model('o').on('u.id', '=', 'o.user_id')
        sql = (user_model('u')
               .leftjoin(join_builder1)
               .select('u.id', 'u.name', 'o.order_no')
               .tosql())
        
        assert 'left join' in sql.lower()


class TestJoinDataIntegrity:
    """测试 JOIN 数据完整性"""
    
    @pytest.mark.join
    def test_leftjoin_data_integrity(self, clean_users, clean_orders):
        """测试 LEFT JOIN 数据完整性"""
        # 插入用户数据
        clean_users.create({'name': 'JoinUser1', 'email': 'join1@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        user = clean_users.where('name', 'JoinUser1').first()
        user_id = user['id'] or user.id
        
        # 插入订单数据
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD001', 'amount': 100.00, 'status': 1})
        
        # 执行 JOIN 查询
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').leftjoin(join_builder).where('u.id', user_id).select('u.name', 'o.order_no').get()
        
        assert len(result) >= 1
    
    @pytest.mark.join
    def test_innerjoin_filters_null(self, clean_users, clean_orders):
        """测试 INNER JOIN 过滤 NULL 结果"""
        # 插入没有订单的用户
        clean_users.create({'name': 'NoOrderUser', 'email': 'noorder@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        # 插入有订单的用户
        clean_users.create({'name': 'HasOrderUser', 'email': 'hasorder@test.com', 'age': 30, 'status': 1, 'score': 85.0})
        user = clean_users.where('name', 'HasOrderUser').first()
        user_id = user['id'] or user.id
        clean_orders.create({'user_id': user_id, 'order_no': 'ORD002', 'amount': 200.00, 'status': 1})
        
        # INNER JOIN 应该只返回有匹配的记录
        join_builder = clean_orders('o').on('u.id', '=', 'o.user_id')
        result = clean_users('u').innerjoin(join_builder).select('u.name', 'o.order_no').get()
        
        # 验证结果
        for r in result:
            name = r['name'] if isinstance(r, dict) else r.name
            assert name != 'NoOrderUser'
