#! usr/bin/python 
#coding=utf-8 

import sys

from pybloom import BloomFilter

from lib.core import scrawler
from lib.core.scrawler import Crawler
from lib.core.scrawler import t_crawlerApi
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio

bloom = BloomFilter(capacity=100000, error_rate=0.001)

#域名收集
#TODO 
def domain_collect(filter, url):

	network = Network()
	
	crawler = Crawler(bloom)
	(proto, subdomain, domain, resources, suffix) = crawler.separate(url)
	domains = Censysio().certificates(filter)['domain']
	crawler.filter = filter
	crawler.level = 2
	crawler.appendDomain(url)
	crawler.start()
	
	#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异的域名
	domain_arry = crawler.getHost()['domain']
	list_diff = [ i for i in domains if i not in domain_arry ]
	if list_diff:
		infoMsg = "diff ==> %s"%str(list_diff)
		logger.info(infoMsg)
		crawler.appendDomain(list_diff)
		crawler.start()
	domain_arry = crawler.getHost()['domain']
	for key in domain_arry:
		for domain in domain_arry[key]:
			domains.append(domain)
	#return network.ip(list(set(domains)))

'''file = open('domain')
 
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        print domain_collect(['http', line.replace('\n','')])'''
domain_collect('fytest.com', 'http://www.fytest.com')
