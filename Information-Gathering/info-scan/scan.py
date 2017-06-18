#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys

import getIP
import getLocal
import whois

info = ['Domain Name', 'Registrant Contact Email', 'Registrant Organization', 'Registrant', 'Registration Time']

def get_info(url):
	ip = getIP.get_ip(url,0)
	if len(ip) == 2:
		local = getLocal.get_local(ip[0], 0)
		if len(ip) == 2:
			print ip[1]
			ws = whois.toJson(whois.whois(ip[1]))
			print '*'*100
			print('%-30s%-30s%-20s' % (local[0] ,ip[1], local[1]))
			for key in info:
				try:
					print('\t%-30s%-30s' % (key ,ws[key]))
				except Exception,e:
					print('\t%-30s%-30s' % (str(e).replace("'","")  ,'[x]'))
		else:
			print '[x] ' + local[0]
	else:
		print '[x] ' + ip[0]
	

def start(path):
	file_object = open(path)
	try:
		i =0
		for line in file_object:
			if line.rstrip() == '\n':
				break
			t = threading.Thread(target=get_info,args=(line.rstrip().strip('http://').strip('\n'),))
			t.start()
			sleep(1)
			i += 1
			if i == 3:
				break
	finally:
		file_object.close()
	

def main():
	if len(sys.argv) < 2:
		help()
		exit()
	start(sys.argv[1])
	
	
if __name__ == '__main__':
	main()