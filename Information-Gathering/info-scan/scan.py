#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys

import getIP
import getLocal

def get_info(url):
	ip = getIP.get_ip(url,0)
	if len(ip) == 2:
		local = getLocal.get_local(ip[0], 0)
		if len(ip) == 2:
			print('%-30s%-30s%-20s' % (local[0] ,ip[1], local[1]))
			#print  local[0] + '\t\t' + ip[1] + '\t\t\t' + local[1]
		else:
			print '[x] ' + local[0]
	else:
		print '[x] ' + ip[0]
	

def start(path):
	file_object = open(path)
	try:
		for line in file_object:
			if line.rstrip() == '\n':
				break
			t = threading.Thread(target=get_info,args=(line.rstrip().strip('http://').strip('\n'),))
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