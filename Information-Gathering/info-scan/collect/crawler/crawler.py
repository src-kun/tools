#! usr/bin/python 
#coding=utf-8 

#参考：
#	http://www.jianshu.com/p/f57187e2b5b9 bloom filter

import urllib 
import urllib2 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import sys
from pybloom import BloomFilter

bloom = BloomFilter(capacity=100000, error_rate=0.001)
url_json = []
host_json = []

def open(url, values):
	headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' ,'Referer': 'https://baidu.com', 'Cookie': 'Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1497505637,1498033165,1498120062;' }  
	try:
		data = urllib.urlencode(values)   
		req = urllib2.Request(url, data, headers)   
		response = urllib2.urlopen(req)   
		return response.read()
	except Exception,e:
		#logger.error('opne '+ url + 'error')
		#logger.exception("Exception Logged")  
		return {"status":"Fail", 'message': e}

#从url中提取出host部分，提取失败返回None
def getHost(url, domain = None):
	proto, rest = urllib.splittype(url)
	res, rest = urllib.splithost(rest)
	if not domain and domain in res
		return res

def push(url):
	if not bloom.add(url):
		url_json.append(url)
		host = getHost(url)
		if host != None:
			if not bloom.add(host):
				host_json.append(host)

	
#return <a href> list		
def parser(html_code):
	soup = BeautifulSoup(str(html_code).decode('utf-8'),  "html.parser")
	for a in soup.find_all('a'):
		try:
			push(a['href'])
		except Exception,e:
			pass

	
if __name__ == '__main__':
	#4903885@qq.com  lifei  1985sc.com 1059928888
	#print ip('124.172.243.59')
	parser(open("http://blog.csdn.net", {'host':"test", 'ddlSearchMode':'2'}))
	print url_json
	print host_json
	#print email('4903885@qq.com')
	#print phone('1059928888')

