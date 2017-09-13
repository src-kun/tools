#! usr/bin/python 
#coding=utf-8 

from lib.core import scrawler
from lib.core.log import logger
from lib.core.domain import network

#scrawler.t_demo()

gp = network()
print gp.ip("sbaidu.com")
print gp.location("140.205.32.12")