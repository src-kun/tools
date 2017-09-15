#! usr/bin/python 
#coding=utf-8 

import sys
from lib.core import scrawler
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio

url = ["http", "csdn.net"]
domains = scrawler.t_demo(url, url[1])

gp = Network()
#gp.ip(["www.baidu.com"])
#print gp.location("192.168.136.138")
#print Censysio().censysIPv4("bit.edu.cn")
d = Censysio().certificates(url[1])[url[1]]
print domains
print 

for key in domains:
	for ds in domains[key]:
		d.append(ds[1])
	

print gp.ip(list(set(d)))