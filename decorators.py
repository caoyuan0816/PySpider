#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Define decorators.
"""

def singleton(cls, *args, **kw):
    """
    Singleton decorator.
    """
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
