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
from lib.core.rest import NessusRest
from lib.core.scan import NessusScan
from lib.core.rest import WvsRest
from lib.core.scan import WvsScan
from lib.core.settings import maseting
from lib.core.settings import neseting
from lib.core.settings import hydseting
from lib.core.crack import Hydra
from lib.utils.common import input
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
		os.system('cd %s && sh %s'%(hydseting.bin, hydseting.install_path))
	if not os.path.exists(maseting.lock_path):
		#安装masscan所需环境
		os.system('cd %s && sh %s'%(maseting.bin, maseting.install_path))
elif WINDOWS in systype.lower():
	#TODO
	pass
else:
	print 'unkown operating system'
#self.__bin_check()

class Information():

	def __init__(self, url):
		self.url = url
		(self.proto, self.substr, self.domain, self.resources, self.suffix) = separate(self.url)
		self.mark = self.domain.replace('www.','')

	#域名收集
	def domain_collect(self): 
		#TODO 测试数据
		return  ['e28.me','www.r28.me','www.d28.me','www.lsf0.com','www.lsf9.com','g28.me','lsf0.com','r28.me','q28.me','www.j28.me','www.z28.me','t28.me','www.q28.me','www.t28.me','www.n28.me','www.p28.me','z28.me','k28.me','www.g28.me','www.l28.me','lsf9.com','n28.me','www.k28.me','d28.me','j28.me','l28.me','y28.me','p28.me','www.e28.me','www.y28.me']
		domains = []
		crawler = Crawler(bloom)
		
		#空间搜索引擎采集域名信息
		domains.extend(Censysio().certificates(self.domain)['domain'])
		
		#爬虫爬取网络信息
		filter = self.domain.replace('www.','')
		crawler.filter = filter
		crawler.level = 5
		crawler.appendDomain(self.url)
		crawler.start()
		
		#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异域名
		diff = crawler.appendDomain(domains)
		if diff:
			crawler.level += 1
			infoMsg = "censys and crawler diff ==> %s"%str(domains)
			logger.info(infoMsg)
			crawler.start()
		return crawler.getHost()['domain']
		
	#ip 采集
	def ip_collect(self, domain_arry):
		return Network().ip(domain_arry)

	#网络扫描
	#targets 扫描IP地址、scan_name 扫描任务名称
	#
	def network_scan(self, targets, description = ''):
		nessus = Nessus()
		folder_id = None
		uuid = nessus.templates('policy', nessus.templates_arry[neseting.BASIC_NETWORK_SCAN])['uuid']
		
		#任务名默认使用
		scan_name = self.mark
		
		#文件夹名字默认使用域名，不存在创建
		folder = self.mark
		msg = nessus.create_folder(folder)
		if nessus.getError(msg):
			folder_id = nessus.folders(folder)['id']
		else:
			folder_id = msg['id']
		policy_id = nessus.policies(neseting.POLICIE_COMPLEX)['id']
		#创建扫描任务
		msg = nessus.create_scan(uuid, scan_name, targets, policy_id = policy_id, folder_id = folder_id, description = description)
		if nessus.getError(msg):
			warnMsg = 'nessus create scan faild : %s'%msg['error']
			logger.warn(warnMsg)
		else:
			#开始扫描
			msg = nessus.start_scan(msg['scan']['id'])
			if nessus.getError(msg): 
				warnMsg = 'nessus start scan faild : %s'%msg['error']
				logger.warn(warnMsg)
				msg = None
		return msg
	
	def port_scan(ip):
		masscan = Masscan()
		scan_dict = masscan.scan('111.202.114.53', maseting.QUICK_SCAN, 'airtel.com')
		print masscan.export_json(scan_dict['name'])
		print 
		print 
		print masscan.select_history(group_id=scan_dict['group_id'])
		
	def proto_crack(self, ip, port, proto):
		hydra = Hydra()
		#hydra.start(target = ip, user_dict_path = hydseting.user_dict_path, password_dict_path =  hydseting.password_dict_path, port = port, proto = proto)
		#hydra.restore(hydseting.restore + 'hydra.restore')
