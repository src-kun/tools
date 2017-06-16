#! usr/bin/python 
#coding=utf-8 
import os,sys

def whois(host):
	output = os.popen('whois ' + host.strip('http://').strip('https://').strip('www.'))
	return output.read()

def json(result):
	js = []
	start_index = result.index('Domain Name:')
	end_index = result.index('DNSSEC: unsigned')
	if result.find('Domain Name:', start_index + 1):
		start_index = result.find('Domain Name:', start_index + 1)
	text = result[start_index:end_index]
	tmp = 0
	while tmp != -1:
		index = text.find('\n', tmp + 1)
		js.append(text[tmp:index].strip('\n').split(': '))
		tmp = index
	return js

print json(whois(sys.argv[1]))
