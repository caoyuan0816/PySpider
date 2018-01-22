#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Defines.
"""
import logging

class QueueElement:
    """
    Class QueueElement.
    Store element data.
    """
    def __init__(self, URL, level):
        """
        Construct method.
        """
        self.URL = URL
        self.level = level


def singleton(cls, *args, **kw):
    """
    Singleton decorator(class decorator).
    """
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class SpiderError(Exception):
    """
    Exception SpiderError.
    """
    def __init__(self, value):
        """
        Init
        """
        self.value = value
        self.logger = logging.getLogger("spider")
        self.logException()

    def __str__(self):
        """
        __str__ method
        """
        return self.value

    def logException(self):
        """
        Log exception to logger.
        """
        self.logger.error("Spider Exception, value = {}".format(
            self.value
        ))
