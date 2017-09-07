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
	__response = None
	__url = None
	code = None
	__values = None

	def __init__(self, headers = None, url = None, values = None, timeout = 5):
		self.headers = headers
		self.timeout = timeout
		self.__url = url
		self.__values = values
		self.open()
		
	def open(self):
		if self.__url is None:
			errMsg = "self.__url is None !"
			logger.error(errMsg) 
			raise BloblastNoneDataException(errMsg)
		elif cmp(self.__url[0:4], "http"):
			errMsg = "{" + self.__url + "}" + " You must start with (http[s]://)"
			logger.error(errMsg)
			raise BloblastDataException(errMsg)

		data = None
		if self.__values:
			data = urllib.self.urlencode(self.__values)
		try:
			request = urllib2.Request(self.__url.encode('utf-8'), data, self.headers)
			self.__response =urllib2.urlopen(request, timeout = self.timeout)
			if self.__response.code == 200:
				logger.info(self.__url + " 200 ok")
			return self.__response
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg = self.__url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
				code = e.code
			else:
				errMsg = str(e) + " " + self.__url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
			return None
			
	def response(self):
		return self.__response
	
	def getHtml(self):
		try:
			if self.__response:
				return self.__response.read()
		except Exception,e:
			errMsg = self.__url + " " + str(e)
			logger.error(errMsg)
			return None
