#! usr/bin/python 
#coding=utf-8 
import os
import time
import ssl
import json

import hashlib
from nessrest import ness6rest

from lib.core.log import logger
from lib.utils.common import read
from lib.utils.common import list_dir_nohidden
from lib.core.settings import maseting
from lib.core.settings import neseting
from lib.core import settings
from lib.utils.common import write
from lib.connection.http import Request

class Nessus():
	templates_arry = ['PCI Quarterly External Scan', 'Host Discovery', 'WannaCry Ransomware', 'Intel AMT Security Bypass', 'Basic Network Scan', 'Credentialed Patch Audit', 'Web Application Tests', 'Malware Scan', 'Mobile Device Scan', 'MDM Config Audit', 'Policy Compliance Auditing', 'Internal PCI Network Scan', 'Offline Config Audit', 'Audit Cloud Infrastructure', 'SCAP and OVAL Auditing', 'Bash Shellshock Detection', 'GHOST (glibc) Detection', 'DROWN Detection', 'Badlock Detection', 'Shadow Brokers Scan', 'Advanced Scan']
	lanch = ['ON_DEMAND', 'DAILY', 'WEEKLY,' 'MONTHLY', 'YEARLY']
	def __init__(self):
		self.template = None
		self.context = ssl._create_unverified_context()
		self.headers = {'X-ApiKeys': 'accessKey=' + neseting.access +'; secretKey=' + neseting.secret}
		self.request = Request(headers = self.headers, context = self.context)
		
	def folders(self, folder = None):
		url = neseting.base_url + 'scans'
		flods = self.action(url)
		if flods and folder:
			for f in flods['folders']:
				if not cmp(folder, f['name']):
					return f
		else:
			return flods
		
	def templates(self, type, template = None):
		url = neseting.base_url + 'editor/' + type + '/templates'
		tems = self.action(url)
		if tems and template:
			for t in tems['templates']:
				if not cmp(template, t['title']):
					return t
		else:
			return tems
		
	def action(self, url, data = None, method = 'GET', content = ''):
		self.request.headers[settings.CONTENT_TYPE] = content
		if not cmp(method, 'POST'):
			response = self.request.post(url, data)
		else:
			response = self.request.get(url)
		result = self.request.read(response)
		if result:
			return json.loads(result)
	
	def scan(self):
		pass
	
	def policies(self, policie = None):
		url = neseting.base_url + 'policies'
		policies = self.action(url)
		if policie and policies:
			for p in policies['policies']:
				if not cmp(policie, p['name']):
					return p
		else:
			return policies
	
	def list_scan(self, folder_id = None, date = None):
		url = neseting.base_url + 'scans'
		#TODO 增加date过滤
		if folder_id:
			url += '?folder_id=' + str(folder_id)
		return self.action(url)
	
	def create_scan(self, uuid, name, targets, enabled = 'false', policy_id = None, folder_id = None, description = None, launch = None):
		url = neseting.base_url + 'scans'
		data = {
		"uuid": uuid,
		"settings": {
			"name": name,
			"enabled": enabled,
			"text_targets": targets
			}
		}
		if policy_id:
			data['settings']['policy_id'] = policy_id
		if folder_id:
			data['settings']['folder_id'] = folder_id
		if description:
			data['settings']['description'] = description 
		if launch:
			data['settings']['launch'] = launch
			
		return self.action(url, data, method = 'POST', content = "application/json")
	def start_scan(self, scan_id):
		url = neseting.base_url + 'scans/%s/launch'%scan_id
		#print self.action(url)

class Wvs():
	def scan(self):
		print "wvs scan"

class BloblastGroupExistException(Exception):
    pass
		
