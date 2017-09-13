#! usr/bin/python 
#coding=utf-8

import sys,socket
import log


"""
url：需要获取ip的域名
debug：打印信息
num：判断是否为分布式服务器，默认循环三次

return:[0/-1,[address list]/msg]
	0: 正常返回
	-1：失败
	msg：错误信息
"""
def get_ip(url, debug = 1, num = 3):
	try:
		myaddr = []
		for i in range(0, num):
			addr = socket.getaddrinfo(url, 'http')[0][4][0]
			myaddr.append(addr)
		logger.debug(myaddr[0] + '\t' + url)
		return [0, list(set(myaddr))]
	except Exception,e:
		logger.error('get ip error for ' + url + ' host')
		logger.exception("Exception Logged")
		return [-1, str(e)]