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


def get_ip(url, pr = 1):
	try:
		myaddr = socket.getaddrinfo(url, 'http')[0][4][0]
		if pr:
			print(myaddr + '\t' + url)
		return [myaddr, url]
	except Exception,e:
		if pr:
			print('[x]\t' + url)
		return [url, ]
	
		
		
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
		file_object.close( )

def main():
	if len(sys.argv) < 2:
		help()
		exit()
	start(sys.argv[1])

if __name__ == '__main__':
	main()