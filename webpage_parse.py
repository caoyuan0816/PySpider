#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
webpage_parse.py

Parse webpage, get links which match re expressions.
"""

import os
import sys
import logging
import re
import urllib.parse

#Set running path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)
LIB_PATH = './thirdlib'
sys.path.append(ROOT_PATH + '/' + LIB_PATH)

import bs4

import config_load

class webParser:
    """
    Class webParser.
    Will use third-lib beautifulsoup to parse HTML code.
    """
    def __init__(self, HTMLcode, baseURL):
        """
        Construct method of class webParser.
        """
        self.HTMLcode = HTMLcode
        self.config = config_load.Config()
        self.baseURL = baseURL

    def parse(self):
        """
        Parse HTML code.
        """
        self.soup = bs4.BeautifulSoup(self.HTMLcode, "html.parser")

    def getLinks(self):
        """
        Get links list in HTML.
        And the link will match re expression.
        """
        def has_href(tag):
            #Judge function
            if tag.name == "a" and tag.has_attr("href"):
                return True
            else:
                return False

        linksList = [x['href'] for x in self.soup.find_all(has_href)]
        #print(linksList)

        #Complie re expression
        self.prog = re.compile(self.config['target_url'])

        return list(filter(lambda x: x != None,
                        map(self.__matchList,
                            map(self.__checkList, linksList))))

    def __checkList(self, link):
        """
        Check links, if it is not complete, fix it.
        """

        parse = list(urllib.parse.urlsplit(urllib.parse.urljoin(self.baseURL, link)))

        if not (parse[0] == 'http' or parse[0] == 'https'):
            return None

        return urllib.parse.urlunsplit(parse)


    def __matchList(self, link):
        """
        Match list using re expression from config file.
        """
        if link == None:
            return None
        result = self.prog.match(link)
        if not result == None:
            return result.group()
        return None
