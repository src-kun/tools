#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys,socket

def help():
    print '''getip.py url.txt
	url.txt 每个域名占据一行
'''

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
		if debug:
			print(myaddr[0] + '\t' + url)
		return [0, list(set(myaddr))]
	except Exception,e:
		if debug:
			print('[x]\t' + url)
			print[-1, str(e)]
		return [-1, str(e)]
	
		
		
def start(path):
	file_object = open(path)
	try:
		for line in file_object:
			if line.rstrip() == '\n':
				break
			t = threading.Thread(target=get_ip,args=(line.rstrip().strip('http://').strip('\n'),))
			t.start()
			sleep(0.05)
	finally:
		file_object.close()

def main():
	if len(sys.argv) < 2:
		help()
		exit()
	start(sys.argv[1])

if __name__ == '__main__':
	main()