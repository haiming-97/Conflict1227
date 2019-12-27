#!/usr/bin/python
#coding=utf-8
import logging
import os.path
import time
__author__="yanmeng 20191020"

class Logger:

    #def __init__(self, name='root', file=f'/Users/yanmeng/PycharmProjects/conflict/conflict.log'):
    def __init__(self, name='root', file='C:/Users/石海明/Desktop/conflict-master (1)/conflict.log'):
        self._logger = logging.getLogger(name)

        # set log level and formtter
        self.level = logging.DEBUG
        self.fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(filename)s(line:%(lineno)d) - %(message)s', '%Y-%m-%d %H:%M:%S')

        # file.log only for debug
        file_handler = logging.FileHandler(filename=file, encoding='utf-8', mode='a')
        file_handler.setFormatter(self.fmt)
        file_handler.setLevel(logging.DEBUG)

        # console.log for info
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.fmt)
        stream_handler.setLevel(logging.INFO)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(self.level)

    def getLogger(self):
        return self._logger
