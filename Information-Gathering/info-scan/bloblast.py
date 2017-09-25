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
from lib.utils.common import separate

bloom = BloomFilter(capacity=100000, error_rate=0.001)

blob = {'domain':[]}

#域名收集
def domain_collect(filter, url):
	
	crawler = Crawler(bloom)
	(proto, substr, domain, resources, suffix) = separate(url)
	domains = []#Censysio().certificates(filter)['domain']
	crawler.filter = filter
	crawler.level = 3
	crawler.appendDomain(url)
	crawler.start()
	
	#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异的域名
	if domains and crawler.appendDomain(domains):
		crawler.level += 1
		infoMsg = "censys and crawler diff ==> %s"%str(domains)
		logger.info(infoMsg)
		crawler.start()
	print
	print
	print crawler.getHost()['raw']['url']
	print
	print
	return crawler.getHost()['domain']
	
#ip 采集
def ip_collect(domain_arry):
	return Network().ip(domain_arry)

'''file = open('domain')
 
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        print domain_collect(['http', line.replace('\n','')])'''

#print domain_collect('csdn.net','http://www.csdn.net')
blob['domain'].extend(domain_collect('cnblogs.','https://www.cnblogs.com'))
blob.update(ip_collect(blob['domain']))
print blob