#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import time
from pybloom import BloomFilter
from scrawler import Crawler
 
class myThread (threading.Thread):
	def __init__(self, threadLock, current_levle, cra, url, data = None):
		threading.Thread.__init__(self)
		self.cra = cra
		self.url = url
		self.data = data
		self.current_levle = current_levle
		self.threadLock = threadLock
		
	def run(self):
		# 获得锁，成功获得锁定后返回True
		# 可选的timeout参数不填时将一直阻塞直到获得锁定
		# 否则超时后将返回False
		
		start(self.current_levle, self.cra, self.url, self.data)
		#threadLock.acquire()
		# 释放锁
		#threadLock.release()
 
def start(current_levle, cra, url, data = None):
	#get request
	current_levle, html = cra.open(current_levle, url)
	#post request
	#html = c.open("http://www.zgyey.com/", data)
	if current_levle != -1:
		cra.parser(current_levle, url, html)
	

def test():
	#http://csdn.net
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	c = Crawler(bloom)
	c.filter = "zgyey.com"
	c.level = 2
	threadLock = threading.Lock()
	threads = []

	c.url[0].append("http://zgyey.com/")
	tmp_url = c.url[0][:]
	for i in range(0, c.level):
		l = len(tmp_url)
		for x in range(l):
			# 创建新线程
			thread = myThread(threadLock, i, c, tmp_url[x])
			# 开启新线程
			thread.start()
			# 添加线程到线程列表
			threads.append(thread)
		# 等待所有线程完成
		for t in threads:
			t.join()
		tmp_url = c.host[0][:]
	print c.url
	print
	print
	print c.host
	print
	print
	print tmp_url
	print "Exiting Main Thread"
	
test()
