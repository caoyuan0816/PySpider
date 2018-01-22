#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Test case of config_load.py
"""

import sys
import os
import unittest
import logging

#Config sys path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)
RUN_PATH = '../../'
sys.path.append(ROOT_PATH + '/' + RUN_PATH)
CONFIG_PATH = ROOT_PATH + '/' + RUN_PATH + 'spider.conf'

import config_load
import webpage_parse
import exception
import log

class TestWebPageParse(unittest.TestCase):
    """
    Class TestConfig, test methods in class Config.
    """
    def setUp(self):
        """
        Set up.
        """
        log.setLogger("spider",
                    logging.DEBUG,
                    "%(asctime)s - %(name)s - %(levelname)s - [%(module)s] - %(message)s",
                    ROOT_PATH + '/log')

        config = config_load.Config()
        config.readConfig(CONFIG_PATH)

        self.logger = logging.getLogger("spider")

        self.baseURL = "http://www.baidu.com"
        self.badData = "<html>1o08971237128937127896123".encode('utf-8')
        self.goodData = "<html><head></head><body><a href = 'http://www.baidu.com'>123123</a></body></html>".encode('utf-8')
        self.fixURLData = "<html><head></head><body><a href = '123'>123123</a></body></html>".encode('utf-8')
        self.badHrefData = "<html><head></head><body><a href = 'javascript:;'>123123</a></body></html>".encode('utf-8')
        self.gbk = "<html><head></head><body><a href = 'http://www.baidu.com'>123123</a></body></html>".encode('gbk')


    def test_readSeed(self):
        """
        Test readConfig:
        """

        self.logger.info("=============Test webParser=============")
        #1
        self.logger.info("-------------------------Test1: Invalid HTML code.")
        parser = webpage_parse.webParser(self.badData, self.baseURL)
        parser.parse()
        parser.getLinks()

        #2
        self.logger.info("-------------------------Test2: normal HTML code.")
        parser = webpage_parse.webParser(self.goodData, self.baseURL)
        parser.parse()
        self.assertEqual(parser.getLinks(),
                        ['http://www.baidu.com'],
                        "normal HTML code.")

        #3
        self.logger.info("-------------------------Test3: Invalid href.")
        parser = webpage_parse.webParser(self.badHrefData, self.baseURL)
        parser.parse()
        self.assertEqual(parser.getLinks(),
                        [],
                        "href = javascript:;")

        #4
        self.logger.info("-------------------------Test4: URLjoin test.")
        parser = webpage_parse.webParser(self.fixURLData, self.baseURL)
        parser.parse()
        self.assertEqual(parser.getLinks(),
                        ['http://www.baidu.com/123'],
                        "Test URLjoin.")

        #4
        self.logger.info("-------------------------Test4: GBK encode data.")
        parser = webpage_parse.webParser(self.gbk, self.baseURL)
        parser.parse()
        self.assertEqual(parser.getLinks(),
                    ['http://www.baidu.com'],
                    "GBK encode data.")



if __name__ == '__main__':
    unittest.main()
