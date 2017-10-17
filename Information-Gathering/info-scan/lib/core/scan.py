#! usr/bin/python 
#coding=utf-8 

from lib.core.rest import NessusRest
from lib.core.rest import NessusRest
from lib.core.rest import WvsRest
from lib.core.log import logger
from lib.utils.common import input

class WvsScan():
	#终止状态
	SCAN_STATUS_ABORT = 'aborted'
	#运行状态
	SCAN_STATUS_PROCESSING = 'processing'
	#等待状态
	SCAN_STATUS_QUEUED = 'queued'
	#完成状态
	SCAN_STATUS_COMPLETED = 'completed'
	
	def __init__(self):
		self.__wvsrest = WvsRest()
	
	#url_arry 需要扫描的url数组
	#description 备注
	def scan(self, url_arry, description = '', group_name = None):
		
		target_id_arry = []
		for url in url_arry:
			#添加到target
			target = self.__wvsrest.add_target(url, description = description)
			
			if not self.__wvsrest.getError(target):
				infoMsg = "add target {%s} success"%url
				logger.info(infoMsg)
				#启动扫描
				#self.__wvsrest.start_scan(target['target_id'])
				target_id_arry.append(target['target_id'])
				#infoMsg = "start scan target {%s} success"%url
				#logger.info(infoMsg)
			else:
				warnMsg = "add target {%s} %s ! "%(url, target)
				logger.warn(warnMsg)
		
		if group_name:
			#检查分组不存在创建
			group = self.__wvsrest.list_groups_target(group_name)
			if not group:
				group = self.__wvsrest.create_group_target(group_name)
			#将启动的target添加到group_name分组
			self.__wvsrest.add_target_to_group(target_id_arry, group['group_id'])
		return target_id_arry
	
	#根据分组名获取分组信息
	def getGroupByName(self, group_name):
		group = self.__wvsrest.list_groups_target(group_name)
		if self.__wvsrest.getError(group):
			logger.info('get group {%s} faild : %s'%(group_name, group))
			return
		return group
	
	def get_scans(self, scan_id = None, group_name = None, group_id = '', status = ''):
		query = ''
		group = None
		
		#filter 过滤状态为{status}的targets
		if status:
			query += 'status:%s;'%status
		
		if group_name:
			group = self.getGroupByName(group_name)
			#分组不存在
			if not group:
				return
			else:
				group_id = group['group_id']
				query += 'group_id:%s;'%group_id
		
		scans = self.__wvsrest.list_scans(scan_id = scan_id, query = query)
		return scans
	
	def stop(self):
		scans = self.get_scans(group_name = group_name, group_id = group_id)['scans']
		
		#开始暂停
		for scan in scans:
			self.__wvsrest.del_scan(scan['scan_id'])
			logger.info('stop scan {%s} success'%scan['target']['address'])
		return scans
	
	def clean_scans(self, group_name = None, group_id = None):
		scans = self.get_scans(group_name = group_name, group_id = group_id)
		if scans:
			#开始删除
			for scan in scans['scans']:
				self.__wvsrest.del_scan(scan['scan_id'])
				logger.info('del scan {%s} success'%scan['target']['address'])
		return scans
	
	#获取targets
	def get_targets(self, target_id = None, group_name = None, group_id = None):
		previous_cursor = 0
		targets = []
		group = None
		
		#获取group name对应的group id
		if group_name:
			group = self.getGroupByName(group_name)
			#分组不存在
			if not group:
				return
			else:
				group_id = group['group_id']
		
		#取出target
		#group_name != None 时取出group_name分组内所有target
		while True:
			ret = self.__wvsrest.list_targets(target_id = target_id, previous_cursor = previous_cursor,  group_id = group_id )
			previous_cursor += 100
			targets.extend(ret['targets'])
			if not ret['pagination']['next_cursor']:
				break
		
		return targets
	
	#清除target
	def clean_targets(self, group_name = None, group_id = None):
		targets = self.get_targets(group_name = group_name, group_id = group_id)
		
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