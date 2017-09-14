#! usr/bin/python 
#coding=utf-8 

import sys
from lib.core import scrawler
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio

#scrawler.t_demo()

#gp = Network()
#print gp.ip("sbaidu.com")
#print gp.location("140.205.32.12")
print Censysio().censysIPv4("bit.edu.cn")
