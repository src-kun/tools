#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys

import getIP
import getLocal
import whois

info = [['Domain Name', 'Registrant Contact Email', 'Registrant Organization', 'Registrant', 'Registration Time', 'Name Server'],['Domain Name', 'Tech Organization', 'Admin Organization', 'Admin Name', 'Admin Email', 'Registrant Fax', 'Registrant Phone', 'Registrant Organization', 'Registrant Name', 'Name Server']]

mutex = threading.Lock()

def help():
	print 'scan.py <path:	host list>'

def get_info(url):
	ip = getIP.get_ip(url,0)
	if len(ip) == 2:
		local = getLocal.get_local(ip[0], 0)
		if len(ip) == 2:
			ws = whois.toJson(whois.whois(ip[1], mutex))
			print '*' * 100
			if ws[0] == -1:
				print('%-30s%-30s' % (url ,ws[1]))
				return 
			elif ws[0] == 0:
				print('%-30s%-30s%-20s' % (local[0] ,ip[1], local[1]))
				for key in info[ws[1]['type']]:
					try:
						print('\t%-30s%-30s' % (key ,ws[1][key]))
					except Exception,e:
						print('\t%-30s%-30s' % (str(e).replace("'","")  ,'[x]'))
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
			sleep(0.1)
	finally:
		file_object.close()
	

def main():
	if len(sys.argv) < 2:
		help()
		exit()
	start(sys.argv[1])
	
	
if __name__ == '__main__':
	main()