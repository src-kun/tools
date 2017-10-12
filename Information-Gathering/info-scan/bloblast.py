#! usr/bin/python 
#coding=utf-8 

import sys
import os

from pybloom import BloomFilter

from lib.core import scrawler
from lib.core.scrawler import Crawler
from lib.core.scrawler import t_crawlerApi
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio
from lib.utils.common import separate
from lib.core.scan import Masscan
from lib.core.scan import Nessus
from lib.core.scan import Wvs
from lib.core.settings import maseting
from lib.core.settings import neseting
from lib.core.settings import hydseting
from lib.core.crack import Hydra
from lib.core import settings
from lib.connection.http import Request
bloom = BloomFilter(capacity=100000, error_rate=0.001)

blob = {'domain':[]}

#初始化项目
import platform
LINUX = 'linux'
WINDOWS = 'windows'

(systype, hostname, kernel, version, graphics, bit) = platform.uname()
if LINUX in systype.lower():
	if not os.path.exists(hydseting.lock_path):
		#安装hydra所需环境
		os.system('sh %s'%hydseting.install_path)
	if not os.path.exists(maseting.lock_path):
		#安装masscan所需环境
		os.system('sh %s'%maseting.install_path)
elif WINDOWS in systype.lower():
	#TODO
	pass
else:
	print 'unkown operating system'
#self.__bin_check()

#域名收集
def domain_collect(filter, url):
	
	crawler = Crawler(bloom)
	(proto, substr, domain, resources, suffix) = separate(url)
	domains = []#Censysio().certificates(filter)['domain']
	crawler.filter = filter
	crawler.level = 5
	crawler.appendDomain(url)
	crawler.start()
	
	#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异的域名
	if domains and crawler.appendDomain(domains):
		crawler.level += 1
		infoMsg = "censys and crawler diff ==> %s"%str(domains)
		logger.info(infoMsg)
		crawler.start()
	return crawler.getHost()['domain']
	
#ip 采集
def ip_collect(domain_arry):
	return Network().ip(domain_arry)


#blob['domain'].extend(domain_collect('cnblogs.','https://www.cnblogs.com'))
#http://www.mlr.gov.cn/
"""blob['domain'].extend(domain_collect('mlr.gov.cn','http://www.mlr.gov.cn'))
blob.update(ip_collect(blob['domain']))
print blob"""

"""masscan = Masscan()
scan_dict = masscan.scan('111.202.114.53', maseting.QUICK_SCAN, 'airtel.com')
print masscan.export_json(scan_dict['name'])
print 
print 
print masscan.select_history(group_id=scan_dict['group_id'])"""
nessus = Nessus()
scan_id = 17
#print nessus.templates('policy', nessus.templates_arry[neseting.BASIC_NETWORK_SCAN])
#print nessus.create_scan("731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65", 'testone', '127.0.0.1', policy_id = 11, folder_id = 4, description = 'test')
#print nessus.policies(neseting.POLICIE_COMPLEX)
#print nessus.folders('test')['id']
#print nessus.start_scan(17)
#print nessus.list_scan(4)
#print nessus.status_scan(9)
"""import time
file_id = nessus.file_id_scan(9)['file']
print file_id
while nessus.export_status(scan_id, file_id):
	time.sleep(0.3)
nessus.download_export(scan_id,file_id)"""
#print nessus.status_scan(scan_id)
#print nessus.details_scan(scan_id)
#检测nessus运行状态
"""
scan_status = nessus.details_scan(25)['history'][0]['status']
while cmp(scan_status,'completed'):
	time.sleep(3)
	print scan_status
"""
wvs = Wvs()
#print wvs.add_target('https://www.q28.me/')
#print wvs.start_scan('e01a9096-d2aa-40da-b564-6ac5196d249f')
#print wvs.type_scan()
#print wvs.list_target()
#print wvs.del_target('820d6a15-c555-4411-ba00-03fe82ce3811')
#print wvs.list_scans()
#print wvs.del_scan('0a6f24d7-b6be-422e-a4d2-8795b77b3ec4')
hydra = Hydra()
#hydra.start()