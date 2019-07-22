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
