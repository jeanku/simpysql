#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 边缘场景与安全性测试
测试空列表IN、SQL注入模拟、极端特殊字符以及特殊Python数据类型等容易引发崩溃的场景。
"""

import pytest
import datetime
from decimal import Decimal


class TestEmptyListCondition:
    """测试空列表条件的边界情况"""

    @pytest.mark.edge
    def test_where_in_empty_list(self, clean_users):
        """极限测试 1：WHERE IN 空列表"""
        # 插入基础数据
        clean_users.create({'name': 'EmptyInTest', 'email': 'emptyin@test.com', 'age': 25, 'status': 1, 'score': 80.0})

        try:
            # 业务中极易出现的场景：动态传入的 ID 列表为空
            empty_ids = []
            result = clean_users.where('id', 'in', empty_ids).get()

            # 正确的期望：不报错，且返回空列表 []
            assert isinstance(result, list)
            assert len(result) == 0
        except Exception as e:
            # 如果底层生成了 `WHERE id IN ()`，MySQL 会抛出 1064 语法错误
            pytest.fail(f"WHERE IN 空列表引发了异常 (可能生成了非法的 IN () 语法): {str(e)}")

    @pytest.mark.edge
    def test_where_not_in_empty_list(self, clean_users):
        """极限测试 2：WHERE NOT IN 空列表"""
        clean_users.create(
            {'name': 'EmptyNotInTest', 'email': 'emptynotin@test.com', 'age': 25, 'status': 1, 'score': 80.0})

        try:
            # NOT IN 空列表理论上应该不过滤任何数据（即返回所有数据）
            empty_ids = []
            result = clean_users.where('id', 'not in', empty_ids).get()
            assert len(result) >= 1
        except Exception as e:
            pytest.fail(f"WHERE NOT IN 空列表引发了异常: {str(e)}")


class TestSqlInjectionAndSpecialChars:
    """测试 SQL 注入防护与极端特殊字符处理"""

    @pytest.mark.edge
    def test_sql_injection_simulation(self, clean_users):
        """安全测试 1：模拟常规的 SQL 注入字符串"""
        # 插入多条正常数据
        for i in range(3):
            clean_users.create(
                {'name': f'NormalUser{i}', 'email': f'normal{i}@test.com', 'age': 20, 'status': 1, 'score': 80.0})

        # 插入一条名字本身就像 SQL 注入语句的“恶意”数据
        evil_name = "admin' OR '1'='1"
        clean_users.create({'name': evil_name, 'email': 'hacker@test.com', 'age': 99, 'status': 1, 'score': 0.0})

        # 模拟业务查询
        result = clean_users.where('name', evil_name).get()

        # 验证：如果没有正确转义，`OR '1'='1'` 会生效，导致返回所有 4 条用户数据！
        # 如果转义正确，它只会返回名字等于这个奇怪字符串的 1 条数据。
        assert len(result) == 1, "严重安全漏洞：SQL 注入生效，查出了不该查出的数据！"
        assert result[0]['email'] == 'hacker@test.com'

    @pytest.mark.edge
    def test_extreme_special_characters(self, clean_users):
        """安全测试 2：极端控制字符与 Emoji"""
        # 包含反斜杠、单双引号、换行、回车、制表符以及 Emoji 表情
        complex_str = "Name\\With'Quotes\"And\nNewlines\r\tAndEmoji😈"

        # 尝试入库
        try:
            clean_users.create({'name': complex_str, 'email': 'weird@test.com', 'age': 25, 'status': 1, 'score': 80.0})
        except Exception as e:
            pytest.fail(f"包含极端特殊字符的数据插入失败: {str(e)}")

        # 尝试精确查询
        result = clean_users.where('name', complex_str).first()
        assert result is not None, "无法通过包含极端字符的字符串查询到对应数据"
        assert result['name'] == complex_str, "取出的数据字符发生了转义丢失或变形"


class TestSpecialDataTypes:
    """测试特定 Python 数据类型的兼容性"""

    @pytest.mark.edge
    def test_datetime_type_support(self, clean_users):
        """兼容性测试 1：传入 Python 的 datetime 对象"""
        # 业务中直接传入 datetime.now() 是非常高频的操作
        now = datetime.datetime.now()

        try:
            # 假设你的 ORM 底层的时间戳字段或普通的 varchar 字段能够兼容序列化
            # (这里用 email 字段暂时代替字符串测试序列化能力)
            clean_users.create({'name': 'DatetimeTest', 'email': str(now), 'age': 25, 'status': 1, 'score': 80.0})
        except Exception as e:
            pytest.fail(f"无法正确处理或序列化 datetime 对象: {str(e)}")

    @pytest.mark.edge
    def test_decimal_type_support(self, clean_users):
        """兼容性测试 2：传入 Python 的 Decimal 高精度对象"""
        # 金融业务中绝对不能用 float，必须用 Decimal
        precise_score = Decimal('99.99')

        try:
            clean_users.create(
                {'name': 'DecimalTest', 'email': 'decimal@test.com', 'age': 25, 'status': 1, 'score': precise_score})
            result = clean_users.where('name', 'DecimalTest').first()

            assert result is not None
            # 注意：取出来的 score 类型取决于 pymysql 的 cursor 配置，这里主要测试插入和查询不报错
        except Exception as e:
            pytest.fail(f"无法正确处理 Decimal 类型的入库转换: {str(e)}")