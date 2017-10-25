#! usr/bin/python 
#coding=utf-8 

from awvsrest import WvsRest

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
	
	def __init__(self, base_url, api_key):
		self.__wvsrest = WvsRest(base_url, api_key)
	
	#url_arry 需要扫描的url数组
	#description 备注
	
	#profile_id 扫描类型（快速、完全 等...）编号
	def scan(self, url_arry, profile_id, group_name = None ,description = '', launch_now = False):
		
		target_id_arry = []
		for url in url_arry:
			#添加到target
			target = self.__wvsrest.add_target(url, description = description)
			
			if not self.__wvsrest.getError(target):
				infoMsg = 'add target {%s} success'%url
				logger.info(infoMsg)
				if launch_now:
					self.start(target_id = target['target_id'])
				target_id_arry.append(target['target_id'])
			else:
				warnMsg = 'add target {%s} %s ! '%(url, target)
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
		infoMsg = 'start scan target {%s} success'%url
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