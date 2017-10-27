#! usr/bin/python 
#coding=utf-8 

import threading 
import sys,socket
import types 

import censys.ipv4
import censys.certificates
import tldextract
import urllib

from lib.connection import http
from lib.core import settings
from lib.core.log import logger
from lib.utils.common import separate

#真实IP
REAL_IP = 0
#云盾防护
YUN_PROTECT = 1

#云平台字典
yun_dict = {'中国':['阿里云', '腾讯集团'],'美国':['亚马逊','']}

base_operator = ['', '联通', '电信', '移动', '铁通']

class Network():
	
	#批量获取域名ip 
	#ip数组的顺序和domain数组内的域名一一对应
	#return {'ip': [ip,ip1,...]}
	def __ip_bat(self, domain_arry):
		index = 0
		ip_arry = []
		for domain in domain_arry:
			try:
				(proto, substr, domain, resources, suffix) = separate(domain)
				ip = socket.getaddrinfo(domain,'http')[0][4][0]
				ip_arry.append(ip)
			except Exception,e:
				ip_arry.append('')
				errMsg = '%s {%s}'%(e, domain)
				logger.error(errMsg)
			index += 1
		logger.debug(ip_arry)
		return ip_arry
	
	#获取域名ip
	#return ip
	def __ip_sin(self, domain):
		ip = None
		try:
			subdomain, subject, suffix = tldextract.extract(domain)
			#过滤掉非法域名
			if not '*' in subdomain and len(subject) and cmp(subject, 'com') and len(suffix):
				debMsg = '%s %s %s {%s}'%(subdomain, subject, suffix, domain)
				logger.debug(debMsg)
				ip = socket.getaddrinfo(domain,'http')[0][4][0]
		except Exception,e:
			errMsg = '%s {%s}'%(e, domain)
			logger.error(errMsg)
		return ip
	
	#获取域名ip的对外接口
	def ip(self, domain):
		if type(domain) is types.ListType:
			return self.__ip_bat(domain)
		elif type(domain) is types.StringType:
			return self.__ip_sin(domain)
		

	#获取本地位置信息和云厂商
	#return {'ip':'139.199.215.179', 'location':['中国','广东','广州','腾讯集团','',''], 'cloud':''}
	def location(self, ip):
		ret = {}
		params = urllib.urlencode({'ip':ip,'datatype':'jsonp'})
		headers = {'token':settings.token}
		url = settings.ip_api + params
		request = http.Request(headers, url)
		request.timeout = 5
		request.open()
		result = eval(request.getHtml())
		logger.debug(result)
		if cmp(result['ret'],'ok') != -1:
			#检测已知云平台
			ret['cloud'] = ''
			if yun_dict.has_key(result['data'][0]) and result['data'][3] in yun_dict[result['data'][0]]:
					ret['cloud'] = result['data'][3]
			#记录未知厂商
			elif result['data'][3] not in base_operator:
				logger.info(result)
				
			ret['ip'] = result['ip']
			ret['localtion'] = result['data']
			return ret
		else:
			logger.warn(result['msg'])

class Censysio():

	UID = settings.UID
	SECRET = settings.SECRET

	def censysIPv4(self, ip, page = 1, fields = ['ip', 'location.country', '443.https.tls.certificate.parsed.names']):
		ipv4 = censys.ipv4.CensysIPv4(self.UID, self.SECRET)
		#paged search
		result = ipv4.paged_search(ip, page = page, fields = fields)
		return result
	
	#domain收集
	#return {'domain':[], 'page':0, 'pages':0} 
	# u'metadata': {u'count': 8, u'query': u'parsed.names: csdn.net', u'backend_time': 796, u'page': 1,u'pages': 1}}
	def certificates(self, domain, page = 1, fields = ['parsed.__expanded_names']):
		domain_dict = {'domain':[], 'metadata': {'count': 0, 'query': 'parsed.names: csdn.net', 'backend_time': 0, u'page': 0,u'pages': 0}}
		try:
			c = censys.certificates.CensysCertificates(self.UID, self.SECRET)
			#paged search
			result = c.paged_search('parsed.names: %s'%domain, page = page, fields = fields)
			infoMsg = "{%s} syscen search result ==> %s"%(domain, result)
			logger.info(infoMsg)
			if 'ok' in result['status']:
				domain_dict['metadata'] = result['metadata']
				for res in result['results']:
					domain_dict['domain'].extend(res['parsed.__expanded_names'])
				if domain_dict['domain']:
					domain_dict['domain'] = list(set(domain_dict['domain']))
			else:
				#TODO 处理失败
				pass
		except Exception,e:
			warnMsg = '{parsed.names: %s} %s'%(domain,str(e))
			logger.warn(warnMsg)
		return domain_dict