#! usr/bin/python 
#coding=utf-8 


import urllib 
import urllib2 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import sys
from pybloom import BloomFilter
import json

class Crawler:
	
	url = {0:[]}
	host = {0:[]}
	filter = None
	#TODO 爬虫深度
	level = 2
	#html编码 默认utf-8
	charset = "utf-8"
	#代理
	proxies = None
	
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
	
	#TODO过滤静态资源、无用链接 过滤掉无用字符(#)/非法字符校验修复url格式（http[s]:\\host） 去掉最后一个斜杠
	#返回格式 (url, host) url/host不符合或重复则赋值为None并返回
	def accept(self, url, in_host):
		host = None
		if not self.bloom.add(url):
			#处理url
			if len(url) > 6 and (not cmp(url[0:5], 'http:') or not cmp(url[0:6], 'https:') or not cmp(url[0:2], '//')):
				host = self.getHost(url)
				#self.filter 不等于None过滤不需要域名 等于None不过滤掉任何域名全部返回
				
				if host and self.filter and self.filter in host or not self.filter:
					if self.bloom.add(host):
						host = None
					return (url, host)
			#处理不完整url
			else:
				#self.filter 等于domain保留拼接后的url过滤掉所有不完整url 或 self.filter为None不过滤任何不完整url
				if self.filter in in_host or not self.filter:
					return (in_host + '/' + url, host)
		#url已存在 或 url不属于此域名被过滤掉
		return (None, None)
					
	
	#成功返回 html / 失败返回 None
	#url not None时优先爬取url
	def open(self, current_level, url = None, values = None):
		try:
			if url is None:
				raise Exception('url is None !')
			
			#检测爬虫深度
			if current_level > self.level:
				return  (-1, None, None)

			#拼接domain的网址
			if not cmp(url[0:5], 'http:'):
				domain = 'http://'
			elif not cmp(url[0:6], 'https:'):
				domain = 'https://'
			domain = domain + self.getHost(url)
			
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
			response = urllib2.urlopen(request) 
			return (current_level, domain, response.read())
		except Exception,e:
			#logger.error('opne '+ url + 'error')
			#logger.exception("Exception Logged") 
			#TODO 增加log输出
			print e
			return  (-1, None, None) 

	#从url中提取出host部分，提取失败返回None
	def getHost(self, url):
		proto, rest = urllib.splittype(url)
		res, rest = urllib.splithost(rest)
		return res
			
	#将url和domain压入数组
	def push(self, current_level, url, host):
		if url:
			self.url[current_level].append(url)
		if host:
			self.host[current_level].append(host)

	#解析出html中的链接
	def parser(self, current_level, in_host, html):
		url = None
		host = None
		soup = BeautifulSoup(str(html).decode(self.charset),  "html.parser")
		for a in soup.find_all('a'):
			try:
				url, host = self.accept(a['href'], in_host)
				self.push(current_level, url, host)
			except Exception,e:
				#LOG 输出
				#print e
				pass
				

	
if __name__ == '__main__':
	#http://csdn.net
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	c = Crawler(bloom)
	c.filter = "cnblogs.com"
	#c.charset = "gb2312"
	#c.headers['Cookie'] = cookies
	#get request
	current_level, host, html = c.open(1, "http://www.cnblogs.com")
	print host
	#post request
	#html = c.open("http://www.zgyey.com/",{'id':1})
	if current_level is not -1:
		c.parser(current_level, host, html)
	print c.url
	print
	print
	print c.host



