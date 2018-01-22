#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Define exceptions.
"""

import logging

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
