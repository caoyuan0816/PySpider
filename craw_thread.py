#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
craw_thread.py
"""

import os
import sys
import logging
import threading
import urllib.request
import traceback
import time

import define
import webpage_parse
import config_load
import webpage_save
import url_table

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)
LIB_PATH = './thirdlib'
sys.path.append(ROOT_PATH + '/' + LIB_PATH)

import requests

class CrawThread(threading.Thread):
    """
    Class CrawThread.
    Implemment craw thread.
    """
    def __init__(self, URLqueue):
        """
        Construct method.
        """
        self._URLqueue = URLqueue
        self._logger = logging.getLogger('spider')
        self._config = config_load.Config()
        self._URLtable = url_table.Table()

        threading.Thread.__init__(self)

    def run(self):
        """
        Override run() method.
        """
        self._logger.info("....{}: Starting".format(
            self._name,
        ))
        while not self._URLqueue.empty():
            try:
                cur = self._URLqueue.get()
                self._logger.info("....{}: Deal URL: {} Level: {}".format(
                    self._name, cur.URL, cur.level
                ))

                #Depth check
                if cur.level >= int(self._config['max_depth']):
                    self._logger.info("....{}: Out of max depth.")
                    continue

                self._logger.info("....{}: Downloading and parse.".format(self._name))
                #Download page
                request = requests.get(cur.URL, timeout=int(self._config['crawl_timeout']))
                content = request.text

                #Parse page
                parser = webpage_parse.webParser(content, cur.URL)
                parser.parse()

                uniqueList = self._URLtable.uniqueAndSave(parser.getLinks())

                for it in uniqueList:
                    self._URLqueue.put(define.QueueElement(it, cur.level + 1))

                self._logger.info("....{}: Encode format is: {}, Have {} links".format(
                    self._name, request.encoding, len(linksList)
                ))

                self._logger.info("....{}: Saving to disk.".format(self._name))
                #Save page to Disk
                webpage_save.saveToDisk(ROOT_PATH + '/' + self._config['output_directory'],
                                        cur.URL,
                                        parser.soup.prettify())

                self._logger.info("....{}: Finished Deal URL: {} Level: {}".format(
                    self._name, cur.URL, cur.level
                ))
            except Exception as e:
                self._logger.warning("....{}: Deal URL: {} Failed.".format(
                    self._name, cur.URL
                ))
                self._logger.warning("....{}: Error Message: \n{}".format(
                    self._name, traceback.format_exc()
                ))
            finally:
                time.sleep(int(self._config['crawl_interval']))
                self._URLqueue.task_done()
