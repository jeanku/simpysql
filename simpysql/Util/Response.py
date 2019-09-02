#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas


class Response(object):

    def __init__(self, data):
        self.__data__ = pandas.DataFrame(data) if data else None

    def data(self):
        return self.__data__

    def tolist(self, columns):
        if self.__data__ is not None:
            return self.__data__[columns].values.tolist()
        return []

    def pluck(self, key, vallue):
        if self.__data__ is not None:
            return dict(self.__data__[[key, vallue]].values)
        return {}
