#! usr/bin/python 
#coding=utf-8 

import sys
import os
import time
import socket

from pybloom import BloomFilter
import platform

from lib.core import scrawler
from lib.core.scrawler import Crawler
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio
from lib.utils.common import separate
from lib.core.rest import NessusRest
from lib.core.scan import NessusScan
from lib.core.rest import WvsRest
from lib.core.scan import WvsScan
from lib.core.settings import maseting
#from lib.core.settings import neseting
from lib.core.settings import hydseting
from lib.core.crack import Hydra
from lib.utils.common import input
from lib.core import settings
from lib.connection.http import Request



blob = {'domain':[]}

#初始化项目
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

access = '9ce1ca30eb7ec4511af9c29cb74e96cd35a7dc400439459599454d079a176f3d'
secret = 'b289fedbb80c0a405609b7493299ebf3235b9cb847554807afdbe00e654d2f29'
base_url = 'https://10.102.16.196:8834/'

wvs_api_key = '1986ad8c0a5b3df4d7028d5f3c06e936c10a743b8beb644cd852d9320bd0e3a4e'
wvs_base_url = 'https://10.102.16.196:3443/'
class Information():
	
	
	def __init__(self, target):
		self.__target = target
		
		self.collect = {
						'domain': [],
						'ip': []
					}
	
	def check_https(self, domain):
		ip = Network().ip(domain)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			s.connect((ip, 443))
			return True
		except Exception,e:
			return False

	def get_target(self):
		return self.__target
	
	#域名收集
	def domain(self, filter, level = 5):
		domains = []
		
		#[u'mx41.csdn.net', u'*.csdn.net', u'code.csdn.net', u'forums.aws.csdn.net', u'aws.csdn.net', u'passport.csdn.net', u'csdn.net', 'www.csdn.net']
		#TODO 调试
		self.collect['domain'].extend(['e28.me','www.r28.me','www.d28.me','www.lsf0.com','www.lsf9.com','g28.me','lsf0.com','r28.me','q28.me','www.j28.me','www.z28.me','t28.me','www.q28.me','www.t28.me','www.n28.me','www.p28.me','z28.me','k28.me','www.g28.me','www.l28.me','lsf9.com','n28.me','www.k28.me','d28.me','j28.me','l28.me','y28.me','p28.me','www.e28.me','www.y28.me'])
		self.collect['ip'].extend(['52.175.25.185', '137.116.169.118', '137.116.169.118', '137.116.169.118', '103.21.118.253', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '13.75.88.216', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '', '137.116.169.118', '137.116.169.118', '137.116.169.118', '103.21.118.253', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '137.116.169.118', '52.175.25.185', '137.116.169.118'])
		return
		#空间搜索引擎采集域名信息
		#domains.extend(Censysio().certificates(self.domain.replace('www.',''))['domain'])
		l = len(domains)
		for i in range(0, l):
			#TODO 支持两种协议
			#domains.append('https://' + domains[i])
			domains[i] = self.proto + '://' + domains[i]
		#爬虫爬取网络信息
		self.crawler.filter = filter
		self.crawler.set_targets(self.__target)
		self.crawler.set_targets(domains)
		self.crawler.level = level
		self.crawler.start()
		self.collect['domain'] = self.crawler.getHost()['domain']
		self.collect['ip'] = Network().ip(self.collect['domain'])
		return self.collect['domain']
	
	#TODO ip 采集
	def ip(self):
		pass
	
	def get_ip(self):
		return self.collect['ip']
		
	def get_domain(self):
		return self.collect['domain']
		
	
	def port_scan(ip):
		masscan = Masscan()
		scan_dict = masscan.scan('111.202.114.53', maseting.QUICK_SCAN, 'airtel.com')
		print masscan.export_json(scan_dict['name'])
		print 
		print 
		print masscan.select_history(group_id=scan_dict['group_id'])

