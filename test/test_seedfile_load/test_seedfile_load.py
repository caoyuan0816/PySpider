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

import seedfile_load
import exception
import log

class TestSeed(unittest.TestCase):
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
        self.seed = seedfile_load.Seed()

    def test_readSeed(self):
        """
        Test readConfig:
        """

        self.logger.info("=============Test readSeed=============")
        #1
        self.logger.info("-------------------------Test1: Invalid file path.")
        with self.assertRaises(exception.SpiderError) as e:
            self.seed.readSeed("123")
        self.assertEqual(e.exception.value,
                        "ERROR - Seed file not exist.",
                        "Invalid file path.")

        #2
        self.logger.info("-------------------------Test2: Invalid encode format file.")
        with self.assertRaises(exception.SpiderError) as e:
            self.seed.readSeed(ROOT_PATH + "/gbk.urls")
        self.assertEqual(e.exception.value,
                        "ERROR - Seed file not encode by utf-8.",
                        "Invalid encode format file.")

        #3
        self.logger.info("-------------------------Test3: Good file.")
        self.seed.readSeed(ROOT_PATH + "/urls")
        self.assertEqual(len(self.seed.value), 3)

        #4
        self.logger.info("-------------------------Test4: singleton decorator test.")
        newSeed = seedfile_load.Seed()
        self.assertEqual(self.seed,
                         newSeed,
                         "singleton decorator test.")

        #5
        self.logger.info("-------------------------Test5: Invalid value.")
        with self.assertRaises(exception.SpiderError) as e:
            self.seed.readSeed(ROOT_PATH + "/wrong.urls")
        self.assertEqual(e.exception.value,
                        "ERROR - URL format wrong. Example: http://www.baidu.com",
                        "Invalid value.")


if __name__ == '__main__':
    unittest.main()
