#! usr/bin/python 
#coding=utf-8 

import sys

import urllib 
import urllib2
import tldextract
import html
from bs4 import BeautifulSoup
from pybloom import BloomFilter
import json
import chardet
import threading
import socket
import config

from lib.connection import http
from lib.core import settings
from lib.core.log import logger

#支持的协议
support_proto = ['http', 'https']

class Crawler:

	#代理 {'proxyPool':{'socks5':['192.168.1.206', 1080], 'socks4':['192.168.1.207', 1080],...}}
	proxies = None
	timeout = 3

	#过滤器
	__bloom = None
	
	#初始化
	def __init__(self, bloom):
		self.bloom = bloom
		self.start_url = None
		# depth当前收集到的域名深度，自定义爬取的依据
		self.__host = {'domain':{0:[]}, 'url':{0:[]}, 'depth':0}
		#TODO 过滤掉了不同域名格式的url（.com/.net/.org...）
		self.filter = None
		#爬虫深度
		self.level = 0
		#TODO cookie and random User-Agent 
		self.headers = settings.headers
	
	#成功返回 html / 失败返回 None
	#url not None时优先爬取url
	def request(self, url, cookies = None, values = None):
			if cookies:
				self.headers['cookies'] = cookies
			request = http.Request(self.headers, url, values)
			request.timeout = self.timeout
			request.open()
			return request
	
	def getHost(self):
		for key in self.__host['domain']:
			self.__host['domain'][key] = list(set(self.__host['domain'][key]))
			self.__host['url'][key] = list(set(self.__host['url'][key]))
		return self.__host

	def depthInc(self):
		 self.__host['depth'] += 1
	#分解url
	#return ('协议', '子域名', '域名', '资源路径', '域名类型')
	def separate(self, url):
		proto, position = urllib.splittype(url)
		domain, resources = urllib.splithost(position)
		tldext = tldextract.extract(url)
		if not tldext.domain and not proto:
			domain = None
		elif tldext.suffix:
			if tldext.subdomain:
				domain = '%s://%s.%s.%s'%(proto, tldext.subdomain, tldext.domain, tldext.suffix)
			else:
				domain = '%s://%s.%s'%(proto, tldext.domain, tldext.suffix)
		else:
			domain = '%s://%s'%(proto, tldext.domain)
		return (proto, tldext.subdomain, domain, resources, tldext.suffix)
	
	#TODO 增加相近url匹配过滤，去除相似url 如 host/2345.html host/4567.html
	#return (url, proto, domain)
	def __accept(self, current_url, url):
		if not url in self.bloom:
			#处理url
			(proto, subdomain, domain, resources, suffix) = self.separate(url)
			#过滤掉非self.filter下的域名 或 self.filter == None 全部通过不过滤
			if (proto and proto in support_proto) and domain and (not self.filter or self.filter in domain):
				if domain in self.bloom:
					domain = None
				return (url, proto, domain)
			#处理不完整url 不完整url识别；域名 and 协议不存在 and 资源路径存在
			elif not domain and not proto and resources:
					url_ret = '%s/%s'%(current_url, resources)
					#self.filter 等于domain保留拼接后的url过滤掉所有不完整url 或 self.filter为None不过滤任何不完整url
					if self.filter in current_url or not self.filter:
						return (url_ret, proto, domain)
			elif proto not in support_proto:
				#TODO处理其它协议
				pass
			else:
				#TODO 处理其它可能
				#域名为ip的情况 ('http', '127.0.0.1', '/123?test=1', '')
				pass
		#url已存在 或 url不属于此域名被过滤掉 或 url不合规
		return (None, None, None)
		
	#将url和domain压入字典中
	def __push(self, current_level, current_url, url):
		if url:
			(url, proto, domain) = self.__accept(current_url, url)
			#字典key不存在则创建
			if not self.__host['url'].has_key(current_level):
				self.__host['url'][current_level] = []
			if not self.__host['domain'].has_key(current_level):
				self.__host['domain'][current_level] = []
				self.__host['depth'] = current_level

			if url:
				self.bloom.add(url)
				self.__host['url'][current_level].append(url)
				debMsg = '{%s} __pushed'%url
				logger.debug(debMsg)

			if domain:
				self.bloom.add(domain)
				self.__host['domain'][current_level].append(domain)
				debMsg = '{%s} __pushed'%domain
				logger.debug(debMsg)

	#解析出html中的链接
	def parser(self, current_level, current_url, html):
		try:
			#动态获取字符集
			charset = chardet.detect(str(html))['encoding']
			soup = BeautifulSoup(str(html).decode(charset, 'ignore'), 'html.parser')
			for a in soup.find_all('a'):
				try:
					self.__push(current_level, current_url, a['href'])
				except Exception,e:
					logger.debug(str(e))
					pass
		except Exception,e:
			logger.debug(str(e))
			pass

	#TODO 线程控制
	def start(self):
		threadLock = threading.Lock()
		threads = []
		(proto, subdomain, domain, resources, suffix) = self.separate(self.start_url)
		self.__push(self.__host['depth'], domain, domain)
		tmp_domain = self.__host['url'][self.__host['depth']][:]
		start_index = self.__host['depth']
		for current_level in range(start_index, self.level):
			host_len = len(tmp_domain)
			for i in range(host_len):
				# 创建新线程
				thread = CrawlerTrd(threadLock, current_level, self, tmp_domain[i])
				# 开启新线程
				thread.start()
				# 添加线程到线程列表
				threads.append(thread)
			# 等待线程完成
			for t in threads:
				t.join()
			if not self.__host['domain'].has_key(current_level):
				break
			tmp_domain = self.__host['domain'][current_level][:]
		logger.info('='*100)
		logger.info(self.__host['domain'])
		logger.info('='*100)
	 
class CrawlerTrd (threading.Thread):
	def __init__(self, threadLock, current_levle, crawler, url, data = None):
		threading.Thread.__init__(self)
		self.crawler = crawler
		self.url = url
		self.data = data
		self.current_levle = current_levle
		self.threadLock = threadLock
		
	def run(self):
		#get request
		html = self.crawler.request(self.url).getHtml()
		#post request
		#html = crawler.request(self.current_levle, self.url, self.data)
		current_url = self.url
		if html:
			self.crawler.parser(self.current_levle, current_url, html)
		#threadLock.acquire()
		# 释放锁
		#threadLock.release()
	
def t_crawlerApi(crawler):
	crawler.start()

#多线程Demo
def t_demo(url, filter):
	#http://csdn.net
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	crawler = Crawler(bloom)
	crawler.filter = filter
	crawler.level = 3
	crawler.start_url = url
	#crawler.proxies = {'type':'socks5', 'ip':'192.168.1.206', 'port':1080}
	crawler.start()
	return crawler.getHost()
	#print crawler.url
	
#Demo
def demo():
	
	current_levle = 0
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	crawler = Crawler(bloom)
	crawler.start_url = ['http','www.bit.edu.cn/']
	crawler.filter = 'eastmoney.com'
	#get request
	html = crawler.request(current_levle, crawler.start_url).getHtml()
	#post request
	#html = crawler.request(current_levle, crawler.start_url, date)
	if html:
		crawler.parser(current_levle, crawler.start_url, html)
	#print crawler.host
	#print crawler.url
	
if __name__ == '__main__':
	t_demo()
	#demo()
	#print config.getConfig('http_header', 'header');


