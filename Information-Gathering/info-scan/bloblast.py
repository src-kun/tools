#! usr/bin/python 
#coding=utf-8 

import sys

from pybloom import BloomFilter


from lib.core.scrawler import Crawler
from lib.core.scrawler import t_crawlerApi
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio

bloom = BloomFilter(capacity=100000, error_rate=0.001)
#域名收集
#TODO 
def domain_collect(dom):

	url = ["http", dom]
	filter = dom.replace("www.","")
	network = Network()
	domains = list(set(Censysio().certificates(url[1])[url[1]]))

	crawler = Crawler(bloom)
	crawler.filter = filter
	crawler.start_url = url
	crawler.level = 3
	while True:
		crawler.start()
		#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异的域名
		list_diff = [ i for i in domains if i not in crawler.host ]
		if not list_diff:
			break
		#depth = crawler.host["depth"] + 1
		break
		
	d = []
	for key in crawler.host:
		for dommin in crawler.host[key]:
			d.append(dommin[1])
	
	return network.ip(list(set(d)))

file = open("domain")
while True:
	lines = file.readlines(10000)
	if not lines:
		break
	for line in lines:
		print domain_collect(line.replace("\n",""))	
