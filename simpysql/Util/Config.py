#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""环境变量类"""

__author__ = ''

from configparser import ConfigParser
import os


class MyConfigParser(ConfigParser):
    """解决ConfigParser会将key名转成小写的问题"""

    def optionxform(self, str):
        return str


class Config(object):
    """Env主要是为了获取.env中的配置数据"""

    _base_path = None

    _instance = None

    _config = {}

    _parser = None

    # 单例模式
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __call__(self, name, defaule=''):
        return self._config.get(name, defaule)

    def __getattr__(self, name):
        return self._config.get(name)

    def items(self, key):
        if self._config.get(key, None) is None:
            filepath = self._base_path + '.env'
            if not (os.path.isfile(filepath) and os.access(filepath, os.R_OK)):
                raise Exception('.env file not access exception')
            self.get_parser().read(filepath)
            try:
                self._config[key] = dict(self.get_parser().items(key))
            except Exception:
                raise Exception('{} not find in .env file'.format(key))
        return self._config[key]

    def get_parser(self):
        if self._parser is None:
            self._parser = MyConfigParser()
        return self._parser

    def set_basepath(self, path):
        if self._base_path is None:
            self._base_path = path
        return self


config = Config()
