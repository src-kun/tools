#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2

from lib.core.exception import BloblastConnectionException
from lib.core.exception import BloblastDataException
from lib.core.log import logger

class Request():
	
	headers = None
	timeout = None

	def __init__(self, headers = None, timeout = 3):
		headers = self.headers
		timeout = self.timeout
		
	def open(self, url = None, values = None):
		response = None
		if url is None:
			errMsg = "url is None !"
			logger.error(errMsg) 
			raise BloblastNoneDataException(errMsg)
		elif cmp(url[0:4], "http"):
			errMsg = "{" + url + "}" + " You must start with (http[s]://)"
			logger.error(errMsg)
			raise BloblastDataException(errMsg)

		data = None
		if values:
			data = urllib.urlencode(values)
		try:
			request = urllib2.Request(url, data, self.headers)
			response = urllib2.urlopen(request, timeout = self.timeout)
			if response.code == 200:
				logger.debug(url + " 200 ok")
			else:
				print response.code
			return response
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg = url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				logger.warn(str(e))
			logger.exception("Exception Logged") 
			return None