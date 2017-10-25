#! usr/bin/python 
#coding=utf-8 

class WvsRest():
	
	def __init__(self, base_url, api_key):
		self.context = ssl._create_unverified_context()
		self.base_url = base_url
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
	def add_target_to_group(self, target_id, group_id):
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