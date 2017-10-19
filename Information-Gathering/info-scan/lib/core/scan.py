#! usr/bin/python 
#coding=utf-8 

from lib.core.rest import NessusRest
from lib.core.rest import NessusRest
from lib.core.rest import WvsRest
from lib.core.log import logger
from lib.utils.common import input
from lib.core.settings import wvseting

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
	FULL_SCAN = "11111111-1111-1111-1111-111111111111"
	
	def __init__(self, api_key):
		self.__wvsrest = WvsRest(api_key)
	
	#url_arry 需要扫描的url数组
	#description 备注
	#profile_id 扫描类型（快速、完全 等...）编号
	def scan(self, url_arry, profile_id, group_name = None ,description = '', launch_now = False):
		
		target_id_arry = []
		for url in url_arry:
			#添加到target
			target = self.__wvsrest.add_target(url, description = description)
			
			if not self.__wvsrest.getError(target):
				infoMsg = "add target {%s} success"%url
				logger.info(infoMsg)
				if launch_now:
					self.start(target_id = target['target_id'])
				target_id_arry.append(target['target_id'])
			else:
				warnMsg = "add target {%s} %s ! "%(url, target)
				logger.warn(warnMsg)
		
		if group_name:
			#检查分组不存在创建
			group = self.getGroupByName(group_name)
			if not group:
				group = self.create_group(group_name)
			#将启动的target添加到group_name分组
			self.__wvsrest.add_target_to_group(target_id_arry, group['group_id'])
		return target_id_arry
	
	#启动扫描
	def start(self, target_id, profile_id):
		self.__wvsrest.start_scan(target_id, profile_id = profile_id)
		infoMsg = "start scan target {%s} success"%url
		logger.info(infoMsg)
	
	#创建分组
	def create_group(self, group_name): 
		return self.__wvsrest.create_group_target(group_name)
	
	#根据分组名获取分组信息
	def getGroupByName(self, group_name):
		groups = self.__wvsrest.list_groups()
		
		if self.__wvsrest.getError(groups):
			logger.info('get group {%s} faild : %s'%(group_name, group))
			return
		
		for group in groups['groups']:
			if not cmp(group_name, group['name']):
				return group
	
	#获取scans
	def get_scans(self, group_name = None, group_id = None, status = ''):
		query = ''
		group = None
		scans = []
		previous_cursor = 0
		
		#filter 过滤状态为{status}的targets
		if status:
			query += 'status:%s;'%status
		
		if group_id:
			query += 'group_id:%s;'%group_id
		elif group_name:
			group = self.getGroupByName(group_name)
			#分组不存在
			if not group:
				return scans
			else:
				query += 'group_id:%s;'%group['group_id']
			
		while True:
			ret = self.__wvsrest.list_scans(previous_cursor = previous_cursor, query = query)
			previous_cursor += 100
			scans.extend(ret['scans'])
			if not ret['pagination']['next_cursor']:
				break
		
		return scans
	
	#暂停扫描
	def stop(self, group_name = None, group_id = None):
		
		#防止获取scans过快获取到的不完整，循环获取直到获取完成
		while True:
			scans = self.get_scans(group_name = group_name, group_id = group_id, status = '%s,%s,%s'%(self.SCAN_STATUS_PROCESSING, self.SCAN_STATUS_QUEUED, self.SCAN_STATUS_SCHEDULED))
			if scans:
				#开始暂停
				for scan in scans:
					self.__wvsrest.stop(scan['scan_id'])
					logger.info('stop scan {%s} success'%scan['target']['address'])
			else:
				break
		
		return scans
	
	#清理扫描记录
	def clean_scans(self, group_name = None, group_id = None, status = None):
		scans = self.get_scans(group_name = group_name, group_id = group_id, status = status)
		
		if scans:
			#开始删除
			for scan in scans:
				self.__wvsrest.del_scan(scan['scan_id'])
				logger.info('del scan {%s} success'%scan['target']['address'])
		return scans
	
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
	def clean_targets(self, group_name = None, group_id = None, text = None):
		targets = self.get_targets(group_name = group_name, group_id = group_id, text = text)
		
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
		
class NessusScan():
	
	def __init__(self, accessKey, secretKey):
		 self.__nescan = NessusRest(accessKey= accessKey, secretKey = secretKey)
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
	
	#scan_type SCAN_TEMPLATES的下标
	#获取系统扫描策略模板信息
	def getScanPolicyTemplateByName(self, template_name_index):
		template_name =  self.__nescan.SCAN_TEMPLATES[template_name_index]
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
	
	#launch_now == True 马上开始扫描
	def scan(self, template_uuid, scan_name, targets, policy_id = None, folder_id = None, description = '', launch_now = False):
		
		#检查文件夹不存在创建
		"""if folder_name:
			folders = getFolderByName(folder_name)
			if folders:
				folder_id = folders['id']
			else:
				create_folder"""
		
		scan = self.__nescan.scan(template_uuid = template_uuid, scan_name = scan_name, targets = targets, policy_id = policy_id, folder_id = folder_id, description = description)
		
		if scan and launch_now:
			self.start(scan['scan']['id'])
		
		return scan
		
	#开始扫描
	def start(self, scan_id):
		scan = self.__nescan.start(scan_id)
		if self.getError(scan):
			warnMsg = 'create scan_id {%d} faild : %s'%(scan_id, self.getError(scan))
			logger.warn(warnMsg)
			return
		return scan
	
	def stop(self, scan_id):
		stop = self.__nescan.stop(scan_id)
		if self.getError(stop):
			warnMsg = 'stop scan_id {%d} faild : %s'%(scan_id, self.getError(stop))
			logger.warn(warnMsg)
			return
		return stop
		
	def list_scan(self, group_name = None):
		list = self.__nescan.list_scan(group_name)
		if self.getError(list):
			warnMsg = 'list scan faild : %s'%self.getError(list)
			logger.warn(warnMsg)
			return
		return list

	def delete(self):
		pass
	
	def getFolderByName(self, name):
		folders = self.folders()
		for folder in folders['folders']:
			if not cmp(name, folder['name']):
				#{u'name': u'test', u'custom': 1, u'unread_count': 1, u'default_tag': 0, u'type': u'custom', u'id': 4}
				return folder
	
	#获取文件夹信息
	def folders(self):
		folders = self.__nescan.folders()
		if self.getError(folders):
			warnMsg = 'get folders faild : %s'%self.getError(folders)
			logger.warn(warnMsg)
			return
		return folders
	
	def create_folder(self, name):
		folder = self.__nescan.create_folder(name)
		if self.getError(folder):
			warnMsg = 'create folder {%s} faild : %s'%(name, self.getError(folder))
			logger.warn(warnMsg)
			return
		return folder
	
	#{u'error': u'A valid policy ID must be provided.'}
	def getError(self, msg):
		if msg.has_key('error'):
			return msg['error']