#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas


class Response(object):

    def __init__(self, data=None):
        self.__data__ = data

    def data(self):
        return pandas.DataFrame(self.__data__)

    def tolist(self, columns):
        if self.__data__ is not None:
            if type(columns) == str:
                return [index[columns] for index in self.__data__]
            elif type(columns) == list:
                return [self._muti_select(index, columns) for index in self.__data__]
        return []

    def pluck(self, key, value):
        if self.__data__ is not None:
            return {index[key]: index[value] for index in self.__data__}
        return {}

    def _muti_select(self, dict, columns):
        item = []
        for index in columns:
            item.append(dict[index])
        return item

