#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseBuilder import BaseBuilder

class Expression(object):

    def format_sql_column(self, key):
        list_str = key.split('.', 1)
        return '.'.join(["`{}`".format(i) if i == list_str[-1] else i for i in list_str])

    def format_str_with_quote(self, key):
        if isinstance(key, str):
            return "'{}'".format(key)
        elif isinstance(key, BaseBuilder):
           return "({})".format(key.tosql())
        return key

    def list_to_str(self, data, parentheses=True):
        returnStr = ''
        if data and isinstance(data, list):
            returnStr = data.__str__()[1: -1]
        elif isinstance(data, BaseBuilder):
            returnStr = data.tosql()
        return '({})'.format(returnStr) if parentheses else returnStr


expression = Expression()