class Masscan():
	
	def __init__(self):
		self.adapter_ip = None
		self.history = self.__historys(maseting.ALL_HISTORY)
		self.group = self.__groups(maseting.ALL_GROUP)
	"""

	历史

	"""
	
	#name （masscan 报告文件名 唯一不可重复） token （ip + port md5值，查询扫描历史纪录） target （扫描参数）time （扫描时间） group （分组 探测不同ip段但同属于一个目标的标记）
	# push {'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}, 'group':''}\n name 不可重复
	def __push_map(self, ip, port, name, group):
		history = maseting.history_format%(name, self.token(ip, port), ip, port, time.time(), group)
		maseting.map_handle.write(history)
		#更新到历史纪录中
		self.update_history(history)
		maseting.map_handle.flush()
		return eval(history)
	
	#line 返回的行数 line等于-1时返回所有历史纪录
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
	
	#获取历史纪录 默认获取100条
	#return  {'history':[{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n,...],'count':0}
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
	
	#更新历史纪录
	def update_history(self, map_text):
		self.history['history'].append(eval(map_text))
		self.history['count'] += 1

	#筛选历史纪录
	#return  {'history':[{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}}\n,...],'count':0}
	def select_history(self, token = None, name = None, ip = None, group_id = None, time = None):
		history = {'history':[], 'count':0}
		if token:
			for h in self.history['history']:
				if not cmp(h['scan']['token'],token):
					history['history'].append(h)
					history['count'] += 1
		elif name:
			for h in self.history['history']:
				if not cmp(h['name'],name):
					history['history'].append(h)
					history['count'] += 1
		elif ip:
			for h in self.history['history']:
				if not cmp(h['scan']['target']['ip'], ip):
					history['history'].append(h)
					history['count'] += 1
		elif group_id:
			#查询同分组的扫描记录
			group = self.select_group(id = group_id)
			for g in self.history['history']:
				if not cmp(g['group_id'], group_id):
					history['history'].append(g)
					history['count'] += 1
		else:
			history = None
		return history
	"""
	分组
	"""

	#添加分组 不存在创建
	#add {'id':id, 'group':'', 'time':0}
	def __push_group(self, group):
		group = maseting.group_format%(self.md5(group.join(str(time.time()))), group, time.time())
		maseting.group_handle.write(group)
		#更新分组
		self.update_group(group)
		maseting.group_handle.flush()
		return eval(group)
	
	def __pop_group(self, line = 100):
		#重置文件指针到文件头
		if maseting.group_handle.tell():
			maseting.group_handle.seek(0)
		group_arry = []
		if line > 0:
			group_arry.extend(maseting.group_handle.readlines(line))
		elif line is maseting.ALL_HISTORY:
			line = 10000
			while True:
				lines = maseting.group_handle.readlines(line)
				if not lines:
					break
				group_arry.extend(lines)
		return group_arry

	#获取历史纪录 默认获取100条
	def __groups(self, line = 100):
		group = {'group':[], 'count':0}
		lines = self.__pop_group(line)
		group['count'] = len(lines)
		for i in range(0, group['count']):
			try:
				group['group'].append(eval(lines[i]))
			except exception, e:
				pass
		return group
	
	#更新分组
	def update_group(self, group):
		self.group['group'].append(eval(group))
		self.group['count'] += 1

	#筛选分组
	def select_group(self, name = None, id = None):
		group = {'group':{}}
		if name:
			for g in self.group['group']:
				if not cmp(g['name'], name):
					group['group'].update(g)
		elif id:
			for g in self.group['group']:
				if not cmp(g['id'], id):
					group['group'].update(g)
		else:
			group = None 
		return group

	"""

	扫描

	"""
	
	def md5(self, key):
		m2 = hashlib.md5()
		m2.update(key)
		return m2.hexdigest()
		
	def token(self, ip, port):
		return self.md5(ip.join(port))

	#TODO --adapter-ip 
	def scan(self, ip, port, group_name = None):
		name = self.md5("%s%s%s"%(ip, port, str(time.time())))
		group_id = ''
		currten_report_path = "%s%s.json"%(maseting.masscan_report_path, name)
		scan_shell = maseting.masscan_shell%(maseting.masscan_path, ip, port, currten_report_path)
		output = os.popen(scan_shell)
		if group_name:
			group = self.select_group(name=group_name)
			if group['group']:
				group_id = group['group']['id']
			else:
				group_id = self.__push_group(group_name)['id']
		if name:
			return self.__push_map(ip, port, name, group_id)
		
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