"""blob['domain'].extend(domain_collect('mlr.gov.cn','http://www.mlr.gov.cn'))
blob.update(ip_collect(blob['domain']))
print blob"""

"""masscan = MasscanRest()
scan_dict = masscan.scan('111.202.114.53', maseting.QUICK_SCAN, 'airtel.com')
print masscan.export_json(scan_dict['name'])
print 
print 
print masscan.select_history(group_id=scan_dict['group_id'])"""

"""
scan_status = nessus.details_scan(25)['history'][0]['status']
while cmp(scan_status,'completed'):
	time.sleep(3)
	print scan_status
"""
from lib.core.settings import wvseting
wvs = WvsRest(wvseting.api_key)
#print wvs.add_target('http://www.q28.me/')
#print wvs.start('283832b5-314b-4135-a333-cf4c1b125dce')
#print wvs.type_scan()
#print wvs.list_targets(query = 'group_id:4d6f4994-7036-4cb8-802f-fed6560e7034')
#print wvs.del_target('820d6a15-c555-4411-ba00-03fe82ce3811')
#print len(wvs.list_scans(query = 'status:aborted;', previous_cursor = 100)['scans'])
#print wvs.del_scan('0a6f24d7-b6be-422e-a4d2-8795b77b3ec4')
#print wvs.search_target('csdn.net')
#print wvs.create_group_target('csdn.net')
#print wvs.del_group_target('008ba33b-af79-4ffb-aba5-6ab78bb47aac')
#print wvs.list_groups_target('csdn.net')
#print wvs.search_scans('cd9f576f-11cb-40ad-8692-e4b3d5271c79')
#print wvs.stop('2c682493-149c-4cbc-b65a-de50313f842a')
hydra = Hydra()
#hydra.start(target = '127.0.0.1', user_dict_path = hydseting.user_dict_path, password_dict_path =  hydseting.password_dict_path, proto = 'ssh')
#hydra.restore(hydseting.restore + 'hydra.restore')
info = Information('http://zfzhandian.com')
#targets = ','.join(info.domain_collect())
#print info.network_scan(targets)
#targets = info.domain_collect()
#wvscan = WvsScan(wvseting.api_key)
#wvscan.scan(targets, wvscan.FULL_SCAN, '28pc.com', launch_now = True)
#wvscan.clean_targets()
#wvscan.clean_scans(group_name = '28pc.com')
#print wvscan.getGroupByName('test')
#print len(wvscan.get_targets(group_id = '28pc.com', text = '.me'))
#print wvscan.get_scans(group_name = '28pc.com', status = wvscan.SCAN_STATUS_PROCESSING)
#wvscan.stop()

nessus = NessusRest(neseting.access, neseting.secret)
scan_id = 17
#print nessus.templates('policy')
#print nessus.create_scan("731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65", 'testone', '127.0.0.1', policy_id = 11, folder_id = 4, description = 'test')
#print nessus.policies(neseting.POLICIE_COMPLEX)
#print nessus.folders('test')
#print nessus.start_scan(17)
#print nessus.list_scan(4)
#print nessus.status_scan(9)
#msg = nessus.create_folder('test')
#print nessus.getError(msg)
#print nessus.del_folder(4)
"""import time
file_id = nessus.file_id_scan(9)['file']
print file_id
while nessus.export_status(scan_id, file_id):
	time.sleep(0.3)
nessus.download_export(scan_id,file_id)"""
#print nessus.status_scan(scan_id)
#print nessus.details_scan(scan_id)
#检测nessus运行状态

#, 
targets = '127.0.0.1,10.102.16.196,10.102.16.197,10.102.16.198,192.168.230.140'
nesscan = NessusScan(neseting.access, neseting.secret)
#template_uuid = nesscan.getScanPolicyTemplateByName(nessus.BASIC_NETWORK_SCAN)['uuid']
#policy_id = nesscan.getPoliciesTemplateByName('complex')['id']
#print nesscan.scan(template_uuid = template_uuid, scan_name = 'scan_name', targets = targets, policy_id = policy_id, launch_now = True)
#nesscan.stop(81)
#print nesscan.create_folder('sedfg')
#print nesscan.list_scan()
print nesscan.getFolderByName('test')