#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys

def start_threads(path, func):
	file_object = open(path)
	try:
		for line in file_object:
			if line.rstrip() == '\n':
				break
			t = threading.Thread(target=getIP,args=(line.rstrip().strip('http://').strip('\n'),))#
			t.start()
			sleep(0.05)
	finally:
		file_object.close()