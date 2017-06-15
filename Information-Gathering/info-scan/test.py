#! usr/bin/python 
#coding=utf-8 
import os

def whois(host):
	output = os.popen('whois ' + host)
	return output.read()

def json(result):
	start = 'Domain Name:'
	start_index = result.index(start)
	end = 'DNSSEC: unsigned'
	end_index = result.index(end)
	print start_index
	print end_index
	print result[start_index:end_index]
json(whois('baidu.com'))