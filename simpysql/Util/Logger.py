#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Log日志类"""

__author__ = ''

import logging
import datetime


class Logger(object):
    _instance = None

    _logger = {}

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kw)
        return cls._instance

    def info(self, msg):
        self.get_logger().info(msg)

    def set_path(self, path):
        self._path = path
        return self

    def get_logger(self):
        date = datetime.datetime.now().strftime("%Y%m%d")
        if self._logger.get(date) is None:
            self._logger = {}
            logger = logging.getLogger(date)
            logger.setLevel("INFO")
            formatter = logging.Formatter('%(asctime)s 【%(levelname)s】%(message)s')
            fh = logging.FileHandler(self._path + "{}.log".format(datetime.datetime.now().strftime("%Y%m%d")))
            ch = logging.StreamHandler()
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            logger.addHandler(fh)
            logger.addHandler(ch)
            self._logger[date] = logger
        return self._logger.get(date)


logger = Logger()
