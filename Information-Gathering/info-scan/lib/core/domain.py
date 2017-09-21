#! usr/bin/python 
#coding=utf-8 

import threading 
import sys,socket
import urllib

from lib.connection import http
from lib.core import settings
from lib.core.log import logger

import censys.ipv4
import censys.certificates
import tldextract

#真实IP
REAL_IP = 0
#云盾防护
YUN_PROTECT = 1

#云平台字典
yun_dict = {"中国":['阿里云', '腾讯集团'],"美国":['亚马逊','']}

base_operator = ["", "联通", "电信", "移动", "铁通"]

class Network():
	
	#获取域名ip
	#return {'www.baidu.com': '61.135.169.125'}
	def ip(self, domain = []):
	
		ip_arry = []	
		ip_dict = {}
		for dm in domain:
			try:
				subdomain, domain, suffix = tldextract.extract(dm)
				#过滤掉非法域名
				if not '*' in subdomain and len(domain) and len(suffix):
					debMsg = "%s %s %s {%s}"%(subdomain, domain, suffix, dm)
					logger.debug(debMsg)
					ip = socket.getaddrinfo(dm,'http')[0][4][0]
					ip_arry.append(ip)
					ip_dict[dm] = ip
			except Exception,e:
				ip_dict[dm] = ""
				errMsg = '%s {%s}'%(e, dm)
				logger.error(errMsg)
		logger.debug(ip_dict)
		return (ip_dict,ip_arry)
		
	
	
	#获取本地位置信息和云厂商
	#return {"ip":"139.199.215.179", "location":["中国","广东","广州","腾讯集团","",""], "cloud":""}
	def location(self, ip):
		ret = {}
		params = urllib.urlencode({"ip":ip,"datatype":"jsonp"})
		headers = {"token":settings.token}
		url = settings.ip_api + params
		request = http.Request(headers, url)
		request.timeout = 5
		request.open()
		result = eval(request.getHtml())
		logger.debug(result)
		if cmp(result["ret"],"ok") != -1:
			#检测已知云平台
			ret["cloud"] = ""
			if yun_dict.has_key(result["data"][0]) and result["data"][3] in yun_dict[result["data"][0]]:
					ret["cloud"] = result["data"][3]
			#记录未知厂商
			elif result["data"][3] not in base_operator:
				logger.info(result)
				
			ret["ip"] = result["ip"]
			ret["localtion"] = result["data"]
			return ret
		else:
			logger.warn(result["msg"])

class Censysio():

	UID = settings.UID
	SECRET = settings.SECRET

	def censysIPv4(self, ip, page = 1, fields = ["ip", "location.country", "443.https.tls.certificate.parsed.names"]):
		ipv4 = censys.ipv4.CensysIPv4(self.UID, self.SECRET)
		#paged search
		result = ipv4.paged_search(ip, page = page, fields = fields)
		return result
		
	def certificates(self, domain, page = 1, fields = ["parsed.__expanded_names"]):
		try:
			c = censys.certificates.CensysCertificates(self.UID, self.SECRET)
			#paged search
			result = c.paged_search("parsed.names:" + domain, page = page, fields = fields)
			domain_dict = {domain:[]}
			for res in result["results"]:
				domain_dict[domain].extend(res["parsed.__expanded_names"])
			domain_dict[domain] = list(set(domain_dict[domain]))
			return domain_dict
		except Exception,e:
			logger.warn(e)
			
			
			
