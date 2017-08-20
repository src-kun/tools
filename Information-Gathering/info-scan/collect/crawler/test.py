#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import time
from pybloom import BloomFilter
from scrawler import Crawler
 
class myThread (threading.Thread):
	def __init__(self, cra, url, data = None):
		threading.Thread.__init__(self)
		self.cra = cra
		self.url = url
		self.data = data
	def run(self):
		print "Starting " + self.name
		# 获得锁，成功获得锁定后返回True
		# 可选的timeout参数不填时将一直阻塞直到获得锁定
		# 否则超时后将返回False
		#threadLock.acquire()
		start(self.cra, self.url, self.data)
		# 释放锁
		#threadLock.release()
 
def start(cra, url, data = None):
	#get request
	domain, html = cra.open(url)
	#post request
	#html = c.open("http://www.zgyey.com/",data)
	cra.parser(domain, html)
	print cra.url
	print
	print
	print cra.host

def test():
	#http://csdn.net
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	c = Crawler(bloom)
	c.setFilter("zgyey.com")
	#c.setCharset("gb2312")
	#c.setCookies("test")
	threadLock = threading.Lock()
	threads = []
	c.url.append('http://www.zgyey.com/')
	 
	# 创建新线程
	thread1 = myThread(c, "http://www.zgyey.com/")
	# 开启新线程
	thread1.start()
	# 添加线程到线程列表
	threads.append(thread1)
	 
	# 等待所有线程完成
	for t in threads:
		t.join()
	print "Exiting Main Thread"
	
test()
