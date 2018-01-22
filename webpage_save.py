#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
webpage_save.py

Save webpage to disk.
"""

import os
import logging

import config_load
import define

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

def saveToDisk(filepath, filename, content, encode_type='utf-8'):
    """
    Save content to file in disk which describe by file path.
    Default use uft-8 encode.
    """

    config = config_load.Config()

    #Transferred URL meaning
    filename = filename.replace('/', '\\')

    try:
        with open(filepath + '/' + filename, 'wb') as writeFile:
            writeFile.write(content.encode(encode_type))
    except IsADirectoryError:
        raise define.SpiderError("ERROR - file path invalid.")
    except LookupError:
        raise define.SpiderError("ERROR - Encode type is wrong.")
