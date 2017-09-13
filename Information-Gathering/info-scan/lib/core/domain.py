#! usr/bin/python 
#coding=utf-8 

import threading 
import sys,socket
import urllib

from lib.connection import http
from lib.core import settings
from lib.core.log import logger


class network():

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
	
	#{"111.13.101.208":{"location":"location"}}
	def location(self, ip):
		params = urllib.urlencode({"ip":ip,"datatype":"jsonp"})
		headers = {"token":settings.token}
		url = settings.ip_api + params
		request = http.Request(headers, url)
		request.timeout = 5
		request.open()
		result = eval(request.getHtml())
		if cmp(result["ret"],"ok") != -1:
			return result
		else:
			logger.warn(result["msg"])
		
	
	