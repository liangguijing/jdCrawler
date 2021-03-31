# -*- coding: utf-8 -*-
"""
@Time: 3/29/2021 17:55
@Name: config.py
@Author: https://github.com/liangguijing
@Description: 
"""

import os
import configparser


class Config:
    def __init__(self, config_filename="config.ini"):
        self._path = os.path.join(os.getcwd(), config_filename)
        if not os.path.exists(self._path):
            raise FileNotFoundError("Missing config file: %s" % self._path)
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding="utf-8")

    def get(self, section, name, strip_blank=True, strip_quote=True):
        s = self._config.get(section, name)
        if strip_blank:
            s = s.strip()
        if strip_quote:
            s = s.strip('"').strip("'")
        return s

    def getboolean(self, section, name):
        return self._config.getboolean(section, name)


config = Config()
