#! usr/bin/python 
#coding=utf-8

import urllib2  
import sys
import log
import threading
import time

logger = log.getLogger()


def help():
    print '''getip.py ip.txt
	ip.txt 每个ip占据一行
'''

def get_local(ip):
	try:
		url ='http://ip.soshoulu.com/ajax/shoulu.ashx?_type=ipsearch&ip='+ ip +'&px=1'
		data = urllib2.urlopen(url)
		logger.debug(ip + '\t' + data.read()[:-10])			
		return [ip, data.read()[:-10]]
	except Exception,e:
		logger.exception("Exception Logged")
		return [ip,]

def start(path):
	file_object = open(path)
	try:
		for line in file_object:
			if line.rstrip() == '\n':
				break
			t = threading.Thread(target=get_local,args=(line.replace(' ',"").strip('\n'),))
			t.start()
			time.sleep(0.05)
	finally:
		file_object.close( )

def main():
	if len(sys.argv) < 2:
		help()
		exit()
	start(sys.argv[1])
	

if __name__ == '__main__':
	main()