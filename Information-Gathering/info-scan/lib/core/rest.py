#! usr/bin/python 
#coding=utf-8 
import os
import time
import ssl
import json

import hashlib

from lib.core.log import logger
from lib.utils.common import read
from lib.utils.common import list_dir_nohidden
from lib.core.settings import maseting
from lib.core import settings
from lib.utils.common import write
from lib.connection.http import Request

class NessusRest():
	
	CONTENT_JSON = {'Content-Type':'application/json'}
	
	def __init__(self, accessKey, secretKey, base_url):
		self.base_url = base_url
		self.template = None
		self.context = ssl._create_unverified_context()
		self.__headers = {'X-ApiKeys': 'accessKey=' + accessKey +'; secretKey=' + secretKey}
		self.__request = Request(headers = self.__headers, context = self.context)
	
	#获取文件夹信息
	def folders(self):
		url = self.base_url + 'folders'
		return self.action(url)
	
	#创建文件夹
	def create_folder(self, folder_name):
		url = self.base_url + 'folders'
		data = {"name":folder_name}
		return self.action(url, data = data, method = 'POST', content = settings.CONTENT_JSON)
		
	#删除文件夹
	def del_folder(self, folder_id):
		url = self.base_url + 'folders/%d'%folder_id
		return self.action(url, method = 'DELETE')
	
	#获取模板
	def templates(self, type):
		url = self.base_url + 'editor/' + type + '/templates'
		return self.action(url)
	
	#获取自定义的策略
	def policies(self):
		url = self.base_url + 'policies'
		return self.action(url)
	
	#获取folder_id文件夹内扫描任务
	#TODO 增加时间过滤
	def list_scan(self, folder_id = None):
		url = self.base_url + 'scans'
		if folder_id:
			url += '?folder_id=' + str(folder_id)
		return self.action(url)
	
	#创建扫描
	def scan(self, template_uuid,  #系统扫描模板uuid
						scan_name, #扫描任务名称
						targets, #扫描目标
						policy_id = None, #自定义模板id
						folder_id = None, #文件夹id
						description = None, #注释信息
						enabled = 'false', #如果为true，则启用扫描时间表。
						launch = None #扫描周期
						):
		url = self.base_url + 'scans'
		data = {
		"uuid": template_uuid,
		"settings": {
			"name": scan_name,
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
			
		return self.action(url, data, method = 'POST', content = settings.CONTENT_JSON)
	
	#开始扫描
	def start(self, scan_id):
		url = self.base_url + 'scans/%d/launch'%(scan_id)
		return self.action(url, method = 'POST')
	
	#暂停
	def pause(self, scan_id):
		url = self.base_url + 'scans/%d/pause'%(scan_id)
		return self.action(url, method = 'POST')
	
	#继续
	def resume(self, scan_id):
		url = self.base_url + 'scans/%d/resume'%(scan_id)
		return self.action(url, method = 'POST')
	
	#停止扫描
	def stop(self, scan_id):
		url = self.base_url + 'scans/%d/stop'%(scan_id)
		return self.action(url, method = 'POST')
	
	#无返回值
	def status(self, scan_id, read = True):
		url = self.base_url + 'scans/%d/status'%(scan_id)
		return self.action(url, {"read":read}, method = 'PUT', content = settings.CONTENT_JSON)
	
	#获取扫描任务、漏洞、描述、历史扫描记录
	def details(self, scan_id, history_id = None):
		url = self.base_url + 'scans/%d'%(scan_id)
		if history_id:
			url += '?history_id=%d'%history_id
		return self.action(url)
		
	def vulnerabilitie_info(self, scan_id, plugin_id):
		url = self.base_url + 'scans/%d/plugins/%d'%(scan_id, plugin_id)
		return self.action(url)

	#通知nessus生成报告
	#return {u'token': u'c8f9425c44306088a383ed7045ceb346c10de51bbc8edd4428c15024b7d20c0c', u'file': 2056893300}
	def export_request(self, scan_id, format):
		url =  self.base_url + 'scans/%d/export'%(scan_id)
		values = {"format":format,"filter.search_type":"and"}
		return self.action(url, values, method = 'POST', content = settings.CONTENT_JSON) 
	
	#查看报告是否可以下载，生成报告有延迟，首先需要判断是否可以下载
	#return 0 可以下载
	def export_status(self, scan_id, file_id):
		url =  self.base_url + 'scans/%d/export/%d/status'%(scan_id, file_id)
		return self.action(url)
		
	#TODO 下载pdf失败
	def download_export(self, scan_id, file_id, path, name, format):
		url =  self.base_url + 'scans/%d/export/%d/download'%(scan_id, file_id)
		data = self.action(url, method = 'GET', content = settings.CONTENT_JSON, download = True) 
		with open('%s%s.%s'%(path, name, format), 'wb') as code:     
			code.write(data)
		
	def action(self, url, data = None, method = 'GET', content = {}, download = False):
		self.__request.headers.update(content)
		if not cmp(method, 'POST'):
			response = self.__request.post(url, data)
		elif not cmp(method, 'PUT'):
			response = self.__request.put(url, data)
		elif not cmp(method, 'GET'):
			response = self.__request.get(url)
		elif not cmp(method, 'DELETE'):
			response = self.__request.delete(url)
		
		result = self.__request.read(response)
		
		#清理添加的content
		if content:
			for key in content:
				del self.__request.headers[key]
		
		#TODO 支持二进制文件下载
		if download:
			return result

		if result:
			return json.loads(result)
		
class WvsRest():
	
	def __init__(self, api_key, base_url):
		self.base_url = base_url
		self.context = ssl._create_unverified_context()
		self.__headers = {'X-Auth':api_key}
		self.__request = Request(headers = self.__headers, context = self.context)

	#return {u'target_id': u'f334a59b-b179-4439-b0bf-ac41e23e2d7f', u'description': u'', u'criticality': 10, u'address': u'https://www.xxx.com/'}
	def add_target(self, target, description = '', criticality = 10):
		url = self.base_url + 'api/v1/targets'
		data = {'address':target,'description':description,"criticality":criticality}
		return self.action(url, data, 'POST', settings.CONTENT_JSON)
	
	#获取target信息
	#max_page 每页target最大个数
	#group_id 分组id
	def list_targets(self, previous_cursor = -1, query = None):
		url = self.base_url +  'api/v1/targets'
		
		#获取分组内从previous_cursor开始100条target
		if query and previous_cursor > 0:
			url += '?c=%d&q=%s'%(previous_cursor, query)
		#获取从previous_cursor开始100条记录
		elif previous_cursor:
			url += '?c=%d'%previous_cursor
		#filter
		elif query:
			url += '?q=%s'%query
		return self.action(url)
		
	#搜索target
	def search_target(self, text = None, group_id = None):
		url = self.base_url + 'api/v1/targets'
		if text:
			url += '?q=text_search:*' + text
		elif group_id:
			url += '?q=group_id:' + group_id
		return self.action(url)
	
	#删除target之后会删除对应的scan
	def del_target(self, target_id):
		url = self.base_url +  'api/v1/targets/' + target_id
		return self.action(url, method = 'DELETE')
	
	#添加target分组
	def create_group_target(self, group_name, description = ''):
		url = self.base_url +  'api/v1/target_groups'
		data = {'name':group_name, 'description': description}
		return self.action(url, data = data, method = 'POST', content = settings.CONTENT_JSON)
	
	#获取所有target分组
	#return {u'pagination': {u'previous_cursor': 0, u'next_cursor': None}, u'groups': [{u'group_id': u'cd9f576f-11cb-40ad-8692-e4b3d5271c79', u'description': u'', u'name': u'test', u'target_count': 1}]}
	def list_groups(self):
		url = self.base_url +  'api/v1/target_groups'
		groups = self.action(url)
		return groups
	
	#将target添加到某个分组
	#group_id 分组id
	#target_id target的id 类型：数组
	def add_targets_to_group(self, target_id, group_id):
		url = self.base_url +  'api/v1/target_groups/%s/targets'%group_id
		data = {'add':target_id,'remove':[]}
		return self.action(url, data, method = 'PATCH', content = settings.CONTENT_JSON)
		
	def del_group(self, group_id):
		url = self.base_url + 'api/v1/target_groups/' + group_id
		return self.action(url, method = 'DELETE')
	
	#?q=status:aborted
	#?q=group_id:4d6f4994-7036-4cb8-802f-fed6560e7034
	#?q=status:aborted;group_id:4d6f4994-7036-4cb8-802f-fed6560e7034
	#?c=100&?q=status:aborted;group_id:4d6f4994-7036-4cb8-802f-fed6560e7034
	def list_scans(self, scan_id = None, previous_cursor = -1, query = None):
		url = self.base_url +  'api/v1/scans'
		#过滤并获取从previous_cursor开始100个target
		if query and previous_cursor >= 0:
			url += '?c=%d&q=%s'%(previous_cursor, query)
		elif previous_cursor >= 0:
			url += '?c=%d'%previous_cursor
		#filter
		elif query:
			url += '?q=%s'%query
		
		return self.action(url)
		
	def search_scans(self, group_id):
		url = self.base_url +  '/api/v1/scans?q=group_id:' + group_id
		return self.action(url)
		
	def del_scan(self, scan_id):
		url = self.base_url +  'api/v1/scans/' + scan_id
		return self.action(url, method = 'DELETE')

	def type_scan(self):
		url = self.base_url + 'api/v1/scanning_profiles'
		return self.action(url)
	
	def stop(self, scan_id):
		url =  self.base_url + 'api/v1/scans/%s/abort'%scan_id
		return self.action(url, method = 'POST')
	
	#{u'ui_session_id': None, u'profile_id': u'11111111-1111-1111-1111-111111111111', u'target_id': u'f334a59b-b179-4439-b0bf-ac41e23e2d7f', u'schedule': {u'disable': False, u'time_sensitive': False, u'start_date': None}}
	def start_scan(self, target_id, 
						profile_id,
						disable = False,
						start_date = None,
						time_sensitive = False):
		url = self.base_url + 'api/v1/scans'
		data = {"target_id":target_id,"profile_id":profile_id,"schedule":{"disable":disable,"start_date":start_date,"time_sensitive":time_sensitive}}
		return self.action(url, data, 'POST', settings.CONTENT_JSON)
	
	def action(self, url, data = None, method = 'GET', content = {}, download = False):
		self.__request.headers.update(content)
		if not cmp(method, 'POST'):
			response = self.__request.post(url, data)
		elif not cmp(method, 'PUT'):
			response = self.__request.put(url, data)
		elif not cmp(method, 'GET'):
			response = self.__request.get(url)
		elif not cmp(method, 'DELETE'):
			response = self.__request.delete(url)
		elif not cmp(method, 'PATCH'):
			response = self.__request.patch(url, data)
			
		result = self.__request.read(response)
		
		#清理添加的content
		if content:
			for key in content:
				del self.__request.headers[key]
		
		#TODO 支持二进制文件下载
		if download:
			return result

		if result:
			return json.loads(result)
	
	#TODO wvs通知消息处理
	def notifications(self):
		pass #'api/v1/notifications/consume'
	
class BloblastGroupExistException(Exception):
    pass
		
class MasscanRest():
	
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
		currten_export_path = "%s%s.json"%(maseting.export_path, name)
		scan_shell = maseting.masscan_shell%(maseting.masscan_path, ip, port, currten_export_path)
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
	def __export_path(self, name):
		return "%s%s.json"%(maseting.export_path, name)

	#return [{"ip": "111.202.114.53","timestamp": "1506482040", "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128}]},...]
	def export_json(self, name):
		export_dict = {'exports':[],'count':0}
		export_arry = read(self.__export_path(name))
		export_dict['count'] = len(export_arry)
		for i in range(0, export_dict['count']):
			try:
				export_dict['exports'].append(eval(export_arry[i]))
			except Exception, e:
				pass
		return export_dict