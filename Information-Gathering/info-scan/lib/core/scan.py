#! usr/bin/python 
#coding=utf-8 

import time

from lib.core.rest import NessusRest
from lib.core.rest import WvsRest
from lib.core.log import logger
from lib.utils.common import input


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
	
	def __init__(self, 
					accessKey, 
					secretKey, 
					base_url,
					nescan = None):
		if nescan:
			self.__nescan = nescan
		else:
			self.__nescan = NessusRest(accessKey = accessKey, 
										secretKey = secretKey,
										base_url = base_url)
		self.info = None
		self.history = None
		self.vuln = None
		self.folders = None
		self.scan_id = ''
		self.uuid = ''
		self.category = ''
		self.settings = {
							'launch': 'ONETIME',
							'enabled': False,
							'launch_now': True,
							'targets':{
								'file':None,
								'text':''
							},
							'text_targets': '',
							'file_targets': '',
							'folder':{
										'id': None,
										'name': ''
							},
							'policy_id': None
						}
		self.download = {
							'format': self.DOWNLOAD_FORMAT[self.DOWNLOAD_NESSUS],
							'path':'',
							'name':'',
							'file_id':None,
							'status':False
						}
	
	#设置扫描目标
	def set_text_targets(self, targets):
		if type(targets) == list:
			self.settings['targets']['text'] = ','.join(targets)
		else:
			self.settings['targets']['text'] = targets
		
	
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
				self.settings['folder']['id'] = folder['id']
			except Exception,e:
				warnMsg = 'folder name {%s} is not defined'%name
				logger.warn(warnMsg)
			return folder
		self.settings['folder']['id'] = id
	
	def get_folder(self):
		return self.settings['folder']
	
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
	def scan(self, name, description = ''):
		infoMsg = '*'*19 + 'create scan' + '*'*19
		infoMsg += '\r\n%s'%self.settings['targets']['text']
		logger.info(infoMsg)
		infoMsg = '*'*50
		logger.info(infoMsg)
		scan = self.__nescan.scan(template_uuid = self.settings['template_uuid'], 
									scan_name = name, 
									targets = self.settings['targets']['text'], 
									policy_id = self.settings['policy_id'], 
									folder_id = self.settings['folder']['id'], 
									description = description)
		try:
			if scan and self.settings['launch_now']:
				self.scan_id = scan['scan']['id']
				self.start()
		except KeyError:
			warnMsg = 'create scan {%s} faild : %s'%(name, self.getError(scan))
			logger.warn(warnMsg)
			return
		
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
		if self.scan_id: 
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
			warnMsg = 'get export status faild : %s'%self.getError(export)
			logger.warn(warnMsg)
	
	def get_scan_history(self):
		try:
			detail = self.__nescan.details(scan_id = self.scan_id)
			self.history = detail['history']
		except Exception, e:
			warnMsg = 'get scan history faild : %s'%self.getError(detail)
			logger.warn(warnMsg)
		return self.history
	
	def get_vulnerabilities(self):
		try:
			detail = self.__nescan.details(scan_id = self.scan_id)
			self.vuln = detail['vulnerabilities']
		except Exception, e:
			warnMsg = 'get vulnerabilities faild : %s'%self.getError(detail)
			logger.warn(warnMsg)
		return self.vuln
		
	def get_vulnerabilitie_info(self, plugin_id):
		vulnerabilitie = self.__nescan.vulnerabilitie_info(scan_id = self.scan_id, plugin_id = plugin_id)
		if self.getError(vulnerabilitie):
			warnMsg = 'get vulnerabilitie info faild : %s'%self.getError(vulnerabilitie)
			logger.warn(warnMsg)
			return
		return vulnerabilitie
	
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
	

