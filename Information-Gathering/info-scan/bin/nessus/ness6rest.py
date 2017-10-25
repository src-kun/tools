#! usr/bin/python 
#coding=utf-8 

import json

from log import logger
from http import Request
from settings import neseting
import ssl

class NessusRest():
	
	CONTENT_JSON = {'Content-Type':'application/json'}
	
	def __init__(self, accessKey, secretKey):
		self.template = None
		self.context = ssl._create_unverified_context()
		self.__headers = {'X-ApiKeys': 'accessKey=' + accessKey +'; secretKey=' + secretKey}
		self.__request = Request(headers = self.__headers, context = self.context)
	
	#获取文件夹信息
	def folders(self):
		url = neseting.base_url + 'folders'
		return self.action(url)
	
	#创建文件夹
	def create_folder(self, folder_name):
		url = neseting.base_url + 'folders'
		data = {"name":folder_name}
		return self.action(url, data = data, method = 'POST', content = self.CONTENT_JSON)
		
	#删除文件夹
	def del_folder(self, folder_id):
		url = neseting.base_url + 'folders/%d'%folder_id
		return self.action(url, method = 'DELETE')
	
	#获取模板
	def templates(self, type):
		url = neseting.base_url + 'editor/' + type + '/templates'
		return self.action(url)
	
	#获取自定义的策略
	def policies(self):
		url = neseting.base_url + 'policies'
		return self.action(url)
	
	#获取folder_id文件夹内扫描任务
	#TODO 增加时间过滤
	def list_scan(self, folder_id = None):
		url = neseting.base_url + 'scans'
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
		url = neseting.base_url + 'scans'
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
			
		return self.action(url, data, method = 'POST', content = self.CONTENT_JSON)
	
	#开始扫描
	def start(self, scan_id):
		url = neseting.base_url + 'scans/%d/launch'%(scan_id)
		return self.action(url, method = 'POST')
	
	#暂停
	def pause(self, scan_id):
		url = neseting.base_url + 'scans/%d/pause'%(scan_id)
		return self.action(url, method = 'POST')
	
	#继续
	def resume(self, scan_id):
		url = neseting.base_url + 'scans/%d/resume'%(scan_id)
		return self.action(url, method = 'POST')
	
	#停止扫描
	def stop(self, scan_id):
		url = neseting.base_url + 'scans/%d/stop'%(scan_id)
		return self.action(url, method = 'POST')
	
	#无返回值
	def status(self, scan_id, read = True):
		url = neseting.base_url + 'scans/%d/status'%(scan_id)
		return self.action(url, {"read":read}, method = 'PUT', content = self.CONTENT_JSON)
	
	#获取扫描任务、漏洞、描述、历史扫描记录
	def details(self, scan_id, history_id = None):
		url = neseting.base_url + 'scans/%d'%(scan_id)
		if history_id:
			url += '?history_id=%d'%history_id
		return self.action(url)

	#通知nessus生成报告
	#return {u'token': u'c8f9425c44306088a383ed7045ceb346c10de51bbc8edd4428c15024b7d20c0c', u'file': 2056893300}
	def export_request(self, scan_id, format):
		url =  neseting.base_url + 'scans/%d/export'%(scan_id)
		values = {"format":format,"filter.search_type":"and"}
		return self.action(url, values, method = 'POST', content = self.CONTENT_JSON) 
	
	#查看报告是否可以下载，生成报告有延迟，首先需要判断是否可以下载
	#return 0 可以下载
	def export_status(self, scan_id, file_id):
		url =  neseting.base_url + 'scans/%d/export/%d/status'%(scan_id, file_id)
		return self.action(url)
	
	#TODO 获取删除记录
	def export_history(self, scan_id):
		pass
		
	#TODO 下载pdf失败
	def download_export(self, scan_id, file_id, path, name, format):
		url =  neseting.base_url + 'scans/%d/export/%d/download'%(scan_id, file_id)
		data = self.action(url, method = 'GET', content = self.CONTENT_JSON, download = True) 
		with open('%s%s.%s'%(path, name, format), 'wb') as code:     
			code.write(data)
			
	def vuln_info():
		pass
		
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