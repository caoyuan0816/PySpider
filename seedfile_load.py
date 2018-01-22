#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Read seedfile.

Seedfile will save urls line by line.
"""

import os
import logging
import urllib.parse

import define

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)


@define.singleton
class Seed:
    """
    Class Seed
    Load and store seed data.
    """
    def __init__(self):
        """
        Construct method of class Seed.
        """
        self.logger = logging.getLogger("spider")

    def readSeed(self, filepath):
        """
        Load sedd data from filepath.
        """
        self.logger.info("....Reading seed from {}".format(
            filepath
        ))
        self.value = []
        try:
            with open(filepath, 'rb') as seedFile:
                self.value = seedFile.read().decode('utf-8').split('\n')[:-1]
        except FileNotFoundError:
            raise define.SpiderError("ERROR - Seed file not exist.")
        except UnicodeDecodeError:
            raise define.SpiderError("ERROR - Seed file not encode by utf-8.")
        self.__checkValue()
        self.logger.info("....Read seed file finished, value is: {}".format(
            self.value
        ))

    def __checkValue(self):
        """
        Check seed value.
        """
        for it in self.value:
            parse = list(urllib.parse.urlsplit(it))
            if parse[0] == '' or parse[1] == '':
                raise define.SpiderError("ERROR - URL format wrong. Example: http://www.baidu.com")
