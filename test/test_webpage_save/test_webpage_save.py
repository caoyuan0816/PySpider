#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Test case of config_load.py
"""

import sys
import os
import unittest
import logging
import subprocess

#Config sys path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)
RUN_PATH = '../../'
sys.path.append(ROOT_PATH + '/' + RUN_PATH)
TEMP_PATH = ROOT_PATH + '/output'

import config_load
import webpage_save
import exception
import log

class TestWebPageSave(unittest.TestCase):
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

        os.mkdir(TEMP_PATH)


    def tearDown(self):
        """
        Tear down.
        """
        self.logger.info("Tearing Down.")

        #Remove temp dir and contents
        fileList = subprocess.check_output(["ls", TEMP_PATH],).decode('utf-8').split('\n')[:-1]
        for it in fileList:
            os.remove(TEMP_PATH + '/' + it)
        os.rmdir(TEMP_PATH)


    def test_saveToDisk(self):
        """
        Test saveToDisk:
        """

        self.logger.info("=============Test saveToDisk=============")
        #1
        self.logger.info("-------------------------Test1: Invalid file path(filepath is a dirpath).")
        with self.assertRaises(exception.SpiderError) as e:
            webpage_save.saveToDisk(TEMP_PATH, '.',"666")
        self.assertEqual(e.exception.value,
                        "ERROR - file path invalid.",
                        "Invalid file path(filepath is a dirpath).")

        #2
        self.logger.info("-------------------------Test2: unicode str value.")
        str_unicode = "你好"
        webpage_save.saveToDisk(TEMP_PATH, 'test2', str_unicode, 'utf-8')
        with open(TEMP_PATH + '/test2','rb') as fileTest2:
            self.assertEqual(fileTest2.read(),
                             str_unicode.encode('utf-8'),
                             "unicode str value.")

        #3
        self.logger.info("-------------------------Test3: Invalid encode type.")
        with self.assertRaises(exception.SpiderError) as e:
            webpage_save.saveToDisk(TEMP_PATH, 'test3', 'test3', 'aaaaa')
        self.assertEqual(e.exception.value,
                         "ERROR - Encode type is wrong.",
                         "Invalid encdoe type.")

        #4
        self.logger.info("-------------------------Test4: URL file name.")
        webpage_save.saveToDisk(TEMP_PATH, 'http://www.baidu.com', 'test4')

        #5
        self.logger.info("-------------------------Test5: URL file name.")
        webpage_save.saveToDisk(TEMP_PATH, 'http://www.baidu.com/231/php?ask=123&id=123', 'test5')

        #6
        self.logger.info("-------------------------Test6: URL file name.")
        webpage_save.saveToDisk(TEMP_PATH, 'http://www.baidu.com/231/php?id=哈哈', 'test6')


if __name__ == '__main__':
    unittest.main()
