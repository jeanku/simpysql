#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simpysql MySQL 测试 - 核心高危漏洞修复验证
测试之前发现的单字段插入、嵌套事务、无条件修改、select状态污染等问题是否得到妥善修复。
"""

import pytest


class TestCriticalFixes:
    """测试核心高危漏洞是否修复"""

    @pytest.mark.fixes
    def test_single_field_insert_syntax(self, clean_users):
        """修复验证 1：测试单字段 Insert 时的 SQL 语法错误 (元组转化问题)"""
        # 在修复前，只包含一个字段的字典会生成类似 (`name`,) 的错误语法，引发 MySQL 语法异常
        try:
            result = clean_users.create({'name': 'SingleFieldFix'})
            assert result is not None

            # 验证数据确实写入
            user = clean_users.where('name', 'SingleFieldFix').first()
            assert user is not None

            name = user['name'] if isinstance(user, dict) else getattr(user, 'name', None)
            assert name == 'SingleFieldFix'
        except Exception as e:
            pytest.fail(f"单字段插入失败，底层 _columnize 可能未修复逗号语法问题。异常信息: {str(e)}")

    @pytest.mark.fixes
    def test_nested_transaction_safety(self, clean_users):
        """修复验证 2：测试嵌套事务互相覆盖导致连接丢失/原子性破坏的问题"""

        def inner_transaction():
            clean_users.create({'name': 'InnerTx', 'email': 'inner@test.com', 'age': 20, 'status': 1, 'score': 80.0})

        def outer_transaction():
            clean_users.create({'name': 'OuterTx', 'email': 'outer@test.com', 'age': 20, 'status': 1, 'score': 80.0})
            # 嵌套调用另一个事务
            clean_users.transaction(inner_transaction)
            # 故意抛出异常，触发外层回滚
            raise Exception("Trigger Rollback")

        with pytest.raises(Exception, match="Trigger Rollback"):
            clean_users.transaction(outer_transaction)

        # 修复前：inner_transaction 会获取新连接并清空全局事务标志，导致 outer 异常时，无法回滚 inner 和 outer 之前的修改。
        # 修复后：内外层复用同一个事务连接，触发异常后应当全部回滚。
        outer_exists = clean_users.where('name', 'OuterTx').first()
        inner_exists = clean_users.where('name', 'InnerTx').first()

        assert not outer_exists, "外层事务回滚失败，数据被意外提交"
        assert not inner_exists, "嵌套事务破坏了原子性，内层事务被意外独立提交"

    @pytest.mark.fixes
    def test_global_update_delete_protection(self, clean_users):
        """修复验证 3：测试无 WHERE 条件的全表 Update / Delete 防护"""
        # 插入基准数据
        clean_users.create({'name': 'Protect1', 'email': 'p1@test.com', 'age': 20, 'status': 1, 'score': 80.0})

        # 测试 Update 拦截 (需要捕获 Exception)
        with pytest.raises(Exception, match="Update missing WHERE clause"):
            clean_users.update({'status': 0})

        # 测试 Delete 拦截 (需要捕获 Exception)
        with pytest.raises(Exception, match="Delete missing WHERE clause"):
            clean_users.delete()

    @pytest.mark.fixes
    def test_compile_select_state_pollution(self, clean_users):
        """修复验证 4：测试 _compile_select 污染实例状态的问题"""
        builder = clean_users.where('status', 1)

        # 记录原始的 select 状态（应当为空）
        original_select_len = len(builder.__select__)
        assert original_select_len == 0

        # 调用 tosql() 触发 _compile_select() 的执行
        sql = builder.tosql()
        assert 'select *' in sql.lower()

        # 验证 __select__ 列表没有被内部的 append('*') 污染
        assert len(builder.__select__) == 0, "调用 tosql() 后，__select__ 状态被意外写入了 '*'"
