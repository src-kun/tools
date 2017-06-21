#! usr/bin/python 
#coding=utf-8 
import threading
from time import ctime,sleep
import urllib2  
import sys

import getIP
import getLocal
import getSame
import whois

info = [['Domain Name', 'Registrant Contact Email', 'Registrant Organization', 'Registrant', 'Registration Time', 'Name Server'],['Domain Name', 'Tech Organization', 'Admin Organization', 'Admin Name', 'Admin Email', 'Registrant Fax', 'Registrant Phone', 'Registrant Organization', 'Registrant Name', 'Name Server']]

mutex = threading.Lock()

def help():
	print 'scan.py -f <path:	host list>\n\
scan.py -h <host>'

def get_info(url):
	ip = getIP.get_ip(url,0)
	if ip[0] == 0:
		same = getSame.get_same(url)
		local = getLocal.get_local(ip[1][0], 0)
		ws = whois.toJson(whois.whois(url, mutex))
		print '*' * 100
		if len(ip[1]) > 1:
			print 'This domain name is distributed !'
		if ws[0] == -1:
			print('%-30s%-30s' % (url ,ws[1]))
			return 
		elif ws[0] == 0:
			print('%-30s%-30s%-20s' % (local[0] ,url, local[1]))
			for s in same['domainArray']:
				print('\t%-30s%-30s' % ('Reverse IP Domain', s[0]))
			for key in info[ws[1]['type']]:
				try:
					print('\t%-30s%-30s' % (key ,ws[1][key]))
				except Exception,e:
					print('\t%-30s%-30s' % (str(e).replace("'","")  ,'[x]'))

	else:
		print '[x] ' + url + '\terror msg:\t' + ip[1]
	

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
	if len(sys.argv) < 3:
		help()
		exit()
	if cmp(sys.argv[1],'-f') == 0:
		start(sys.argv[2])
	elif cmp(sys.argv[1],'-h') == 0:
		t = threading.Thread(target=get_info,args=(sys.argv[2].rstrip().strip('http://').strip('\n'),))
		t.start()
	else:
		help()
	
	
if __name__ == '__main__':
	main()