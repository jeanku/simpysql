#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Eloquent.BaseBuilder import BaseBuilder
import pymysql

class Expression(object):

    def format_sql_column(self, key):
        return key

    def format_str_with_quote(self, key):
        if isinstance(key, str):
            return "'{}'".format(pymysql.escape_string(key))
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
