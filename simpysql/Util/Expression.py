#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Eloquent.BaseBuilder import BaseBuilder
import pymysql

class Expression(object):

    def __init__(self, name=None):
        self.__name = name

    def format_column(self, key, model=None):
        if model is not None and model.columns and key in model.columns:
            return '`{}`'.format(key)
        return key

    def format_column_for_cassandra(self, key, model=None):
        if model is not None and model.columns and key in model.columns:
            return '"{}"'.format(key)
        return key

    def format_string(self, key):
        if isinstance(key, Expression):
            return key.__name
        elif isinstance(key, str):
            if key == "NULL" or key == "null":
                return "{}".format(key)
            return "'{}'".format(pymysql.converters.escape_string(key))
        elif isinstance(key, BaseBuilder):
            return "({})".format(key.tosql())
        return key

    def list_to_str(self, data):
        if data and isinstance(data, list):
            return tuple(data).__str__().replace(",)", ")") if len(data) == 1 else tuple(data).__str__()
        if data and isinstance(data, tuple):
            return data.__str__()
        elif isinstance(data, BaseBuilder):
            return "(" + data.tosql() + ")"
        else:
            raise Exception('param invalid')


expression = Expression()
