#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect

from .Eloquent.BuilderFactory import builderfactory
from .Util.MagicMetaClass import MagicMetaClass
import time


class DBModel(MagicMetaClass):
    __create_time__ = None  # 插入时间字段

    __update_time__ = None  # 更新时间字段

    # 获取创建时间字段
    def create_time_column(self):
        return self.__create_time__

    # 获取更新时间字段
    def update_time_column(self):
        return self.__update_time__

    # 获取当前时间戳
    def fresh_timestamp(self):
        return int(time.time())

    @classmethod
    def transaction(cls, callback=None):
        builder = cls.__new__(cls)

        # 兼容写法：如果用户写了 @ModelDemo.transaction() 带括号
        if callback is None:
            return builder.transaction_wrapper

        # 智能探测：如果函数带有参数，那绝对是作为装饰器使用的
        sig = inspect.signature(callback)
        if len(sig.parameters) > 0:
            return builder.transaction_wrapper(callback)

        # 默认情况：如果是无参函数，走传统的立即执行 (方法 1)
        return builder.transaction(callback)

    def __new__(cls, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], str):
            return builderfactory.make(super(DBModel, cls).__new__(cls), alias=args[0])
        return builderfactory.make(super(DBModel, cls).__new__(cls))