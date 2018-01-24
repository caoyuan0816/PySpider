#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
Python mini spider

A mini multithread spider.
"""

import os
import logging
import urllib.request
import queue

import log
import define
import config_load
import seedfile_load
import webpage_save
import webpage_parse
import url_table
import craw_thread

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

#Set logger
log.setLogger("spider",
            logging.DEBUG,
            "%(asctime)s - %(name)s - %(levelname)s - [%(module)s] - %(message)s",
            ROOT_PATH + '/log')
logger = logging.getLogger("spider")


def init(configFilePath = ROOT_PATH + '/spider.conf'):
    """
    Run init functions.
    Will init class Config and Seed(singleton class).
    - load config data from config file. Default: ./spider.conf
    - load seed data from seed file. Default: ./urls
    """

    logger.info("Init config, seedfile, urltalbe and URL queue.")
    #Load config data
    config = config_load.Config()
    config.readConfig(configFilePath)

    #Load urls data
    seed = seedfile_load.Seed()
    seed.readSeed(ROOT_PATH + '/' + config.value['url_list_file'])

    #Init url_table and queue use seed URL
    table = url_table.Table()
    URLqueue = queue.Queue()
    addList = table.uniqueAndSave(seed.value)
    for it in addList:
        URLqueue.put(define.QueueElement(it, 0))

    logger.info("Init success.")
    return config, seed, URLqueue


def main():
    """
    Main function of mini spider.
    """
    logger.info("Starting Mini-spider.")

    #Init
    config, seed, URLqueue = init(ROOT_PATH + '/spider.conf')

    THREAD_NUM = int(config['thread_count'])
    logger.info("Creating craw threads. Thread num: {}".format(
        THREAD_NUM
    ))
    for i in range(THREAD_NUM):
        thread = craw_thread.CrawThread(URLqueue)
        thread.start()
    URLqueue.join()

    logger.info("Shutting down Mini-spider.\n")


if __name__ == '__main__':
    main()
