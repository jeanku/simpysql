#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - WHERE 条件查询方法
测试方法: where, orwhere, whereor, exist
"""

import pytest
from tests.mysql_tester.models import User, Order, Product, Article


class TestWhereBasic:
    """测试基本 WHERE 条件"""
    
    @pytest.mark.where
    def test_where_single_param_dict(self, user_model):
        """测试 where() 单参数字典形式"""
        sql = user_model.where({'status': 1}).tosql()
        assert 'where' in sql.lower()
        assert '`status`' in sql.lower()
    
    @pytest.mark.where
    def test_where_two_params(self, user_model):
        """测试 where() 两个参数 (等于)"""
        sql = user_model.where('id', 1).tosql()
        assert 'where' in sql.lower()
        assert '`id`' in sql.lower()
    
    @pytest.mark.where
    def test_where_three_params_equal(self, user_model):
        """测试 where() 三个参数显式等于"""
        sql = user_model.where('id', '=', 1).tosql()
        assert 'where' in sql.lower()
        assert '`id`' in sql.lower()


class TestWhereOperators:
    """测试 WHERE 条件运算符"""
    
    @pytest.mark.where
    def test_where_greater_than(self, user_model):
        """测试大于运算符"""
        sql = user_model.where('age', '>', 18).tosql()
        assert '>' in sql
    
    @pytest.mark.where
    def test_where_greater_equal(self, user_model):
        """测试大于等于运算符"""
        sql = user_model.where('age', '>=', 18).tosql()
        assert '>=' in sql
    
    @pytest.mark.where
    def test_where_less_than(self, user_model):
        """测试小于运算符"""
        sql = user_model.where('age', '<', 60).tosql()
        assert '<' in sql
        assert '<=' not in sql
    
    @pytest.mark.where
    def test_where_less_equal(self, user_model):
        """测试小于等于运算符"""
        sql = user_model.where('age', '<=', 60).tosql()
        assert '<=' in sql
    
    @pytest.mark.where
    def test_where_not_equal(self, user_model):
        """测试不等于运算符"""
        sql = user_model.where('status', '!=', 0).tosql()
        assert '!=' in sql
    
    @pytest.mark.where
    def test_where_not_equal_alt(self, user_model):
        """测试不等于运算符 (<>)"""
        sql = user_model.where('status', '<>', 0).tosql()
        assert '<>' in sql


class TestWhereInAndNotIn:
    """测试 IN 和 NOT IN 条件"""
    
    @pytest.mark.where
    def test_where_in_list(self, user_model):
        """测试 IN 条件"""
        sql = user_model.where('id', 'in', [1, 2, 3]).tosql()
        assert 'in' in sql.lower()
        assert '(1,2,3)' in sql.replace(' ', '').lower()
    
    @pytest.mark.where
    def test_where_in_tuple(self, user_model):
        """测试 IN 条件 (元组)"""
        sql = user_model.where('id', 'in', (1, 2, 3)).tosql()
        assert 'in' in sql.lower()
    
    @pytest.mark.where
    def test_where_not_in(self, user_model):
        """测试 NOT IN 条件"""
        sql = user_model.where('id', 'not in', [1, 2, 3]).tosql()
        assert 'not in' in sql.lower()


class TestWhereBetween:
    """测试 BETWEEN 条件"""
    
    @pytest.mark.where
    def test_where_between_list(self, user_model):
        """测试 BETWEEN 条件"""
        sql = user_model.where('age', 'between', [18, 60]).tosql()
        assert 'between' in sql.lower()
        assert 'and' in sql.lower()
    
    @pytest.mark.where
    def test_where_between_tuple(self, user_model):
        """测试 BETWEEN 条件 (元组)"""
        sql = user_model.where('age', 'between', (18, 60)).tosql()
        assert 'between' in sql.lower()
    
    @pytest.mark.where
    def test_where_not_between(self, user_model):
        """测试 NOT BETWEEN 条件"""
        sql = user_model.where('age', 'not between', [18, 60]).tosql()
        assert 'not between' in sql.lower()
    
    @pytest.mark.where
    def test_where_between_invalid_params(self, user_model):
        """测试 BETWEEN 无效参数"""
        # BETWEEN 需要两个值
        with pytest.raises(Exception):
            user_model.where('age', 'between', [1]).tosql()


class TestWhereLike:
    """测试 LIKE 条件"""
    
    @pytest.mark.where
    def test_where_like(self, user_model):
        """测试 LIKE 条件"""
        sql = user_model.where('name', 'like', '张%').tosql()
        assert 'like' in sql.lower()
    
    @pytest.mark.where
    def test_where_like_with_wildcards(self, user_model):
        """测试 LIKE 条件带通配符"""
        sql = user_model.where('name', 'like', '%测试%').tosql()
        assert 'like' in sql.lower()
    
    @pytest.mark.where
    def test_where_not_like(self, user_model):
        """测试 NOT LIKE 条件"""
        sql = user_model.where('name', 'not like', '%测试%').tosql()
        assert 'not like' in sql.lower()


class TestWhereNull:
    """测试 NULL 相关条件"""
    
    @pytest.mark.where
    def test_where_is(self, user_model):
        """测试 IS 条件"""
        sql = user_model.where('status', 'is', None).tosql()
        assert 'is' in sql.lower()
    
    @pytest.mark.where
    def test_where_is_not(self, user_model):
        """测试 IS NOT 条件"""
        sql = user_model.where('status', 'is not', None).tosql()
        assert 'is not' in sql.lower()


class TestWhereMultiple:
    """测试多条件 WHERE"""
    
    @pytest.mark.where
    def test_where_multiple_dict(self, user_model):
        """测试多条件字典形式"""
        sql = user_model.where({'status': 1, 'age': 25}).tosql()
        assert 'where' in sql.lower()
        assert 'and' in sql.lower()
    
    @pytest.mark.where
    def test_where_chained(self, user_model):
        """测试链式 WHERE"""
        sql = user_model.where('status', 1).where('age', '>', 18).tosql()
        assert 'where' in sql.lower()
        assert 'and' in sql.lower()
    
    @pytest.mark.where
    def test_where_dict_and_tuple(self, user_model):
        """测试字典和元组混合"""
        sql = user_model.where({'status': 1}).where('age', '>', 18).tosql()
        assert 'where' in sql.lower()


class TestOrWhere:
    """测试 OR WHERE 条件"""
    
    @pytest.mark.where
    def test_orwhere_two_params(self, user_model):
        """测试 orwhere() 两个参数"""
        sql = user_model.where('id', 1).orwhere('id', 2).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_three_params(self, user_model):
        """测试 orwhere() 三个参数"""
        sql = user_model.where('id', 1).orwhere('id', '=', 2).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_dict(self, user_model):
        """测试 orwhere() 字典形式"""
        sql = user_model.where('id', 1).orwhere({'status': 1}).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_with_operators(self, user_model):
        """测试 orwhere() 带运算符"""
        sql = user_model.where('id', 1).orwhere('age', '>', 30).tosql()
        assert 'or' in sql.lower()
        assert '>' in sql
    
    @pytest.mark.where
    def test_orwhere_in(self, user_model):
        """测试 orwhere() IN 条件"""
        sql = user_model.where('id', 1).orwhere('id', 'in', [2, 3, 4]).tosql()
        assert 'or' in sql.lower()
        assert 'in' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_between(self, user_model):
        """测试 orwhere() BETWEEN 条件"""
        sql = user_model.where('id', 1).orwhere('age', 'between', [20, 30]).tosql()
        assert 'or' in sql.lower()
        assert 'between' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_like(self, user_model):
        """测试 orwhere() LIKE 条件"""
        sql = user_model.where('id', 1).orwhere('name', 'like', '张%').tosql()
        assert 'or' in sql.lower()
        assert 'like' in sql.lower()
    
    @pytest.mark.where
    def test_orwhere_list(self, user_model):
        """测试 orwhere() 列表形式 (AND 嵌套)"""
        # select * from table where id=1 or (id > 2 and id < 5)
        sql = user_model.where('id', 1).orwhere([('id', '>', 2), ('id', '<', 5)]).tosql()
        assert 'or' in sql.lower()


class TestWhereOr:
    """测试 whereor() 方法"""
    
    @pytest.mark.where
    def test_whereor_single_dict(self, user_model):
        """测试 whereor() 单个字典"""
        sql = user_model.where('id', 1).whereor([{'status': 1}]).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_whereor_multiple_dicts(self, user_model):
        """测试 whereor() 多个字典"""
        sql = user_model.where('id', 1).whereor([{'status': 1}, {'age': 25}]).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_whereor_tuples(self, user_model):
        """测试 whereor() 元组形式"""
        sql = user_model.where('id', 1).whereor([('status', 1), ('age', '>', 25)]).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_whereor_mixed(self, user_model):
        """测试 whereor() 混合形式"""
        sql = user_model.where('id', 1).whereor([
            {'status': 1, 'name': 'test'},
            ('age', '>', 25),
            [['score', '>', 80], ['score', '<', 90]]
        ]).tosql()
        assert 'or' in sql.lower()
    
    @pytest.mark.where
    def test_whereor_invalid_params(self, user_model):
        """测试 whereor() 无效参数"""
        with pytest.raises(Exception):
            user_model.whereor({'status': 1}).tosql()  # 必须是列表


class TestExist:
    """测试 exist() 方法"""
    
    @pytest.mark.where
    def test_exist_returns_bool(self, user_model):
        """测试 exist() 返回布尔值"""
        result = user_model.exist()
        assert isinstance(result, bool)
    
    @pytest.mark.where
    def test_exist_with_condition(self, user_model):
        """测试带条件的 exist()"""
        # 先插入测试数据
        user_model.create({'name': 'ExistTest', 'email': 'exist@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        
        result = user_model.where('name', 'ExistTest').exist()
        assert result is True
    
    @pytest.mark.where
    def test_exist_false(self, user_model):
        """测试 exist() 返回 False"""
        result = user_model.where('name', 'NonExistentUser12345').exist()
        assert result is False


class TestWhereInvalidOperator:
    """测试无效运算符"""
    
    @pytest.mark.where
    def test_where_invalid_operator(self, user_model):
        """测试无效运算符抛出异常"""
        with pytest.raises(Exception) as excinfo:
            user_model.where('id', '<<<', 1).tosql()
        assert 'operator key world not found' in str(excinfo.value)
    
    @pytest.mark.where
    def test_orwhere_invalid_operator(self, user_model):
        """测试 orwhere 无效运算符抛出异常"""
        with pytest.raises(Exception) as excinfo:
            user_model.where('id', 1).orwhere('id', '<<<', 2).tosql()
        assert 'operator key world not found' in str(excinfo.value)
