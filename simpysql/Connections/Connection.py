#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from simpysql.Util.Logger import logger


class Connection(object):

    def log(self, sql):
        if self._logger:
            self._logger.info('【sql】:{}'.format(sql))

    def set_database(self, database):
        self._database = database
