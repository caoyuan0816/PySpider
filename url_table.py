#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Python mini spider

A mini multithread spider.
"""

import os
import logging
import threading

import define
import seedfile_load

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

@define.singleton
class Table:
    """
    Class Table.
    To store and unique URL data.
    """
    LOCK = threading.Lock()
    def __init__(self):
        """
        Construct method.
        """
        self.value = set()

    def uniqueAndSave(self, linksList):
        """
        Unique data, and save it into store.
        Multithread safe.
        Will return unique link list.
        """

        with self.LOCK:
            linksListSet = set(linksList)
            uniqueSet = linksListSet - self.value
            self.value = self.value | linksListSet

        return list(uniqueSet)
