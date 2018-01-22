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

import config_load
import exception
import log

class TestConfig(unittest.TestCase):
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
        self.logger = logging.getLogger("spider")
        self.config = config_load.Config()

    def test_readConfig(self):
        """
        Test readConfig:
        """
        self.logger.info("=============Test readConfig=============")
        #1
        self.logger.info("-------------------------Test1: Invalid file path.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig("123")

        self.assertEqual(e.exception.value,
                        "ERROR - Config file not exist.",
                        "Invalid file path.")

        #2
        self.logger.info("-------------------------Test2: Empty file.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/empty.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - Config file format wrong.",
                        "Empty file.")

        #3
        self.logger.info("-------------------------Test3: Wrong file.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/wrong.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - Config file format wrong.",
                        "Wrong file.")

        #4
        self.logger.info("-------------------------Test4: Broken file.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/broken.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - Config file is broken.",
                        "Broken file.")

        #5
        self.logger.info("-------------------------Test5: Good file.")
        self.config.readConfig(ROOT_PATH + "/good.conf")


    def test_configValue(self):
        """
        Test config value:
        """
        self.logger.info("=============Test check config value=============")
        #1
        self.logger.info("-------------------------Test1: max_depth is not number.")
        with self.assertRaises(ValueError) as e:
            self.config.readConfig(ROOT_PATH + "/value1.conf")

        self.assertEqual(str(e.exception),
                        "ERROR - max_depth, crawl_interval, crawl_timeout" +\
                                " should be number.",
                        "max_depth is not number.")

        #2
        self.logger.info("-------------------------Test1: max_depth is not number.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/value2.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - crawl_interval should bigger than 0.",
                        "crawl_interaval is -1.")

        #3
        self.logger.info("-------------------------Test2: URL list file not exist.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/value3.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - url list file not exist.",
                        "URL list file not exist.")

        #4
        self.logger.info("-------------------------Test3: target_url is not a legal re expression.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/value4.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - target_url is not a legal re expression.",
                        "target_url is not a legal re expression.")

        #5
        self.logger.info("-------------------------Test4: Config key is wrong.")
        with self.assertRaises(exception.SpiderError) as e:
            self.config.readConfig(ROOT_PATH + "/value5.conf")

        self.assertEqual(e.exception.value,
                        "ERROR - Config key is wrong.",
                        "Config key is wrong.")

        #6
        self.logger.info("-------------------------Test5: __getitem__ overload.")
        self.config.readConfig(ROOT_PATH + "/good.conf")
        self.assertEqual(self.config['thread_count'],
                        '8',
                        "__getitem__ overload.")

        #7
        self.logger.info("-------------------------Test6: singleton decorator test.")
        newConfig =  config_load.Config()
        self.assertEqual(self.config,
                         newConfig,
                         "singleton decorator test.")


if __name__ == '__main__':
    unittest.main()
