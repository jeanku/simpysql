#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""环境变量类"""

__author__ = ''
import decimal

class Dynamic(dict):
    def __init__(self, d=None):
        if d is not None:
            for k, v in d.items():
                self[k] = str(v) if isinstance(v, decimal.Decimal) else v
        return super().__init__()

    def __key(self, key):
        return "" if key is None else key.lower()

    # def __str__(self):
    #     import json
    #     return json.dumps(self)

    def __setattr__(self, key, value):
        self[self.__key(key)] = value

    def __getattr__(self, key):
        return self.get(self.__key(key))

    def __getitem__(self, key):
        return super().get(self.__key(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.__key(key), value)
