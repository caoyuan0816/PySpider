#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Log setting.
"""

import os
import logging

import define

def setLogger(loggername, level, formaterStr, dirpath):
    """
    Set loger, using logging lib.
    """
    if not os.path.isdir(dirpath):
        try:
            os.makedirs(dirpath)
        except:
            raise define.SpiderError("ERROR - can not create log dir.")

    try:
        loggerHandler = logging.FileHandler(dirpath + '/' + loggername + '.log')
    except:
        raise define.SpiderError("ERROR - can not create log file.")

    loggerHandler.setFormatter(logging.Formatter(formaterStr))
    logger = logging.getLogger(loggername)
    logger.setLevel(level)
    logger.addHandler(loggerHandler)
