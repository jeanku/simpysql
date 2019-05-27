#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Log日志类"""

__author__ = ''

import logging
import datetime


class Logger(object):
    _instance = None

    _logger = None

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
        if self._logger is None:
            self._logger = logging.getLogger("logging")
            self._logger.setLevel("INFO")
            formatter = logging.Formatter('%(asctime)s 【%(levelname)s】%(message)s')
            fh = logging.FileHandler(self._path + "{}.log".format(datetime.datetime.now().strftime("%Y%m%d")))
            ch = logging.StreamHandler()
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self._logger.addHandler(fh)
            self._logger.addHandler(ch)
        return self._logger


logger = Logger()
