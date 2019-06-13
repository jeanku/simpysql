#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
from simpysql.Util.Expression import expression as expr, Expression
from simpysql.Util.Response import Response
from .BaseBuilder import BaseBuilder
from simpysql.Util.Dynamic import Dynamic


class SqlServerBuilder(BaseBuilder):
    operators = [
        '=', '<', '>', '<=', '>=', '<>', '!=',
        'like', 'like binary', 'not like', 'between', 'ilike',
        '&', '|', '^', '<<', '>>',
        'rlike', 'regexp', 'not regexp',
        '~', '~*', '!~', '!~*', 'similar to',
        'not similar to', 'not ilike', '~~*', '!~~*', 'in', 'not in', 'not between'
    ]

    def __init__(self, model, alias=None):
        self.__model__ = model
        self.__alias__ = alias
        self.__where__ = []
        self.__orwhere__ = []                           # orwhere处理逻辑
        self.__whereor__ = []                           # orwhere处理逻辑
        self.__select__ = []                            # 检索的字段
        self.__limit__ = 0                              # 检索的数据条数
        self.__orderby__ = []                           # 排序字段
        self.__groupby__ = []                           # 排序字段
        self.__offset__ = None                          # offset
        self.__lock__ = None                            # lock
        self.__join__ = []                              # leftjoin
        self.__union__ = []                             # union & unionall
        self.__on__ = []                                # leftjoin
        self.__having__ = None                          # having
        self.__subquery__ = []                          # subquery

    def first(self):
        self.__limit__ = 1
        data = self.get()
        if data:
            return data.pop()
        return data

    def one(self):
        data = self.get()
        if data:
            return data.pop()
        return data

    def get(self):
        return [Dynamic(index) for index in self._get_connection().execute(self._compile_select())]

    def lists(self, columns):
        return Response(self._get_connection().execute(self._compile_select())).tolist(columns)

    def data(self):
        return Response(self._get_connection().execute(self._compile_select())).data()

    def response(self):
        return Response(self._get_connection().execute(self._compile_select()))

    def max(self, column):
        if isinstance(column, str) and column in self.__model__.columns:
            self.__select__ = ['max({}) as aggregate'.format(column)]
            data = self.one()
            return data['aggregate'] if data else None
        raise Exception('param invalid in function max')

    def min(self, column):
        if isinstance(column, str) and column in self.__model__.columns:
            self.__select__ = ['min({}) as aggregate'.format(column)]
            data = self.one()
            return data['aggregate'] if data else None
        raise Exception('param invalid in function min')

    def avg(self, column):
        if isinstance(column, str) and column in self.__model__.columns:
            self.__select__ = ['avg({}) as aggregate'.format(column)]
            data = self.one()
            return data['aggregate'] if data else None
        raise Exception('param invalid in function avg')

    def sum(self, column):
        if isinstance(column, str) and column in self.__model__.columns:
            self.__select__ = ['sum({}) as aggregate'.format(column)]
            data = self.one()
            return data['aggregate'] if data else None
        raise Exception('param invalid in function sum')

    def count(self):
        self.__select__ = ['count(*) as aggregate']
        data = self.one()
        return data['aggregate'] if data else None

    def exist(self):
        return True if self.count() > 0 else False

    def update(self, data):
        if data and isinstance(data, dict):
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_update(data))

    def increment(self, key, amount=1):
        if isinstance(amount, int) and amount > 0:
            data = collections.defaultdict(dict)
            data[key] = '{}+{}'.format(expr.format_column(key), str(amount))
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_increment(data))

    def decrement(self, key, amount=1):
        if isinstance(amount, int) and amount > 0:
            data = collections.defaultdict(dict)
            data[key] = '{}-{}'.format(expr.format_column(key), str(amount))
            data = self._set_update_time(data)
            return self._get_connection().execute(self._compile_increment(data))

    def create(self, data):
        if data:
            if data and isinstance(data, dict):
                data = [data]
            data = self._set_create_time(data)
            self._get_connection().execute(self._compile_create(data))
        return self

    def insert(self, columns, data):
        self._get_connection().execute(self._compile_insert(columns, data))
        return self

    def lastid(self):
        data = self._get_connection().execute(self._compile_lastid())
        return data[0][0] if data and data[0] and data[0][0] else None

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
        return self._compile_select()

    def where(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict):
            self.__where__.append(args[0])
        elif length == 2:
            self.__where__.append({args[0]: self._check_columns_value(args[1])})
        elif length == 3:
            if args[1] in self.operators:
                if args[1] == '=':
                    self.__where__.append({args[0]: self._check_columns_value(args[2])})
                else:
                    self.__where__.append((args[0], args[1], self._check_columns_value(args[2])))
            else:
                raise Exception('operator key world not found: "{}"'.format(args[1]))
        else:
            raise Exception('bad parameters in where function')
        return self

    def orwhere(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], dict):
            self.__orwhere__.append(args[0])
        elif length == 1 and isinstance(args[0], list):
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

    def whereor(self, *args):
        length = args.__len__()
        if length == 1 and isinstance(args[0], list):
            self.__whereor__.append(args[0])
        else:
            raise Exception('bad parameters in where function')
        return self

    def orderby(self, column, direction='asc'):
        if direction.lower() == 'asc':
            self.__orderby__.append(expr.format_column(column))
        else:
            self.__orderby__.append(expr.format_column(column) + ' desc')
        return self

    def execute(self, sql):
        return self._get_connection().execute(sql)

    def having(self, *args):
        length = args.__len__()
        if length == 2:
            self.__having__ = ' having {} {} {}'.format(args[0], '=',  expr.format_string(args[1]))
        elif length == 3:
            self.__having__ = ' having {} {} {}'.format(args[0], args[1], expr.format_string(args[2]))
        else:
            raise Exception('invalid parameter in having function')
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

    def on(self, *args):
        length = args.__len__()
        if length == 2:
            self.__on__.append((args[0], '=', args[1]))
        elif length == 3:
            self.__on__.append((args[0], args[1], args[2]))
        else:
            raise Exception('invalid parameter in on function')
        return self

    def subquery(self, model, alias='tmp'):
        self.__subquery__.append((alias, model))
        return self

    def _compile_select(self):
        if len(self.__select__) == 0:
            self.__select__.append('*')
        subsql = ''.join(
            [self._compile_where(), self._compile_whereor(), self._compile_orwhere(), self._compile_groupby(), self._compile_orderby(),
             self._compile_having(), self._compile_offset(), self._compile_lock()])
        joinsql = ''.join(self._compile_leftjoin())
        returnsql = "select {}{} from {}{}{}".format(self._compile_limit(), ','.join(self.__select__), self._tablename(), joinsql, subsql)
        if self.__union__:
            return '{}'.format(returnsql) + self._compile_union()
        return returnsql

    def _compile_create(self, data):
        return "insert into {} {} values {}".format(self._tablename(), self._columnize(data[0]), self._valueize(data))

    def _compile_insert(self, columns, data):
        return "insert into {} {} values {}".format(self._tablename(), self._columnize(columns), ','.join([tuple(index).__str__() for index in data]))

    def _compile_update(self, data):
        return "update {} set {}{}".format(self._tablename(), ','.join(self._compile_dict(data)), self._compile_where())

    def _compile_increment(self, data):
        subsql = ','.join(['{}={}'.format(expr.format_column(index), value) for index, value in data.items()])
        return "update {} set {}{}".format(self._tablename(), subsql, self._compile_where())

    def _compile_delete(self):
        return 'delete from {}{}'.format(self._tablename(), self._compile_where())

    def _compile_lastid(self):
        return 'select last_insert_id() as lastid'

    def _columnize(self, columns):
        return tuple(columns).__str__().replace('\'', '`')

    def _valueize(self, data):
        return ','.join([tuple(index.values()).__str__() for index in data])

    def _compile_groupby(self):
        return '' if len(self.__groupby__) == 0 else ' group by ' + ','.join(self.__groupby__)

    def _compile_orderby(self):
        return '' if len(self.__orderby__) == 0 else ' order by ' + ','.join(self.__orderby__)

    def _compile_limit(self):
        return '' if self.__limit__ == 0 else 'top ({}) '.format(self.__limit__)

    def _compile_offset(self):
        if self.__offset__:
            if self.__orderby__:
                return '' if self.__offset__ is None else ' offset {} rows fetch next {} rows only'.format(self.__offset__, self.__limit__)
            raise Exception('orderby function not set exception')
        return ''

    def _compile_lock(self):
        return '' if self.__lock__ is None else self.__lock__

    def _compile_leftjoin(self):
        if self.__join__:
            return ' ' + ' '.join(['{} {} on {}'.format(index, value._tablename(), value._compile_on()) for (index, value) in
                 self.__join__])
        return ''

    def _compile_union(self):
        if self.__union__:
            return ' ' + ' '.join(['{} ({})'.format(index, value.tosql()) for (index, value) in self.__union__])
        return ''

    def _compile_on(self):
        sqlstr = ['{} {} {}'.format(index[0], index[1], index[2]) for index in self.__on__]
        return ' and '.join(sqlstr)

    def _compile_having(self):
        if self.__having__:
            return self.__having__
        return ''

    def _compile_where(self):
        if len(self.__where__) > 0:
            sqlstr = []
            for index in self.__where__:
                if isinstance(index, dict):
                    sqlstr.append(' and '.join(self._compile_dict(index)))
                elif isinstance(index, tuple):
                    sqlstr.append(self._compile_tuple(index))
            return ' where {}'.format(' and '.join(sqlstr))
        return ''

    def _compile_orwhere(self):
        if len(self.__orwhere__) > 0:
            sqlstr = []
            for index in self.__orwhere__:
                if isinstance(index, dict):
                    subsql = self._compile_dict(index)
                    if len(subsql) == 1:
                        sqlstr.append(subsql.pop())
                    else:
                        sqlstr.append('({})'.format(' and '.join(subsql)))
                elif isinstance(index, tuple):
                    sqlstr.append(self._compile_tuple(index))
                elif isinstance(index, list):
                    subsql = []
                    for items in index:
                        if len(items) == 2:
                            subsql.append(self._compile_keyvalue(items[0], items[1]))
                        if len(items) == 3:
                            subsql.append(self._compile_tuple((items[0], items[1], items[2])))
                    sqlstr.append('({})'.format(' and '.join(subsql)))
                else:
                    raise Exception('undefined query condition {}'.format(index.__str__()))
            if len(self.__where__) > 0:
                return ' or {}'.format(' or '.join(sqlstr))
            return ' where {}'.format(' or '.join(sqlstr))
        return ''

    def _compile_whereor(self):
        if len(self.__whereor__) > 0:
            sqlstr = []
            for index in self.__whereor__:
                subsql = []
                for item in index:
                    if isinstance(item, dict):
                        if len(item) == 1:
                            subsql.append(self._compile_dict(item).pop())
                        else:
                            subsql.append('(' + ' and '.join(self._compile_dict(item)) + ')')
                    elif isinstance(item, list):
                        if isinstance(item[0], str):
                            subsql.append(self._compile_tuple(tuple(item)))
                        else:
                            subsql.append(self._compile_lists(item))
                    elif isinstance(item, tuple):
                        subsql.append(self._compile_tuple(item))
                    else:
                        raise Exception('whereor param invalid')
                sqlstr.append(' or '.join(subsql))
            if len(self.__where__) > 0:
                return ' and ({})'.format(' or '.join(sqlstr))
            return ' where ({})'.format(' or '.join(sqlstr))
        return ''

    def _compile_dict(self, data):
        return ['{}={}'.format(expr.format_column(index), expr.format_string(value)) for index, value in data.items()]

    def _compile_tuple(self, data):
        if data[1] in ['in', 'not in']:
            return self._compile_in((data[0], data[1], data[2]))
        elif data[1] in ['between', 'not between']:
            return self._compile_between((data[0], data[1], data[2]))
        return '{} {} {}'.format(expr.format_column(data[0]), data[1], expr.format_string(data[2]))

    def _compile_in(self, data):
        return '{} {} {}'.format(expr.format_column(data[0]), data[1], expr.list_to_str(data[2]))

    def _compile_list(self, data):
        length = len(data)
        if length == 2:
            return self._compile_keyvalue(data[0], data[1])
        if length == 3:
            return self._compile_tuple((data[0], data[1], data[2]))

    def _compile_lists(self, data):
        return_data = []
        for index in data:
            if isinstance(index, list):
                return_data.append(self._compile_list(index))
            if isinstance(index, tuple):
                return_data.append(self._compile_tuple(index))
        return '(' + ' and '.join(return_data) + ')'

    def _compile_between(self, data):
        if not (len(data) == 3 and len(data[2]) == 2):
            raise Exception('between param invalid')
        return '{} {} {} and {}'.format(expr.format_column(data[0]), data[1], expr.format_string(data[2][0]),
                                                     expr.format_string(data[2][1]))

    def _compile_keyvalue(self, key, value):
        return '{}={}'.format(expr.format_column(key), expr.format_string(value))

    def _compile_subquery(self):
        subquery = []
        for index, value in self.__subquery__:
            if isinstance(value, str):
                subquery.append('{} as {}'.format(value, index))
            else:
                subquery.append('({}) as {}'.format(value.tosql(), index))
        return ','.join(subquery)

    def _get_connection(self):
        return self.connect(self.__model__)

    def _check_columns_value(self, value):
        if self.__subquery__ and len(self.__subquery__) >= 2 and isinstance(value, str):
            tmp = value.split('.')
            if len(tmp) == 2 and tmp[0] in self._get_subquery_alias():
                return Expression(value)
        return value

    def _get_subquery_alias(self):
        return [index for index, value in self.__subquery__]

    def database(self, name):
        self.__model__.__database__ = name
        return self

    def _tablename(self):
        if self.__subquery__:
            return self._compile_subquery()
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

    def transaction(self, callback):
        return self._get_connection().transaction(callback)

    def transaction_wrapper(self, callback):
        return self._get_connection().transaction_wrapper(callback)
