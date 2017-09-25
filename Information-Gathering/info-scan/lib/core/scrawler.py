#! usr/bin/python 
#coding=utf-8 

import sys

import urllib 
import urllib2
import html
from bs4 import BeautifulSoup
from pybloom import BloomFilter
import json
import chardet
import threading
import socket
import config
import types

from lib.connection import http
from lib.core import settings
from lib.core.log import logger
from lib.utils.common import separate

#支持的协议
support_proto = ['http', 'https']
#代理 {'proxyPool':{'socks5':['192.168.1.206', 1080], 'socks4':['192.168.1.207', 1080],...}}
proxies = None

class Crawler:

	timeout = 3
	#过滤器
	__bloom = None
	
	#初始化
	def __init__(self, bloom):
		self.bloom = bloom
		# depth当前收集到的域名深度，自定义爬取的依据
		self.__host = {'full_domain':{0:[]}, 'domain':[], 'raw':{'url':{0:[]}, 'another':[]}, 'depth':0}
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
		for key in self.__host['raw']['url']:
			self.__host['full_domain'][key] = list(set(self.__host['full_domain'][key]))
			self.__host['raw']['url'][key] = list(set(self.__host['raw']['url'][key]))
		self.__host['domain'] = list(set(self.__host['domain']))
		self.__host['raw']['another'] = list(set(self.__host['raw']['another']))
		return self.__host

	def depthInc(self):
		 self.__host['depth'] += 1

	#添加domain并返回添加成功的个数
	def appendDomain(self, full_domain_arry):
		num = 0
		if type(full_domain_arry) is types.ListType:
			full_domain_arry = list(set(full_domain_arry))
			for full_domain in full_domain_arry:
				if not full_domain in self.bloom:
					num += 1
				self.__push(self.__host['depth'], full_domain, full_domain)
		elif type(full_domain_arry) is types.StringType:
			if not full_domain_arry in self.bloom:
				num += 1
			self.__push(self.__host['depth'], full_domain_arry, full_domain_arry)
		return num
	
	#TODO 增加相近url匹配过滤，去除相似url 如 host/2345.html host/4567.html
	#return ('url', '协议', '完整域名', '域名', '非域名链接')
	def __accept(self, current_url, url):
		if not url in self.bloom:
			another = None
			#处理url
			(proto, substr, domain, resources, suffix) = separate(url)
			#过滤掉非self.filter下的域名 或 self.filter == None 全部通过不过滤
			if (proto and proto in support_proto) and domain and (not self.filter or self.filter in domain):
				full_domain = "%s://%s"%(proto, domain)
				if full_domain in self.bloom:
					full_domain = None
				return (url, proto, full_domain, domain, url)
			#处理不完整url 不完整url识别；域名 and 协议不存在 and 资源路径存在
			elif not domain and resources:
				if not url in self.bloom:
					full_url = '%s/%s'%(current_url, resources)
					return (full_url, proto, None, None, another)
			elif proto not in support_proto:
				#TODO 处理其它协议
				pass
			elif self.filter and domain and not (self.filter in domain):
				#TODO 保存爬取到的其它网站url
				#another = url
				#print another
				#return (None, None, None, None, another)
				pass
			else:
				pass
				#TODO 处理其它可能 域名为ip的情况 ('http', '127.0.0.1', '/123?test=1', '')
				
		#url已存在 或 url不属于此域名被过滤掉 或 url不合规
		return (None, None, None, None, None)
	
	#检查字典key不存在则创建
	def __createLevelKey(self, level):
		if not self.__host['raw']['url'].has_key(level):
			self.__host['raw']['url'][level] = []
		if not self.__host['full_domain'].has_key(level):
			self.__host['full_domain'][level] = []
			self.__host['depth'] = level
	
	#将url和domain压入字典中
	def __push(self, current_level, current_url, url):
		if url:
			(full_url, proto, full_domain, domain, another) = self.__accept(current_url, url)
			
			self.__createLevelKey(current_level)
			if full_domain and not self.bloom.add(full_domain):
				self.__host['full_domain'][current_level].append(full_domain)
				self.__host['domain'].append(domain)
				debMsg = '{%s} __pushed'%full_domain
				logger.debug(debMsg)
			
			#保存domain下的url链接
			if full_url and not self.bloom.add(full_url):
				self.__host['raw']['url'][current_level].append(full_url)
				debMsg = '{%s} __pushed'%full_url
				logger.debug(debMsg)
				
			#保存非domain下的url链接
			if another and not self.bloom.add(another):
				self.__host['raw']['another'][current_level].append(another)
				debMsg = '{%s} __pushed'%another
				logger.debug(debMsg)
			#将不完整url压入bloom
			self.bloom.add(url)
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
	#depth :从host那一层开始，为-1时默认使用self.__host['depth']
	def start(self, depth = -1):
		threadLock = threading.Lock()
		threads = []
		start_index = self.__host['depth']
		tmp_domain = self.__host['full_domain'][self.__host['depth']][:]
		for current_level in range(start_index, self.level):
			host_len = len(tmp_domain)
			if not host_len:
				break
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
			if not self.__host['full_domain'].has_key(current_level):
				break
			tmp_domain = self.__host['full_domain'][self.__host['depth']][:]
		if tmp_domain:
			self.__host['depth'] += 1
			self.__host['full_domain'][self.__host['depth']] = []
		logger.info('{doamin}' + '='*50)
		logger.info(self.__host['full_domain'])
		logger.info('='*50)
	 
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
		respose = self.crawler.request(self.url)
		#post request
		#html = crawler.request(self.current_levle, self.url, self.data)
		current_url = self.url
		if respose:
			html = respose.getHtml()
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


