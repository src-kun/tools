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
		return [u'so.csdn.net', u'server.csdn.net', u'letter.csdn.net', u'special.csdn.net', u'xamarin.csdn.net', u'photo.csdncms.csdn.net', u'database.csdn.net', u'vuforia.csdn.net', u'geek.csdn.net', u'biz.csdn.net', u'space.csdncms.csdn.net', u'tencent_qcloud.csdn.net', u'con2.csdn.net', u'ibm.csdn.net', u'ea.csdn.net', u'ems.csdn.net', u'talk.csdncms.csdn.net', u'www.csdncms.csdn.net', u'subject.csdn.net', u'aws.csdn.net', u'articles.csdn.net', u'hadoop.csdn.net', u'club.csdn.net', u'bss.csdn.net', u'lib.csdn.net', u'cto.csdn.net', u'job.csdn.net', u'order.csdn.net', u'student.csdn.net', u'mailfeed.csdn.net', u'write.blog.csdn.net', u'cloud.csdn.net', u'storage.csdn.net', u'docker.csdn.net', u'Atlassian.csdn.net', u'atlassian.csdn.net', u'bbs.csdn.net', u'msdn.csdn.net', u'mall.csdn.net', u'huiyi.csdn.net', u'api.csdn.net', u'powerlinux.csdn.net', u'primeton.csdn.net', u'app.csdncms.csdn.net', u'g.csdn.net', u'hardware.csdn.net', u'special.csdncms.csdn.net', u'sd.csdn.net', u'visualstudio2017.csdn.net', u'ibmuniversity.csdn.net', u'video.csdncms.csdn.net', u'download.csdn.net', u'programmer.csdn.net', u'openstack.csdn.net', u'qcloud.csdn.net', u'my.csdn.net', u'wiki.csdn.net', u'news.csdn.net', u'edu.csdn.net', u'code.csdn.net', u'cie.csdn.net', u'qualcomm.csdn.net', u'blog.csdn.net', u'newsletter.csdn.net', u'passport.csdn.net', u'hc.csdn.net', u'ask.csdn.net', u'security.csdn.net', u'intel.csdn.net', u'msg.csdn.net', u'huawei.csdn.net', u'mobile.csdn.net', 'www.csdn.net', u'events.csdn.net']
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
	
	def application_scan(self, url, description = ''):
		wvs = Wvs()
		#未写描述时，默认使用mark作为描述
		if not description:
			description = self.mark
		msg = wvs.add_target(url, description = description)
		
		if not wvs.getError(msg):
			infoMsg = "add target {%s} success"%url
			logger.info(infoMsg)
			#msg = wvs.start_scan(msg['target_id'])
			#infoMsg = "start scan target {%s} success"%url
			#logger.info(infoMsg)
		else:
			warnMsg = "add target {%s} %s ! "%(url, msg)
			logger.warn(warnMsg)
			msg = None
		return msg
		
	def clean_scans():
		pass
	
	#confirm = True 时需要确认是否删除targets
	def clean_targets(self, group_name = None, confirm = True):
		
		if confirm:
			msg = 'Are you sure you want to clean targets? (Y/N) :'
			if not cmp(input(msg).lower(), 'y'):
				logger.info('Are you sure you want to clean targets? (Y/N) :Y')
			else:
				logger.info('Are you sure you want to clean targets? (Y/N) :N')
				return
				
		if group_name:
			#删除一个分组的target
			targets = wvs.search_target(group_name)['targets']
		else:
			#删除全部target
			targets = wvs.list_targets()['targets']
		
		#开始删除
		for target in targets:
			wvs.del_target(target['target_id'])
			logger.info('del target {%s} success'%target['address'])
		
		return targets
	
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
"""
scan_status = nessus.details_scan(25)['history'][0]['status']
while cmp(scan_status,'completed'):
	time.sleep(3)
	print scan_status
"""
wvs = Wvs()
#print wvs.add_target('http://www.q28.me/')
#print wvs.start_scan('f334a59b-b179-4439-b0bf-ac41e23e2d7f')
#print wvs.type_scan()
#print wvs.list_targets()
#print wvs.del_target('820d6a15-c555-4411-ba00-03fe82ce3811')
#print wvs.list_scans()
#print wvs.del_scan('0a6f24d7-b6be-422e-a4d2-8795b77b3ec4')
#print wvs.search_target('csdn.net')
#print wvs.create_group_target('test')
#print wvs.del_group_target('008ba33b-af79-4ffb-aba5-6ab78bb47aac')
#print wvs.list_groups_target()
#print wvs.search_scans('cd9f576f-11cb-40ad-8692-e4b3d5271c79')
hydra = Hydra()
#hydra.start(target = '127.0.0.1', user_dict_path = hydseting.user_dict_path, password_dict_path =  hydseting.password_dict_path, proto = 'ssh')
#hydra.restore(hydseting.restore + 'hydra.restore')
info = Information('http://www.csdn.net/')
#targets = ','.join(info.domain_collect())
#print info.network_scan(targets)
targets = info.domain_collect()
for target in targets:
	info.application_scan(target)
info.clean_targets('test')