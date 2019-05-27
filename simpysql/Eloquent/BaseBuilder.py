#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..Connections.ConnectionFactory import connfactory


class BaseBuilder(object):

    def connect(self, model):
        return connfactory.make(self.connection_name(model), model.__basepath__)

    def new_connect(self, model, database):
        return connfactory.make(database, model.__basepath__)

    def connection_name(self, model):
        return model.__database__ if hasattr(model, '__database__') and model.__database__ is not None else 'default'
