#! usr/bin/python 
#coding=utf-8 
import os

from lib.core.log import logger

class Nessus():
	def scan(self):
		print "nessus scan"
	
class Wvs():
	def scan(self):
		print "wvs scan"
	
class Masscan():
	
	def __init__(self):
		self.ip = None
		self.port = None
		self.adapter_ip = None

	#def config(self, ):
	
	#TODO --adapter-ip 
	def scan(self, ip, ports):
		output = os.popen('masscan %s -p%s --banners --rate 10000 --adapter-ip 192.168.1.105 -oJ 1.json --wait=3  > /dev/null 2>&1'%(ip, ports))
