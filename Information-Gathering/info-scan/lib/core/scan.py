#! usr/bin/python 
#coding=utf-8 
import os

import hashlib

from lib.core.log import logger
from lib.utils.common import read
from lib.utils.common import list_dir_nohidden
from lib.utils.common import chk_file
from lib.core.settings import masscan_path
from lib.core.settings import masscan_report_path
from lib.core.settings import masscan_shell
from lib.core.settings import masscan_report_map_path


class Nessus():
	def scan(self):
		print "nessus scan"
	
class Wvs():
	def scan(self):
		print "wvs scan"

#检查map文件 不存在则创建
chk_file(masscan_report_map_path)
class Masscan():
	
	def __init__(self):
		self.ip = None
		self.port = None
		self.adapter_ip = None
		self.token_list = []
		self.report_history = []

	#def config(self, ):
	
	def get_tokens(self):
		return self.token_list
		
	def get_history_tokens(self):
		dir_list = list_dir_nohidden(masscan_report_path)
		if dir_list:
			self.report_history = []
			self.report_history.extend(dir_list)
		return self.report_history
		
	def map(self):
		return {'ip': [], 'ports':[], 'report':[]}
	
	def token(self, key):
		m2 = hashlib.md5()
		m2.update(key)
		return m2.hexdigest()

	def get_report_path(self, token):
		return "%s%s.json"%(masscan_report_path, token)

	#TODO --adapter-ip 
	def scan(self, ip, ports):
		token = self.token(ip + ports)
		self.token_list.append(token)
		currten_report_path = "%s%s.json"%(masscan_report_path, token)
		scan_shell = masscan_shell%(masscan_path, ip, ports, currten_report_path)
		output = os.popen(scan_shell)
		return token
		
	def report_json(self, token):
		return read(self.get_report_path(token))
