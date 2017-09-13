#! usr/bin/python 
#coding=utf-8 

import threading 
import sys,socket
import urllib

from lib.connection import http
from lib.core import settings
from lib.core.log import logger

#真实IP
REAL_IP = 0
#云盾防护
YUN_PROTECT = 1

#云盾字典	{"中国":["阿里云", "腾讯集团"]}
yundun_dict = {"\xe4\xb8\xad\xe5\x9b\xbd":['\xe9\x98\xbf\xe9\x87\x8c\xe4\xba\x91', '\xe8\x85\xbe\xe8\xae\xaf\xe9\x9b\x86\xe5\x9b\xa2']}


class network():
	
	type = REAL_IP
	#{"baidu.com": ["111.13.101.208":{"location":"location"}, "220.181.57.217":{"location":"location"}, "220.181.57.217":{"location":"location"}]}
	def ip(self, domain, num = 3):
		ip_dict = {}
		try:
			for i in range(0, num):
				addr = socket.getaddrinfo(domain, "http")[0][4][0]
				if not ip_dict.has_key(domain):
					ip_dict[domain] = []
				ip_dict[domain].append(addr)
		except Exception,e:
			print e
		return ip_dict
	
	#{"ret":"ok","ip":"139.199.215.179","data":["中国","广东","广州","腾讯集团","",""],"yundun":""}
	def location(self, ip):
		params = urllib.urlencode({"ip":ip,"datatype":"jsonp"})
		headers = {"token":settings.token}
		url = settings.ip_api + params
		request = http.Request(headers, url)
		request.timeout = 5
		request.open()
		result = eval(request.getHtml())
		if cmp(result["ret"],"ok") != -1:
			if result[data][3]
			return result
		else:
			logger.warn(result["msg"])
		
	
		
	
	