#! usr/bin/python 
#coding=utf-8 


import urllib 
import urllib2 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import sys
from pybloom import BloomFilter
import json
import chardet
import threading

class Crawler:
	
	url = {0:[]}
	host = {0:[]}
	filter = None
	#爬虫深度
	level = 0
	#代理
	proxies = None
	timeout = 3
	
	#TODO cookie and random User-Agent 
	headers = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Referer":"https://baidu.com",
			"Cookie":" dc_session_id=1502790073620_0.12930882713190395",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
	}
	
	#初始化
	def __init__(self, bloom):
		self.bloom = bloom
	
	#TODO过滤静态资源、无用链接 过滤掉无用字符(#)/非法字符校验修复url格式（http[s]:\\host） 归类（host/url） 去掉最后一个斜杠
	#TODO 增加相近url匹配过滤，去除相似url 如 host/2345.html host/4567.html
	#返回格式 (url, host) url/host不符合或重复则赋值为None并返回
	def accept(self, url, current_url):
		if not self.bloom.add(url):
			#处理url
			if len(url) > 6 and (not cmp(url[0:5], 'http:') or not cmp(url[0:6], 'https:') or not cmp(url[0:2], '//')):
				proto, host = self.getHost(url)
				#self.filter 不等于None过滤不需要域名 等于None不过滤掉任何域名全部通过
				if host and self.filter and self.filter in host or not self.filter:
					if self.bloom.add(host):
						host = None
					elif proto and host:
						host = proto + "://" + host
					return (url, host)
			#处理不完整url
			else:
				#TODO url 合规性检测 后期优化启动后直接加载到内存中
				messy = ["javascript:", "tencent:"]
				if str(messy).find(url[0:4]) == -1:
					path = "/" + url
					#self.filter 等于domain保留拼接后的url过滤掉所有不完整url 或 self.filter为None不过滤任何不完整url
					if self.filter in current_url or not self.filter:
						return (current_url + path, None)
		#url已存在 或 url不属于此域名被过滤掉 或 url不合规
		return (None, None)
					
	
	#成功返回 html / 失败返回 None
	#url not None时优先爬取url
	def open(self, current_level, url = None, values = None):
		try:
			if url is None:
				raise Exception('url is None !')
			
			#检测爬虫深度
			if current_level > self.level:
				return None

			#获取domain的网址
			proto, host = self.getHost(url)
			current_url = url#proto + "://" + host
			#values 不等于None则是POST请求
			data = values
			if values:
				data = urllib.urlencode(values)
			
			#设置代理
			#TODO 代理池
			if self.proxies :   
				proxy_s = urllib2.ProxyHandler(self.proxies)
				opener = urllib2.build_opener(proxy_s)
				urllib2.install_opener(opener) 
				
			request = urllib2.Request(url, data, self.headers) 	
			response = urllib2.urlopen(request, timeout = self.timeout) 
			return response.read()
		except Exception,e:
			#logger.error('opne '+ url + 'error')
			#logger.exception("Exception Logged") 
			#TODO 增加log输出
			#print e
			return  (-1, None) 

	#从url中提取出host部分，提取失败返回None
	def getHost(self, url):
		proto, rest = urllib.splittype(url)
		res, rest = urllib.splithost(rest)
		return (proto, res)
			
	#将url和domain压入数组
	def push(self, current_level, url, host):
	
		#字典key不存在则创建
		if not self.url.has_key(current_level):
			self.url[current_level] = []
		if not self.host.has_key(current_level):
			self.host[current_level] = []
			
		if url:
			self.url[current_level].append(url)
		if host:
			self.host[current_level].append(host)

	#解析出html中的链接
	def parser(self, current_level, current_url, html):
		url = None
		host = None
		try:
			#动态获取字符集
			charset = chardet.detect(str(html))['encoding']
			soup = BeautifulSoup(str(html).decode(charset), "html.parser")
			for a in soup.find_all('a'):
				try:
					url, host = self.accept(a['href'], current_url)
					self.push(current_level, url, host)
				except Exception,e:
					#LOG 输出
					#print e
					pass
		except Exception,e:
			#LOG 输出
			#print e
			pass
	#TODO线程控制
	def start(self, url):
		threadLock = threading.Lock()
		threads = []
		self.url[0].append(url)
		tmp_host = self.url[0][:]
		for current_level in range(0, self.level):
			host_len = len(tmp_host)
			for i in range(host_len):
				# 创建新线程
				thread = CrawlerTrd(threadLock, current_level, self, tmp_host[i])
				# 开启新线程
				thread.start()
				# 添加线程到线程列表
				threads.append(thread)
			# 等待线程完成
			for t in threads:
				t.join()
			if not self.host.has_key(current_level):
				break
			tmp_host = self.host[current_level][:]
	 
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
		html = self.crawler.open(self.current_levle, self.url)
		#post request
		#html = crawler.open(self.current_levle, self.url, self.data)
		if html:
			self.crawler.parser(self.current_levle, self.url, html)
		#threadLock.acquire()
		# 释放锁
		#threadLock.release()
	


#多线程Demo
def t_demo():
	#http://csdn.netn
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	crawler = Crawler(bloom)
	crawler.filter = "zgyey.com"
	crawler.level = 4
	crawler.start("http://www.zgyey.com")
	print crawler.host
	#print crawler.url
	
#单线程Demo	
def demo():
	url = "http://zgyey.com/"
	current_levle = 0
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	crawler = Crawler(bloom)
	crawler.filter = "zgyey.com"
	#get request
	html = crawler.open(current_levle, url)
	#post request
	#html = crawler.open("http://www.zgyey.com/", data)
	if html:
		crawler.parser(current_levle, url, html)
	print crawler.host
	#print crawler.url
	
if __name__ == '__main__':
	#t_demo()
	demo()


