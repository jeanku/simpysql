#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""metaclass静态方法调用处理类"""

__author__ = ''


class BaseMagicMetaClass(type):
    def __getattr__(self, key):
        if key == "__new__":
            return object.__new__(self)
        try:
            return object.__getattribute__(self, key)
        except:
            return getattr(self.__new__(self), key)


class MagicMetaClass(metaclass=BaseMagicMetaClass):
    pass
