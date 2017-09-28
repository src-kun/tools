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
		self.token_list = []
		self.report_history = []

	#def config(self, ):
	
	def get_tokens(self):
		return self.token_list
		
	def history(self):
		dir_list = list_dir_nohidden(maseting.masscan_report_path)
		if dir_list:
			self.report_history = []
			self.report_history.extend(dir_list)
		return self.report_history
		
	def history2(self):
		self.__pop_map()
	
	#return {'map':[{'ip': [], 'ports':[], 'report':[]}], count:0}
	def __pop_map(self):
		pass

	#{'id':'%s','scan':{'token':'%s','target':{'%s':'%s'}},'time':%s}\n id 不可重复
	def __push_map(self, ip, port, token):
		id = self.md5(ip.join(str(time.time())))
		text = "{'id':'%s','scan':{'token':'%s','target':{'%s':'%s'}},'time':%s}\n"%(id, token, ip, port, time.time())
		maseting.map_handle.write(text)
	
	def md5(self, key):
		m2 = hashlib.md5()
		m2.update(key)
		return m2.hexdigest()

	#TODO --adapter-ip 
	def scan(self, ip, ports):
		token = self.md5(ip.join(ports))
		self.token_list.append(token)
		currten_report_path = "%s%s.json"%(maseting.masscan_report_path, token)
		scan_shell = maseting.masscan_shell%(maseting.masscan_path, ip, ports, currten_report_path)
		output = os.popen(scan_shell)
		if token:
			self.__push_map(ip, ports, token)
		return token

	def __report_path(self, token):
		return "%s%s.json"%(maseting.masscan_report_path, token)

	#return [{"ip": "111.202.114.53","timestamp": "1506482040", "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128}]},...]
	def report_json(self, token):
		return read(self.__report_path(token))