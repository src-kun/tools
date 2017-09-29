#! usr/bin/python 
#coding=utf-8 
import os
import time

import hashlib

from lib.core.log import logger
from lib.utils.common import read
from lib.utils.common import list_dir_nohidden
from lib.core.settings import maseting
from lib.utils.common import write

class Nessus():
	def scan(self):
		print "nessus scan"
	
class Wvs():
	def scan(self):
		print "wvs scan"

class Masscan():
	
	def __init__(self):
		self.adapter_ip = None
		self.history = self.__historys(maseting.ALL_HISTORY)
	"""

	历史

	"""
	#line 返回的行数 等于-1时返回所有历史纪录
	#return ["{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n",...]
	def __pop_map(self, line):
		#重置文件指针到文件头
		if maseting.map_handle.tell():
			maseting.map_handle.seek(0)
		map_arry = []
		if line > 0:
			map_arry.extend(maseting.map_handle.readlines(line))
		elif line is maseting.ALL_HISTORY:
			line = 10000
			while True:
				lines = maseting.map_handle.readlines(line)
				if not lines:
					break
				map_arry.extend(lines)
		return map_arry
	
	#{'history':[{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n,...],'count':0}
	def __historys(self, line = 100):
		history = {'history':[], 'count':0}
		lines = self.__pop_map(line)
		history['count'] = len(lines)
		for i in range(0, history['count']):
			try:
				history['history'].append(eval(lines[i]))
			except exception, e:
				pass
		return history
		
	def update_history(self, map_text):
		self.history['count'] += 1
		self.history['history'].append(eval(map_text))
	
	#TODO 筛选历史纪录
	def select_history(self, token):
		pass

	"""

	扫描

	"""	
	
	#{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n name 不可重复
	def __push_map(self, ip, port, name):
		map_text = "{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n"%(name, self.token(ip, port), ip, port, time.time())
		maseting.map_handle.write(map_text)
		#更新到历史纪录中
		self.update_history(map_text)
		maseting.map_handle.flush()
	
	def md5(self, key):
		m2 = hashlib.md5()
		m2.update(key)
		return m2.hexdigest()
		
	def token(self, ip, port):
		return self.md5(ip.join(port))

	#TODO --adapter-ip 
	def scan(self, ip, port):
		name = self.md5("%s%s%s"%(ip, port, str(time.time())))
		currten_report_path = "%s%s.json"%(maseting.masscan_report_path, name)
		scan_shell = maseting.masscan_shell%(maseting.masscan_path, ip, port, currten_report_path)
		output = os.popen(scan_shell)
		if name:
			self.__push_map(ip, port, name)
		return name
	"""

	报告

	"""
	def __report_path(self, name):
		return "%s%s.json"%(maseting.masscan_report_path, name)

	#return [{"ip": "111.202.114.53","timestamp": "1506482040", "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128}]},...]
	def report_json(self, name):
		report_dict = {'reports':[],'count':0}
		report_arry = read(self.__report_path(name))
		report_dict['count'] = len(report_arry)
		for i in range(0, report_dict['count']):
			try:
				report_dict['reports'].append(eval(report_arry[i]))
			except Exception, e:
				pass
		return report_dict