class Exploit:
	
	def __init__(self, name, target = None, info = None, nesscan = None, wvs = None, bloom = None):
		
		self.settings = {
							'crawler': {
								'targets': '',
								'bloom': None,
								'filter': [],
								'level': 5
							},
							'nessus': {
								'scan': {
										'name':'',
										'targets': [],
										'description':'',
										'policy': 'complex',#complex 自定义的扫描策略 TODO complex不存在自动创建
								},
								'floder': {
										'id':None,
										'name':''
								}
							},
							'wvs': {
								'scan': {
										'name':'',
										'targets': [],
										'description':'',
										'profile_id': None
								},
								'group': {
									'id':None,
									'name':''
								}
							}
						}
		self.set_exploit_name(name)
		
		if info:
			self.__info = info
		else:
			self.__info = Information(target)
			
		self.__info.domain(filter = self.settings['crawler']['filter'])
		
		if nesscan:
			self.__nesscan = nesscan
		else:
			self.__nesscan = NessusScan(access, secret, base_url)
			
		if wvs:
			self.__wvs = wvs
		else:
			self.__wvs = WvsScan(api_key = wvs_api_key, base_url = wvs_base_url)
		
		if bloom:
			self.settings['crawler']['bloom'] = bloom
		else:
			self.settings['crawler']['bloom'] = BloomFilter(capacity=100000, error_rate=0.001)
		
		self.crawler = Crawler(self.settings['crawler']['bloom'])
	
	def set_exploit_name(self, name):
		self.settings['nessus']['scan']['name'] = name
		self.settings['nessus']['floder']['name'] = name
		self.settings['wvs']['group']['name'] = name
	
	#网络扫描
	#targets 扫描IP地址、scan_name 扫描任务名称
	def network(self):
		(proto, substr, domain, resources, suffix) = separate(self.__info.get_target())
		
		if not self.settings['crawler']['filter']:
			self.settings['crawler']['filter'] = domain.replace('www.','')
		
		if not self.settings['nessus']['scan']['targets']:
			self.settings['nessus']['scan']['targets'].extend(self.__info.collect['ip'])
		self.__nesscan.set_text_targets(self.settings['nessus']['scan']['targets'])
		floder = self.__nesscan.set_folder(self.settings['nessus']['floder']['name'])
		if not floder:
			self.__nesscan.create_folder(self.settings['nessus']['floder']['name'])
		self.settings['nessus']['floder'].update(self.__nesscan.get_folder())
		self.__nesscan.set_template(self.__nesscan.BASIC_NETWORK_SCAN)
		self.__nesscan.set_policy(self.settings['nessus']['scan']['policy'])
		self.__nesscan.scan(self.settings['nessus']['scan']['name'])
		#TODO 调试
		self.__nesscan.stop()
		return self.__nesscan.is_running()
		
	def application(self):
		if not self.settings['wvs']['scan']['targets']:
			self.settings['wvs']['scan']['targets'] = self.__info.get_domain()

		self.__wvs.set_targets(self.settings['wvs']['scan']['targets'])
		self.__wvs.scan(group_name = self.settings['wvs']['group']['name'])
		#TODO 调试
		self.__wvs.clean_targets()
		
	def crack(self, ip, port, proto):
		hydra = Hydra()
		#hydra.start(target = ip, user_dict_path = hydseting.user_dict_path, password_dict_path =  hydseting.password_dict_path, port = port, proto = proto)
		#hydra.restore(hydseting.restore + 'hydra.restore')
	
info = Information('http://www.csdn.net')
exp = Exploit('test', info = info)
exp.network()
exp.application()
"""
masscan = MasscanRest()
scan_dict = masscan.scan('111.202.114.53', maseting.QUICK_SCAN, 'airtel.com')
print masscan.export_json(scan_dict['name'])
print 
print 
print masscan.select_history(group_id=scan_dict['group_id'])
"""
from lib.core.settings import wvseting

hydra = Hydra()
#hydra.start(target = '127.0.0.1', user_dict_path = hydseting.user_dict_path, password_dict_path =  hydseting.password_dict_path, proto = 'ssh')
#hydra.restore(hydseting.restore + 'hydra.restore')
#info = Information('http://zfzhandian.com')
#targets = info.domain_collect()
#print info.network_scan(targets)
#targets = info.domain_collect()
#wvscan = WvsScan(wvseting.api_key, 'https://10.102.16.196:3443/', None )
#wvscan.scan(group_name = 'tegfsddvj')
#wvscan.stop()
#wvscan.set_group('test')
#wvscan.del_group()
#wvscan.clean_targets()
#wvscan.add_targets_to_group();
#https://10.102.16.196:3443/api/v1/scans?c=0
#https://10.102.16.196:3443/api/v1/scans
#print wvscan.get_scans()
#print wvscan.get_current_scans()
#print wvscan.get_current_targets()
#wvscan.stop()
#wvscan.clean_scans()

POLICIE_COMPLEX = 'complex'
access = '9ce1ca30eb7ec4511af9c29cb74e96cd35a7dc400439459599454d079a176f3d'
secret = 'b289fedbb80c0a405609b7493299ebf3235b9cb847554807afdbe00e654d2f29'
base_url = 'https://10.102.16.196:8834/'
targets = ['127.0.0.1', '10.102.16.196', '10.102.16.197', '10.102.16.198', '192.168.230.140']
formats = ['ftp','ssh', 'www']
scan_name = 'test'
#plugin_id
SERVICE_DETECTION = 22964

#nessus = NessusRest(access, secret, base_url)
#scan_id = 112
#print nessus.templates('policy')
#print nessus.scan("731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65", 'testone', '127.0.0.1', policy_id = 11, folder_id = 4, description = 'test')
#print nessus.policies(POLICIE_COMPLEX)
#print nessus.folders('test')
#print nessus.start_scan(17)
#print nessus.list_scan(4)
#print nessus.status_scan(9)
#msg = nessus.create_folder('test')
#print nessus.getError(msg)
#print nessus.del_folder(4)
"""
file_id = nessus.file_id_scan(9)['file']
print file_id
while nessus.export_status(scan_id, file_id):
	time.sleep(0.3)
nessus.download_export(scan_id,file_id)"""
#print nessus.status_scan(scan_id)
#print nessus.details(scan_id)

"""
nesscan = NessusScan(access, secret, base_url)
nesscan.set_text_targets(targets)
nesscan.set_template(nesscan.BASIC_NETWORK_SCAN)
#complex 自定义的扫描策略
#nesscan.set_policy('complex')
nesscan.scan(scan_name)
print nesscan.is_running()
nesscan.pause()
nesscan.resume()
nesscan.stop()
print nesscan.is_running()
print nesscan.get_folders()
id = nesscan.create_folder('test')['id']
nesscan.del_floder(id = id)
#nesscan.scan_id = 145
print nesscan.get_scan_history()
print nesscan.get_vulnerabilities()
print nesscan.get_vulnerabilitie_info(SERVICE_DETECTION)
"""
