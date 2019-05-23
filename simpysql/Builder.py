#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
from pymysql.cursors import SSCursor, DictCursor, SSDictCursor
from .Expression import expression
from .Response import Response
from .BaseBuilder import BaseBuilder

class Builder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'like binary', 'not like', 'between', 'ilike',
        '&', '|', '^', '<<', '>>',
        'rlike', 'regexp', 'not regexp',
        '~', '~*', '!~', '!~*', 'similar to',
        'not similar to', 'not ilike', '~~*', '!~~*', 'in', 'not in', 'not between'
    ];

    def __init__(self, model, alias=None):
        self.__model__ = model
        self.__alias__ = alias
        self.__where__ = collections.defaultdict(dict)
        self.__orwhere__ = []                       # orwhere处理逻辑
        self.__select__ = []                        # 检索的字段
        self.__limit__ = None                       # 检索的数据条数
        self.__orderby__ = []                       # 排序字段
        self.__groupby__ = []                       # 排序字段
        self.__offset__ = None                      # offset
        self.__lock__ = None                        # lock
        self.__join__ = []                          # leftjoin
        self.__union__ = []                         # union & unionall
        self.__on__ = []                            # leftjoin
        self.__having__ = None                      # having
        self.__subquery__ = None                    # subquery

    def first(self):
        self.__limit__ = 1
        data = self.get()
        if data:
            return data.pop()
        return data

    def get(self):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        return self._get_connection().execute(self._compile_select(), DictCursor)

    def lists(self, columns):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        return Response(self._get_connection().execute(self._compile_select(), DictCursor)).tolist(columns)

    def data(self):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        return Response(self._get_connection().execute(self._compile_select(), DictCursor)).data()

    def response(self):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        return Response(self._get_connection().execute(self._compile_select(), DictCursor))

    def update(self, data):
        if data and isinstance(data, dict):
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_update(data))

    def increment(self, key, amount='1'):
        if isinstance(amount, int) and amount > 0:
            data = collections.defaultdict(dict)
            data[key] = '{}+{}'.format(expression.format_sql_column(key), str(amount))
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_increment(data))

    def decrement(self, key, amount='1'):
        if isinstance(amount, int) and amount > 0:
            data = collections.defaultdict(dict)
            data[key] = '{}-{}'.format(expression.format_sql_column(key), str(amount))
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_increment(data))

    def create(self, data):
        if data:
            if data and isinstance(data, dict):
                data = [data]
            data = self._set_create_time(data)
            self._get_connection().execute(self._compile_create(data))
        return self

    def lastid(self):
        data = self._get_connection().execute(self._compile_lastid())
        if data and data[0] and data[0][0]:
            return data[0][0]
        return None

    def delete(self):
        return self._get_connection().execute(self._compile_delete())

    def take(self, number):
        if number <= 0:
            raise Exception('take number invalid')
        self.__limit__ = int(number)
        return self

    def select(self, *args):
        self.__select__ = self._format_columns(list(args))
        return self

    def groupby(self, *args):
        self.__groupby__ = self._format_columns(list(args))
        return self

    def offset(self, number):
        if number <= 0:
            raise Exception('offset number invalid')
        self.__offset__ = int(number)
        return self

    def tosql(self):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        return self._compile_select()

    def where(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict):
            self.__where__.update(args[0])
        elif length == 2:
            self.__where__.update({args[0]: args[1]})
        elif length == 3:
            if args[1] in self.operators:
                if args[1] == '=':
                    self.__where__.update({args[0]: args[2]})
                else:
                    self.__where__[args[1]].update({args[0]: args[2]})
            else:
                raise Exception('operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def orwhere(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict) or isinstance(args[0], list):
            self.__orwhere__.append(args[0])
        elif length == 2:
            self.__orwhere__.append({args[0]: args[1]})
        elif length == 3:
            if args[1] in self.operators:
                if args[1] == '=':
                    self.__orwhere__.append({args[0]: args[2]})
                else:
                    self.__orwhere__.append((args[0], args[1], args[2]))
            else:
                raise Exception('operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def orderby(self, column, direction='asc'):
        if direction.lower() == 'asc':
            self.__orderby__.append(expression.format_sql_column(column))
        else:
            self.__orderby__.append(expression.format_sql_column(column) + ' desc')
        return self

    def execute(self, sql):
        return self._get_connection().execute(sql)

    def having(self, column1, operator, column2):
        self.__having__ = ' having {} {} {}'.format(column1, operator, column2)
        return self

    def lock_for_update(self):
        self.__lock__ = ' for update'
        return self

    def lock_for_share(self):
        self.__lock__ = ' lock in share mode'
        return self

    def leftjoin(self, model):
        if not (isinstance(model, BaseBuilder)):
            raise TypeError('invalid parameter type in leftjoin')
        self.__join__.append(('left join', model))
        return self

    def rightjoin(self, model):
        if not (isinstance(model, BaseBuilder)):
            raise TypeError('invalid parameter type in rightjoin')
        self.__join__.append(('right join', model))
        return self

    def join(self, model):
        return self.innerjoin(model)

    def innerjoin(self, model):
        if not (isinstance(model, BaseBuilder)):
            raise TypeError('invalid parameter type in innerjoin')
        self.__join__.append(('inner join', model))
        return self

    def union(self, model):
        if not (isinstance(model, BaseBuilder)):
            raise TypeError('invalid parameter type in union')
        self.__union__.append(('union', model))
        return self

    def unionall(self, model):
        if not (isinstance(model, BaseBuilder)):
            raise TypeError('invalid parameter type in unionall')
        self.__union__.append(('union all', model))
        return self

    def on(self, column1, operator, column2):
        self.__on__.append((column1, operator, column2))
        return self

    def subquery(self, model: BaseBuilder, alias='tmp'):
        if not (isinstance(model, BaseBuilder) and isinstance(alias, str)):
            raise TypeError('invalid parameter type in subquery')
        self.__subquery__ = (alias, model)
        return self

    def _compile_select(self):
        subsql = ''.join(
            [self._compile_where(), self._compile_orwhere(), self._compile_groupby(), self._compile_orderby(), self._compile_limit(),
             self._compile_offset(), self._compile_lock(), self._compile_having(),])
        joinsql = ''.join(self._compile_leftjoin())
        returnsql = "select {} from {}{}{}".format(','.join(self.__select__), self._tablename(), joinsql, subsql)
        if self.__union__:
            return '({})'.format(returnsql) + ' union ' + self._compile_union()
        return returnsql

    def _compile_create(self, data):
        if isinstance(data, dict):
            data = [data]
        return "insert into {} {} values {}".format(self._tablename(), self._columnize(data[0]), self._valueize(data))

    def _compile_insert(self, columns, data):
        return "insert into {} {} values {}".format(self._tablename(), self._columnize(columns),
                                                    ','.join([tuple(index).__str__() for index in data]))

    def _compile_update(self, data):
        return "update {} set {}{}".format(self._tablename(), self._keyvalueize(data), self._compile_where())

    def _compile_increment(self, data):
        subsql = ','.join(['{}={}'.format(expression.format_sql_column(index), value) for index, value in data.items()])
        return "update {} set {}{}".format(self._tablename(), subsql, self._compile_where())

    def _compile_delete(self):
        return 'delete from {}{}'.format(self._tablename(), self._compile_where())

    def _compile_lastid(self):
        return 'select last_insert_id() as lastid'

    def _columnize(self, columns):
        return tuple(columns).__str__().replace('\'', '`')

    def _valueize(self, data):
        return ','.join([tuple(index.values()).__str__() for index in data])

    def _keyvalueize(self, data):
        return ','.join(
            ['{}={}'.format(expression.format_sql_column(index), expression.format_str_with_quote(value)) for
             index, value in data.items()])

    def _compile_groupby(self):
        return '' if len(self.__groupby__) == 0 else ' group by ' + ','.join(self.__groupby__)

    def _compile_orderby(self):
        return '' if len(self.__orderby__) == 0 else ' order by ' + ','.join(self.__orderby__)

    def _compile_limit(self):
        return '' if self.__limit__ is None else ' limit {}'.format(self.__limit__)

    def _compile_offset(self):
        return '' if self.__offset__ is None else ' offset {}'.format(self.__offset__)

    def _compile_lock(self):
        return '' if self.__lock__ is None else self.__lock__

    def _compile_leftjoin(self):
        if self.__join__:
            return ' ' + ' '.join(['{} {} on {}'.format(index, value._tablename(), value._compile_on()) for (index, value) in self.__join__])
        return ''

    def _compile_union(self):
        if self.__union__:
            return ' ' + ' '.join(['{} ({})'.format(index, value.tosql()) for (index, value) in self.__union__])
        return ''

    def _compile_on(self):
        sqlstr = ['{} {} {}'.format(index[0], index[1],index[2]) for index in self.__on__]
        return ' and '.join(sqlstr)

    def _compile_having(self):
        if self.__having__:
            return self.__having__
        return ''
    def _compile_where(self):
        if len(self.__where__) > 0:
            sqlstr = []
            for index, values in self.__where__.items():
                if index in self.operators:
                    if index in ['in', 'not in'] and isinstance(values, dict):
                        for key, value in values.items():
                            sqlstr.append('{} {} {}'.format(expression.format_sql_column(key), index, expression.list_to_str(value)))
                    elif index in ['between', 'not between'] and isinstance(values, dict):
                        for key, value in values.items():
                            if isinstance(value, list) and len(value) == 2:
                                sqlstr.append('{} {} {} and {}'.
                                              format(expression.format_sql_column(key), index,
                                                     expression.format_str_with_quote(value[0]),
                                                     expression.format_str_with_quote(value[1])))
                    else:
                        for key, value in values.items():
                            sqlstr.append('{} {} {}'.format(expression.format_sql_column(key), index,
                                                            expression.format_str_with_quote(value)))
                else:
                    sqlstr.append(
                        '{}={}'.format(expression.format_sql_column(index), expression.format_str_with_quote(values)))
            return ' where {}'.format(' and '.join(sqlstr))
        return ''

    def _compile_orwhere(self):
        if len(self.__orwhere__) > 0:
            sqlstr = []
            for index in self.__orwhere__:
                if isinstance(index, dict):
                    subsql = []
                    for index, value in index.items():
                        subsql.append('{}={}'.format(expression.format_sql_column(index), expression.format_str_with_quote(value)))
                    sqlstr.append(' and '.join(subsql))
                elif isinstance(index, tuple):
                    sqlstr.append('{} {} {}'.format(expression.format_sql_column(index[0]), index[1], expression.format_str_with_quote(index[2])))
                elif isinstance(index, list):
                    subsql = []
                    for items in index:
                        if len(items) == 2:
                            subsql.append('{}={}'.format(expression.format_sql_column(items[0]), expression.format_str_with_quote(items[1])))
                        if len(items) == 3:
                            subsql.append('{} {} {}'.format(expression.format_sql_column(items[0]), items[1], expression.format_str_with_quote(items[2])))
                    sqlstr.append('({})'.format(' and '.join(subsql)))
                else:
                    raise Exception('undefined query condition {}'.format(index.__str__()))
            if len(self.__where__) > 0:
                return ' or {}'.format(' or '.join(sqlstr))
            return ' where {}'.format(' or '.join(sqlstr))
        return ''

    def _get_connection(self):
        return self.__model__.__connection__

    def database(self, name):
        self._get_connection().set_database(name)
        return self

    def _tablename(self):
        if self.__subquery__:
            index, value = self.__subquery__
            return '({}) as {}'.format(value.tosql(), index)
        if self.__alias__ is None:
            return self.__model__.__tablename__
        return self.__model__.__tablename__ + ' as {}'.format(self.__alias__)


    def _format_columns(self, columns):
        return list(map(lambda index: expression.format_sql_column(index), columns))

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

    def transaction(self, callback):
        return self._get_connection().transaction(callback)

    def transaction_wrapper(self, callback):
        return self._get_connection().transaction_wrapper(callback)