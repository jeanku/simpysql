#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Util.Expression import expression as expr
from ..Util.Response import Response
from .BaseBuilder import BaseBuilder
import pymongo


class MongoBuilder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'in', 'not in', 'not between', 'exist'
    ]
    operators_map = {
        '<': '$lt',
        '<=': '$lte',
        '>': '$gt',
        '>=': '$gte',
        '!=': '$ne',
        'in': '$in',
        'not in': '$nin',
        'like': '$regex',
        'exist': '$exist',
    }

    def __init__(self, model, alias=None):
        self.__model__ = model
        self.__alias__ = alias
        self.__where__ = {}
        self.__select__ = {}  # 检索的字段
        self.__limit__ = 0  # 检索的数据条数
        self.__orderby__ = []  # 排序字段
        self.__groupby__ = []  # 排序字段
        self.__offset__ = None  # offset
        self.__lock__ = None  # lock
        self.__join__ = []  # leftjoin
        self.__union__ = []  # union & unionall
        self.__on__ = []  # leftjoin
        self.__having__ = None  # having
        self.__subquery__ = None  # subquery

    def first(self):
        data = self.get()
        if data:
            return data.pop()
        return data

    def get(self):
        return self._get_connection().get(self)

    def lists(self, columns):
        return Response(self.get()).tolist(columns)

    def data(self):
        return Response(self.get()).data()

    def response(self):
        return Response(self.get())

    def count(self):
        return self._get_connection().count(self)

    def update(self, data):
        if data and isinstance(data, dict):
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_update(data))

    def create(self, data):
        if data:
            if data and isinstance(data, dict):
                data = [data]
            data = self._set_create_time(data)
            self._get_connection().execute(self._compile_create(data))
        return self

    def delete(self):
        return self._get_connection().execute(self._compile_delete())

    def take(self, number):
        if number <= 0:
            raise Exception('take number invalid')
        self.__limit__ = int(number)
        return self

    def select(self, *args):
        self.__select__.update({'_id': 0})
        [self.__select__.update({index: 1}) for index in args]
        return self

    def groupby(self, *args):
        self.__groupby__ = self._format_columns(list(args))
        return self

    def offset(self, number):
        if number <= 0:
            raise Exception('offset number invalid')
        self.__offset__ = int(number)
        return self

    def where(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict):
            self.__where__.update(args[0])
        elif length == 2:
            if self.__where__.get('$and', None) is None:
                self.__where__['$and'] = []
            self.__where__['$and'].append({args[0]: args[1]})
        elif length == 3:
            if self.__where__.get('$and', None) is None:
                self.__where__['$and'] = []
            if args[1] in self.operators:
                if args[1] == '=':
                    self.__where__['$and'].append({args[0]: args[2]})
                else:
                    self.__where__['$and'].append({args[0]: {self.operators_map[args[1]]: args[2]}})
            else:
                raise Exception('operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def whereor(self, *args):
        if self.__where__.get('$or', None) is None:
            self.__where__['$or'] = []
        length = args.__len__()
        if length == 1 and isinstance(args[0], list):
            for index in args[0]:
                self.__where__['$or'].append(self._compile(index))
        else:
            self.__where__['$or'].append(self._compile(args))
        return self

    def orderby(self, column, direction='asc'):
        if direction.lower() == 'asc':
            self.__orderby__.append((column, pymongo.ASCENDING))
        else:
            self.__orderby__.append((column, pymongo.DESCENDING))
        return self

    def sort(self, column, direction='asc'):
        return self.orderby(column, direction)

    def execute(self, sql):
        return self._get_connection().execute(sql)

    def _compile(self, data):
        length = data.__len__()
        if isinstance(data, dict):
            return data
        if length == 2:
            return {data[0]: data[1]}
        if length == 3:
            if data[1] in self.operators:
                if data[1] == '=':
                    return {data[0]: data[2]}
                else:
                    return {{data[0]: {self.operators_map[data[1]]: data[2]}}}
        raise Exception('bad parameters')

    def _compile_select(self):
        subsql = ''.join(
            [self._compile_where(), self._compile_orwhere(), self._compile_groupby(), self._compile_orderby(),
             self._compile_having(),
             self._compile_limit(),
             self._compile_offset(), self._compile_lock()])
        joinsql = ''.join(self._compile_leftjoin())
        returnsql = "select {} from {}{}{}".format(','.join(self.__select__), self._tablename(), joinsql, subsql)
        if self.__union__:
            return '({})'.format(returnsql) + ' union ' + self._compile_union()
        return returnsql

    def _get_connection(self):
        return self.connect(self.__model__)

    def database(self, name):
        self.__model__.__database__ = name
        return self

    def _tablename(self):
        if self.__subquery__:
            index, value = self.__subquery__
            return '({}) as {}'.format(value.tosql(), index)
        if self.__alias__ is None:
            return self.__model__.__tablename__
        return self.__model__.__tablename__ + ' as {}'.format(self.__alias__)

    def _format_columns(self, columns):
        return list(map(lambda index: expr.format_column(index), columns))

    def _set_create_time(self, data):
        currtime = self.__model__.fresh_timestamp()
        update_column = self.__model__.update_time_column()
        create_column = self.__model__.create_time_column()
        for index in data:
            if create_column and create_column not in index:
                index[create_column] = currtime
            if update_column and update_column not in index:
                index[update_column] = currtime
        return data

    def _set_update_time(self, data):
        currtime = self.__model__.fresh_timestamp()
        update_column = self.__model__.update_time_column()
        if update_column and update_column not in data:
            data[update_column] = currtime
        return data
