#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2

from lib.core.exception import BloblastConnectionException
from lib.core.exception import BloblastDataException
from lib.core.exception import BloblastNoneDataException
from lib.core.log import logger

class Request():

	def __init__(self, headers = {}, context = None):
		self.headers = headers
		self.context = context
		self.timeout = 5
		
	def open(self, url = None, values = None):
		self.__accept(url)

		data = None
		if values:
			data = urllib.self.urlencode(self.values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			self.__response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if self.__response.code == 200:
				logger.info(url + " 200 ok")
			return self.__response
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
				code = e.code
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
			return None
	
	def __accept(self, url):
		if url is None:
			errMsg = "url is None !"
			logger.error(errMsg)
			raise BloblastNoneDataException(errMsg)
		elif cmp(url[0:4], "http"):
			errMsg = "{" +url + "}" + " You must start with (http[s]://)"
			logger.error(errMsg)
			raise BloblastDataException(errMsg)
	
	def response(self):
		return self.__response
	
	def setCookie():
		self.headers['cookie']
	
	def get(self, url = None):
		self.__accept(url)
		try:
			request = urllib2.Request(url.encode('utf-8'), headers = self.headers)
			request.get_method = lambda: 'GET'
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if response.code == 200:
				logger.info(url + " 200 ok")
			return response
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
				code = e.code
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
			return None
		
	def post(self, url = None, values = None):
		self.__accept(url)

		data = None
		if values:
			data = urllib.self.urlencode(self.values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			request.get_method = lambda: 'POST'
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if response.code == 200:
				logger.info(url + " 200 ok")
			return response
		except Exception,e:
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
				code = e.code
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
			return None

	def read(self, response):
		try:
			if response:
				return response.read()
		except Exception,e:
			errMsg = self.__url + " " + str(e)
			logger.error(errMsg)
			return None
