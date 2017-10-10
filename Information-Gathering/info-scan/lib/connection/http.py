#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2
import json

from lib.core.exception import BloblastConnectionException
from lib.core.exception import BloblastDataException
from lib.core.exception import BloblastNoneDataException
from lib.core.log import logger

class Request():

	def __init__(self, headers = {}, context = None):
		self.headers = headers
		self.context = context
		self.timeout = 5
	
	def __accept(self, url):
		if url is None:
			errMsg = "url is None !"
			logger.error(errMsg)
			raise BloblastNoneDataException(errMsg)
		elif cmp(url[0:4], "http"):
			errMsg = "{" +url + "}" + " You must start with (http[s]://)"
			logger.error(errMsg)
			raise BloblastDataException(errMsg)
	
	"""def get(self, url = None, lamb = 'GET'):
		self.__accept(url)
		try:
			request = urllib2.Request(url.encode('utf-8'), headers = self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if not cmp(lamb, 'GET') and response.code == 200:
				logger.info(url + " 200 ok")
		except urllib2.HTTPError,e:
			response = e
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
				#logger.exception("Exception Logged");
		return response"""
		
	def get(self, url):
		response = self.connect(url, lamb = 'GET')
		if response.code == 200:
			logger.info(url + " 200 ok")
		return response
		
	"""def post(self, url = None, values = None, lamb = 'POST'):
		self.__accept(url)
		response = None
		data = None
		if not cmp(self.headers['Content-Type'], 'application/json'):
			data = json.dumps(values)
		elif values:
			data = urllib.urlencode(values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
			if not cmp(lamb, 'POST') and response.code == 200:
				logger.info(url + " 200 ok")
		except urllib2.HTTPError,e:
			response = e
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
		return response"""
	def post(self, url, values = None):
		response = self.connect(url, values = values, lamb = 'POST')
		if response.code == 200:
			logger.info(url + " 200 ok")
		return response

	def connect(self, url, lamb, values = None):
		self.__accept(url)
		response = None
		data = None
		if not cmp(self.headers['Content-Type'], 'application/json') and values:
			data = json.dumps(values)
		elif values:
			data = urllib.urlencode(values)
		try:
			request = urllib2.Request(url.encode('utf-8'), data, self.headers)
			request.get_method = lambda: lamb
			response = urllib2.urlopen(request, timeout = self.timeout, context = self.context)
		except urllib2.HTTPError,e:
			response = e
			"""
			print e.code  
			print e.reason
			print e.geturl()  
			print e.read()
			"""
			if hasattr(e, 'code'):
				warnMsg =url + " " + str(e.code) + " failed"
				logger.warn(warnMsg)
			else:
				errMsg = str(e) + " " +url
				logger.error(errMsg)
			#logger.exception("Exception Logged");
		return response

	def put(self, url, values):
		response = self.connect(url, values = values, lamb = 'PUT')
		if response.code == 200:
			logger.info(url + " 200 ok")
		return response
		
	def delete(self, url, values):
		response = self.connect(url, lamb = 'DELETE')
		if response.code == 200:
			logger.info(url + " 200 ok")
		return response

	def read(self, response):
		try:
			if response:
				return response.read()
		except Exception,e:
			errMsg = self.__url + " " + str(e)
			logger.error(errMsg)
			return None
