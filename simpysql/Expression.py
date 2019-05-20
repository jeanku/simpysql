#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Expression(object):

    def format_sql_column(self, key):
        if isinstance(key, str):
            return '`{}`'.format(key)
        return ''

    def format_str_with_quote(self, key):
        if isinstance(key, str):
            return "'{}'".format(key)
        return key

    def list_to_str(self, data, parentheses=True):
        returnStr = ''
        if data and isinstance(data, list):
            returnStr = data.__str__()[1: -1]
        return '({})'.format(returnStr) if parentheses else returnStr


expression = Expression()
