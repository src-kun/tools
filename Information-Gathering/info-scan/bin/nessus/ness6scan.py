#! usr/bin/python 
#coding=utf-8

import time
from log import logger
from ness6rest import NessusRest

class NessusScan():
	
	#模板列表
	SCAN_TEMPLATES = ['PCI Quarterly External Scan', 'Host Discovery', 'WannaCry Ransomware', 'Intel AMT Security Bypass', 'Basic Network Scan', 'Credentialed Patch Audit', 'Web Application Tests', 'Malware Scan', 'Mobile Device Scan', 'MDM Config Audit', 'Policy Compliance Auditing', 'Internal PCI Network Scan', 'Offline Config Audit', 'Audit Cloud Infrastructure', 'SCAP and OVAL Auditing', 'Bash Shellshock Detection', 'GHOST (glibc) Detection', 'DROWN Detection', 'Badlock Detection', 'Shadow Brokers Scan', 'Advanced Scan']
	#network扫描模板
	BASIC_NETWORK_SCAN = 4
	#扫描周期
	lanch = ['ON_DEMAND', 'DAILY', 'WEEKLY,' 'MONTHLY', 'YEARLY']
	#Nessus 下载
	DOWNLOAD_NESSUS = 0
	#下载格式
	DOWNLOAD_FORMAT = ['nessus','csv','db','html','pdf']
	
	def __init__(self, name, 
					accessKey, 
					secretKey, 
					nescan = None):
		if nescan:
			self.__nescan = nescan
		else:
			self.__nescan = NessusRest(accessKey = accessKey, 
										secretKey = secretKey)
		self.info = None
		self.folders = None
		self.name = name
		self.scan_id = ''
		self.uuid = ''
		self.category = ''
		self.settings = {'launch':'ONETIME',
							'enabled':False,
							'launch_now':True,
							'text_targets':'',
							'file_targets':'',
							'folder_id':None}
		self.download = {'format': self.DOWNLOAD_FORMAT[self.DOWNLOAD_NESSUS],
						'path':'',
						'name':'',
						'file_id':None,
						'status':False
						}
	
	#设置扫描目标
	def set_text_targets(self, targets):
		if type(targets) == list:
			self.settings['text_targets'] = ','.join(targets)
		else:
			self.settings['text_targets'] = targets
	
	#TODO
	def set_file_targets(self, targets):
		pass
	
	#name 不存在返回None
	#设置模板uuid
	def set_template(self, name = None, uuid = None):
		if name:
			template = self.getScanPolicyTemplateByName(name)
			try:
				self.settings['template_uuid'] = template['uuid']
			except KeyError:
				warnMsg = 'template name {%s} is not defined'%name
				logger.warn(warnMsg)
			return template
		self.settings['template_uuid'] = uuid
	
	#name 不存在返回None
	#设置扫描策略
	def set_policy(self, name = None, id = None):
		if name:
			policie = self.getPoliciesTemplateByName(name)
			try:
				self.settings['policy_id'] = policie['id']
			except KeyError:
				warnMsg = 'policy name {%s} is not defined'%name
				logger.warn(warnMsg)
			return policie
		self.settings['policy_id'] = id
	
	#name 不存在返回None
	#设置扫描保存文件夹
	def set_folder(self, name = None, id = None):
		if name:
			folder = self.getFolderByName(name)
			try:
				self.settings['folder_id'] = folder['id']
			except KeyError:
				warnMsg = 'folder name {%s} is not defined'%name
				logger.warn(warnMsg)
			return folder
		self.settings['folder_id'] = id
	
	#scan_type SCAN_TEMPLATES的下标
	#获取系统扫描策略模板信息
	def getScanPolicyTemplateByName(self, template_name_index):
		template_name =  self.SCAN_TEMPLATES[template_name_index]
		templates = self.__nescan.templates('policy') 
		for template in templates['templates']:
			if not cmp(template_name, template['title']):
				return template
	
	#获取自定义的扫描模板 policies
	def getPoliciesTemplateByName(self, name):
		policies = self.__nescan.policies()
		for policie in policies['policies']:
			if not cmp(name, policie['name']):
				return policie
	
	#根据文件夹名获取文件夹 id
	def getFolderByName(self, name):
		folders = self.get_folders()
		for folder in folders['folders']:
			if not cmp(name, folder['name']):
				#{u'name': u'test', u'custom': 1, u'unread_count': 1, u'default_tag': 0, u'type': u'custom', u'id': 4}
				return folder
	
	#launch_now is True 马上开始扫描
	def scan(self, description = ''):
		scan = self.__nescan.scan(template_uuid = self.settings['template_uuid'], 
									scan_name = self.name, 
									targets = self.settings['text_targets'], 
									policy_id = self.settings['policy_id'], 
									folder_id = self.settings['folder_id'], 
									description = description)
		
		if scan and self.settings['launch_now']:
			self.scan_id = scan['scan']['id']
			self.start()
		
		return scan
		
	#开始扫描
	def start(self):
		scan = self.__nescan.start(self.scan_id)
		if self.getError(scan):
			warnMsg = 'create scan_id {%d} faild : %s'%(scan_id, self.getError(scan))
			logger.warn(warnMsg)
			return
		return scan
	
	def stop(self):
		return self.__nescan.stop(self.scan_id)
	
	def pause(self):
		return self.__nescan.pause(self.scan_id)
		
	def resume(self):
		return self.__nescan.resume(self.scan_id)
	
	def get_scan_info(self):
		details = self.__nescan.details(self.scan_id)
		if 'info' in details:
			self.info = details['info']
		
	def is_running(self):
		self.get_scan_info()
		return self.info['status'] == 'running'

	def is_completed(self):
		self.get_scan_info()
		return self.info['status'] == 'completed'
	
	def list_scans(self, folder_name = None):
		list = None
		folder = self.getFolderByName(folder_name)
		if folder:
			list = self.__nescan.list_scan(folder['id'])
			if self.getError(list):
				warnMsg = 'list scan faild : %s'%self.getError(list)
				logger.warn(warnMsg)
				return
		else:
			warnMsg = 'folder name {%s} is not defined'%folder_name
			logger.warn(warnMsg)
		return list

	def delete(self):
		pass
	
	#获取文件夹信息
	def get_folders(self):
		folders = self.__nescan.folders()
		if self.getError(folders):
			warnMsg = 'get folders faild : %s'%self.getError(folders)
			logger.warn(warnMsg)
			return
		self.folders = folders
		return folders
	
	def create_folder(self, name):
		folder = self.__nescan.create_folder(name)
		if self.getError(folder):
			warnMsg = 'create folder {%s} faild : %s'%(name, self.getError(folder))
			logger.warn(warnMsg)
			return
		return folder
		
	def del_floder(self, folder_name = None, id = None):
		if folder_name:
			folder = self.getFolderByName(folder_name)
			if folder:
				id = folder['id']
		if id:
			self.__nescan.del_folder(id)
			return True
	
	def __get_file_id(self):
		self.download['file_id'] = self.__nescan.export_request(scan_id = self.scan_id, format = self.download['format'])['file']
		return self.download['file_id']
	
	def export_status(self):
		try:
			export = self.__nescan.export_status(scan_id = self.scan_id, file_id = self.download['file_id'])
			self.download['status'] = export['status'] == 'ready'
		except Exception, e:
			print e
			warnMsg = 'get export status faild : %s'%self.getError(export)
			logger.warn(warnMsg)
		
	#https://10.102.16.196:8834/scans/130/export/1989408344/download
	def download_export(self):
		if not self.download['file_id']:
			self.__get_file_id()
		
		while True:
			#等待nessus生成报告
			self.export_status()
			if self.download['status']:
				result = self.__nescan.download_export(scan_id = self.scan_id, 
												file_id = self.download['file_id'], 
												path = self.download['path'], 
												name = self.download['name'], 
												format = self.download['format'])
				break
			time.sleep(0.2)
			
	#{u'error': u'A valid policy ID must be provided.'}
	def getError(self, msg):
		if msg.has_key('error'):
			return msg['error']