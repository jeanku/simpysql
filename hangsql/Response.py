#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas

class Response(object):

    def __init__(self, data):
        self.__data__ = pandas.DataFrame(data)

    def data(self):
        return self.__data__

    def tolist(self, columns):
        return self.__data__[columns].values
