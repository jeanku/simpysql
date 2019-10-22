#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Util.Expression import expression as expr
from ..Util.Response import Response
from .BaseBuilder import BaseBuilder
from simpysql.Util.Dynamic import Dynamic
import pymongo
import re

class MongoBuilder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'in', 'not in', 'not between', 'exist',
        'not like', 'ilike', 'not ilike', 'between', 'mod', 'all', 'size'
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
        'ilike': '$regex',
        'not like': '$regex',
        'not ilike': '$regex',
        'exist': '$exists',
        'mod': '$mod',
        'all': '$all',
        'size': '$size',
    }

    def __init__(self, model, alias=None):
        self.__model__ = model
        self.__alias__ = alias
        self.__where__ = {}
        self.__select__ = {}  # 检索的字段
        self.__limit__ = 0  # 检索的数据条数
        self.__orderby__ = []  # 排序字段
        self.__groupby__ = []  # 排序字段
        self.__offset__ = 0  # offset
        self.__lock__ = None  # lock
        self.__join__ = []  # leftjoin
        self.__union__ = []  # union & unionall
        self.__on__ = []  # leftjoin
        self.__having__ = None  # having
        self.__subquery__ = None  # subquery
        self.__groupbykey__ = None  # mongo groupby 字段名

    def first(self):
        self.__limit__ = 1
        data = self.get()
        if data:
            return data.pop()
        return data

    def get(self):
        return [Dynamic(index) for index in self._get_connection().get(self)]

    def lists(self, columns):
        return Response(self._get_connection().get(self)).tolist(columns)

    def pluck(self, key, value):
        return Response(self._get_connection().get(self)).pluck(key, value)

    def data(self):
        return Response(self._get_connection().get(self)).data()

    def response(self):
        return Response(self._get_connection().get(self))

    def count(self):
        return self._get_connection().count(self)

    def update(self, data, **kwargs):
        if data and isinstance(data, dict):
            data = self._set_update_time(data)
            return self._get_connection().update(self, {'$set': data}, **kwargs)
        return None

    def replace(self, data, **kwargs):
        if self.first():
            self.update(data, **kwargs)
        else:
            self.create(data)

    def create(self, data):
        if data:
            if isinstance(data, dict):
                data = [data]
            data = self._set_create_time(data)
            return self._get_connection().create(self, data)
        return None

    def delete(self):
        return self._get_connection().delete(self)

    def take(self, number):
        if number <= 0:
            raise Exception('take number invalid')
        self.__limit__ = int(number)
        return self

    def select(self, *args):
        self.__select__.update({'_id': 0})
        [self.__select__.update({index: 1}) for index in args]
        return self

    def groupby(self, groupkey):
        groupby = {
            "$group": {}
        }
        if self.__select__.__len__() == 0:
            raise Exception('invalid select filed')
        for key, value in self.__select__.items():
            if value == 1:
                groupby['$group'].update(self.format_group_sql(key))
        self.__select__ = {}
        self.__groupby__ = groupby
        self.__groupbykey__ = groupkey
        return self

    def where_to_match(self):
        return {'$match': self.__where__}

    def _format_column(self, column):
        return '$' + column

    def format_group_sql(self, sqlstr):
        p=r'([\w\.-_]*)(?:\(([a-zA-Z0-9.*]*)\))?(?:\s+as\s+(\w*))?'
        temp = re.match(p, sqlstr).groups()
        if temp[1] is None:
            return {'_id': self._format_column(temp[0])}
        if temp[0] == 'count':
            return {temp[0] if temp[2] is None else temp[2]: {self._format_column('sum'): 1}}
        else:
            return {temp[0] if temp[2] is None else temp[2]: {self._format_column(temp[0]): self._format_column(temp[1])}}

    def offset(self, number):
        if number < 0:
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
                    self.__where__['$and'].append(self._compile_tuple((args[0], args[1], args[2])))
            else:
                raise Exception('operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def whereor(self, *args):
        if self.__where__.get('$or', None) is None:
            self.__where__['$or'] = []
        length = args.__len__()
        if length == 1:
            if isinstance(args[0], list):
                for index in args[0]:
                    self.__where__['$or'].append(self._compile(index))
            elif isinstance(args[0], dict):
                self.__where__['$or'].append(self._compile(args[0]))
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
                    return {data[0]: {self.operators_map[data[1]]: data[2]}}
        raise Exception('bad parameters')

    def _compile_tuple(self, data):
        if data[1] == 'not like':
            return {data[0]: {self.operators_map[data[1]]: '^((?!{}).)*$'.format(data[2])}}
        elif data[1] == 'ilike':
            return {data[0]: {self.operators_map[data[1]]: data[2], '$options': 'i'}}
        elif data[1] == 'not ilike':
            return {data[0]: {self.operators_map[data[1]]: '^((?!{}).)*$'.format(data[2]), '$options': 'i'}}
        elif data[1] == 'between':
            if len(data[2]) != 2:
                raise Exception('between param error')
            return {data[0]: {'$lte': data[2][1], '$gte': data[2][0]}}
        elif data[1] == 'not between':
            if len(data[2]) != 2:
                raise Exception('not between param error')
            return {'$or': [{data[0]: {'$gt': data[2][1]}}, {data[0]: {'$lt': data[2][0]}}]}
        else:
            return {data[0]: {self.operators_map[data[1]]: data[2]}}

    def _compile_aggregate_orderby(self):
        temp = {}
        for index in self.__orderby__:
            temp[index[0]] = index[1]
        return {'$sort': temp}

    def _compile_aggregate_offset(self):
        return {'$skip': self.__offset__}

    def _compile_aggregate_limit(self):
        return {'$limit': self.__limit__}

    def _compile_aggregate_project(self):
        temp = dict(zip(self.__groupby__['$group'].keys(), [1, 1, 1]))
        temp['_id'] = 0
        temp[self.__groupbykey__] = self._format_column('_id')
        return {'$project': temp}

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
