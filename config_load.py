#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Config load module of python mini spider.

Load config from provided file.
"""

import os
import configparser
import re
import logging

import define

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

@define.singleton
class Config:
    """
    Class Config.

    Use to load and store config.
    """

    def __init__(self):
        """
        Construct method of class Config.
        """
        self.logger = logging.getLogger("spider")

    def readConfig(self, filepath):
        """
        Read config from config file.
        """
        self.logger.info("....Reading config from {}".format(
            filepath
        ))
        self.value = {}
        configParse = configparser.ConfigParser()

        try:
            if len(configParse.read(filepath)) == 0:
                raise define.SpiderError("ERROR - Config file not exist.")
        except configparser.MissingSectionHeaderError:
            raise define.SpiderError("ERROR - Config file is broken.")

        if "spider" not in configParse.sections():
            raise define.SpiderError("ERROR - Config file format wrong.")
        for key in configParse['spider']:
            self.value[key] = configParse['spider'][key]

        self.logger.info("....Checking config value.")
        self.__checkValue()
        self.logger.info("....Read config finished, config is: {}".format(
            self.value
        ))

    def __checkValue(self):
        """
        Check legitimacy of config value.
        """
        try:
            #Check value of max_depth, crawl_interval, crawl_timeout, thread_count.
            try:
                numberCheckDict = {
                    "max_depth": 0,
                    "crawl_interval": 0,
                    "crawl_timeout": 0,
                    "thread_count": 0
                }

                for key in numberCheckDict:
                    if not int(self.value[key]) > numberCheckDict[key]:
                        raise define.SpiderError(
                            "ERROR - {} should bigger than {}.".format(
                                key, numberCheckDict[key]
                            ))
            except ValueError:
                raise ValueError("ERROR - max_depth, crawl_interval, crawl_timeout" +\
                            " should be number.")

            #Check url list files
            if not os.path.isfile(ROOT_PATH + '/' + self.value['url_list_file']):
                raise define.SpiderError("ERROR - url list file not exist.")
            #Check output_directory
            if not os.path.isdir(ROOT_PATH + '/' + self.value['output_directory']):
                try:
                    os.mkdir(ROOT_PATH + '/' + self.value['output_directory'])
                except:
                    raise define.SpiderError("ERROR - output_directory value wrong.")
            #Check target_url
            try:
                re.compile(self.value['target_url'])
            except:
                raise define.SpiderError("ERROR - target_url is not a legal re expression.")
        except KeyError:
            raise define.SpiderError("ERROR - Config key is wrong.")


    def __getitem__(self, i):
        """
        Override getitem operation.
        """
        return self.value[i]