class WvsScan():
	#终止状态
	SCAN_STATUS_ABORT = 'aborted'
	#运行状态
	SCAN_STATUS_PROCESSING = 'processing'
	#等待状态
	SCAN_STATUS_QUEUED = 'queued'
	#完成状态
	SCAN_STATUS_COMPLETED = 'completed'
	#定时状态
	SCAN_STATUS_SCHEDULED = 'scheduled'
	#完全扫描
	FULL_SCAN = '11111111-1111-1111-1111-111111111111'
	
	def __init__(self, 
					api_key,
					base_url,
					targets = None):
		self.__wvsrest = WvsRest(api_key, base_url)
		self.target_id = None
		self.targets = []
		self.wvs = {
						'scans': [],
						'targets': [],
						'group': {
							'name': '',
							'id': None
						}
					}
		self.settings = {
							'launch_now': True,
							'profile_id': self.FULL_SCAN #扫描类型（快速扫描、完全扫描等...）编号
						}
							
		if targets:
			self.set_targets(targets)
	
	#url_arry 需要扫描的url数组
	#description 备注
	def set_targets(self, targets):
		if type(targets) == list:
			self.targets.extend(targets)
		else:
			self.targets.append(targets)
	
	#return {u'group_id': u'b66848f0fed647e29e2b1185d11fd60a', u'description': u'', u'name': u'group_name'}
	#创建分组
	def __create_group(self, name): 
		return self.__wvsrest.create_group_target(name)
		
	def del_group(self):
		return self.__wvsrest.del_group(self.wvs['group']['id'])
		
	#设置分组 不存在创建
	def set_group(self, name = None, id = None):
		if name:
			group = self.getGroupByName(name)
			if not group:
				group = self.__create_group(name)
			id = group['group_id']
			self.wvs['group']['name'] = name
		self.wvs['group']['id'] = id
		
	#return  {u'target_id': u'eefff2bc-b688-43df-855d-eb901c5f1352', u'description': u'', u'criticality': 10, u'address': u'www.y28.me'}
	#扫描
	def scan(self, group_name = None, group_id = None, description = ''):
		
		self.set_group( name = group_name, id = group_id)
		
		infoMsg = '*'*19 + 'add targets ' + '*'*19
		infoMsg += '\r\n%s'%self.targets
		logger.info(infoMsg)
		infoMsg = '*'*50
		logger.info(infoMsg)
		for address in self.targets:
			#添加到target
			target = self.__wvsrest.add_target(address, description = description)
			if self.getError(target):
				warnMsg = 'add target {%s} %s ! '%(address, self.getError(target))
				logger.warn(warnMsg)
			self.wvs['targets'].append(target)
		
		self.add_targets_to_group()
		
		if self.settings['launch_now']:
			scan = self.start()
		
		return self.wvs['targets']
	
	#将target添加到group_name分组
	def add_targets_to_group(self, group_id = None, targets_id_arry = None):
		
		if group_id:
			self.wvs['group']['id'] = group_id
		
		if not targets_id_arry:
			targets_id_arry = []
			for scan in self.wvs['targets']:
				targets_id_arry.append(scan['target_id'])
		
		result = self.__wvsrest.add_targets_to_group(targets_id_arry, self.wvs['group']['id'])
		if self.getError(result):
			warnMsg = 'add targets id {%s} to group {%s} faild : %s'%(targets_id_arry, group_id, self.getError(result))
			logger.warn(warnMsg)
		return result
	
	def getScanNameByTargetId(self, id):
		pass
	
	#启动扫描
	def start(self):
		for target in self.wvs['targets']:
			scan = self.__wvsrest.start_scan(target['target_id'], profile_id = self.settings['profile_id'])
			try:
				self.wvs['scans'].append(scan)
			except KeyError:
				warnMsg = 'start scan target {%s} faild : %s'%(target['address'], self.getError(scan))
				logger.warn(warnMsg)
		return self.wvs['scans']
	
	#根据分组名获取分组信息
	def getGroupByName(self, group_name):
		groups = self.__wvsrest.list_groups()
		
		if self.getError(groups):
			logger.info('get group {%s} faild : %s'%(group_name, self.getError(groups)))
			return
		
		for group in groups['groups']:
			if not cmp(group_name, group['name']):
				return group
	
	def get_current_scans(self, status = ''):
		if self.wvs['group']['name']:
			return self.get_scans(group_name = self.wvs['group']['name'], status = status)
	
	#获取scans
	def get_scans(self, group_name = None, group_id = None, status = ''):
		query = ''
		group = None
		scans = []
		previous_cursor = 0
		
		#filter 过滤状态为{status}的targets q=status:processing,completed
		if status:
			query += 'status:%s;'%status
		
		if group_id:
			query += 'group_id:%s;'%group_id
		elif group_name:
			group = self.getGroupByName(group_name)
			try:
				query += 'group_id:%s;'%group['group_id']
			except KeyError:
				pass
		
		while True:
			ret = self.__wvsrest.list_scans(previous_cursor = previous_cursor, query = query)
			try:
				previous_cursor += 100
				scans.extend(ret['scans'])
				if not ret['pagination']['next_cursor']:
					break
			except KeyError:
				break
		
		return scans
	
	#暂停扫描
	def stop(self):
		scans = []
		#防止scans添加延迟导致不能暂停任务
		while True:
			current_scans = self.get_current_scans(status = 'queued,processing,scheduled')
			for scan in current_scans:
				self.__wvsrest.stop(scan['scan_id'])
			if not scans:
				break
			scans.append(current_scans)
		return scans
	
	#清理扫描记录
	def clean_scans(self, group_name = None, group_id = None, status = None):
	
		if not group_name:
			group_name = self.wvs['group']['name']
			
		if not group_id:
			group_id = self.wvs['group']['id']
		
		scans = self.get_scans(group_name = self.wvs['group']['name'], group_id = self.wvs['group']['id'], status = status)
		
		#开始删除
		for scan in scans:
			self.__wvsrest.del_scan(scan['scan_id'])
		return scans
	
	#获取当前targets
	def get_current_targets(self, text = ''):
		group_name = self.wvs['group']['name']
		if group_name:
			return self.get_targets(group_name = group_name, text = text)
	
	#获取targets
	def get_targets(self, group_name = None, group_id = None, text = ''):
		previous_cursor = 0
		targets = []
		group = None
		query = ''
		
		#模糊搜索
		if text:
			query += 'text_search:*%s;'%text
		
		if group_id:
			query += 'group_id:%s'%group_id
		#获取group name对应的group id
		elif group_name:
			group = self.getGroupByName(group_name)
			#分组不存在
			if not group:
				return targets
			else:
				query += 'group_id:%s;'%group['group_id']
		
		#取出target
		#group_name != None 时取出group_name分组内所有target
		while True:
			ret = self.__wvsrest.list_targets(previous_cursor = previous_cursor, query = query)
			previous_cursor += 100
			targets.extend(ret['targets'])
			if not ret['pagination']['next_cursor']:
				break
		
		return targets
	
	#清除target
	#TODO 目前只能删除有分组的扫描任务
	def clean_targets(self, group_name = None, group_id = None, text = None):
	
		if not group_name and not group_id:
			targets = self.get_current_targets()
		else:
			targets = self.get_targets(group_name = self.wvs['group']['name'], group_id = self.wvs['group']['id'], text = text)
		
		if targets:
			#开始删除
			for target in targets:
				self.__wvsrest.del_target(target['target_id'])
				logger.info('del target {%s} success'%target['address'])
		
		return targets
		
	def clean_confirm(self, msg):
		keys = input(msg).lower()
		if not cmp(keys, 'y'):
			logger.info('%s Yes'%msg)
			return
		else:
			logger.info('%s No'%msg)
		return keys
	
	#{u'message': u'Feature not allowed', u'code': 1, u'details': None}
	def getError(self, msg):
		if msg and msg.has_key('message'):
			return msg['message']