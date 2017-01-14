#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : WLOG
# @Author   : asd
# @Date     : 2017-01-05 22:18

import logging.config
import os
from logging.handlers import RotatingFileHandler

import time

rootpath = os.path.dirname(os.path.basename(__file__))

class Log(object):

    def __init__(self, **kwargs):
        self.format = kwargs['format'].replace("@", "%")
        self.level = kwargs['level'].upper()
        self.backpcount = int(kwargs['backupcount'])
        self.maxbytes = int(kwargs['maxbytes'])
        self.logpath = kwargs['logpath']

    # 标准输出
    def __logger(self, logname):
        return logging.getLogger(logname)

    # 写入日志
    def write_log(self, logname, message, directory=None, level=None):
        '''
        写入日志，可配置logger名,日志级别，日志目录
        :param logname:
        :param message:
        :param level:
        :param directory:
        :return:
        '''
        filename = time.strftime('%Y-%m-%d')
        # 判断是否需要创建目标文件夹
        if directory == None or directory == '':
            path = self.__create_directory(self.logpath)
        else:
            path = self.__create_directory(directory + '/')
        logger = self.__logger(logname)
        logpath = path + filename + '.log'
        Rthandler = RotatingFileHandler(logpath, maxBytes=self.maxbytes, backupCount=self.backpcount)
        Stream = logging.StreamHandler()
        logger.setLevel(self.level)
        formatter = logging.Formatter(self.format)
        Rthandler.setFormatter(formatter)
        logger.addHandler(Rthandler)
        logger.addHandler(Stream)
        if level == None or level == '':
            if self.level == 'WARNING':
                logger.warning(message)
            if self.level == 'ERROR':
                logger.error(message)
            if self.level == 'CRITICAL':
                logger.critical(message)
        else:
            if level == 'warning':
                logger.warning(message)
            if level == 'error':
                logger.error(message)
            if level == 'critical':
                logger.critical(message)
        logger.removeHandler(Rthandler)
        logger.removeHandler(Stream)

    def __create_directory(self, path):
        # 判断是否存在目录，若不存在，则创建
        if not os.path.exists(path):
            os.mkdir(path)
        # 返回路径
        return path + '/'

if __name__ == '__main__':
    config = {
        'format': '@(asctime)s - @(name)s - @(levelname)s - @(message)s',
        'backupcount': 5,
        'maxbytes': 104857600,
        'level': 'ERROR',
        'logpath': u'/vagrant_data/python_dev/logs'
    }
    Log = Log(**config)
    Log.write_log('asd', 'name_error_critical')
