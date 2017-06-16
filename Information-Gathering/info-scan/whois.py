#! usr/bin/python 
#coding=utf-8 
import os,sys
import json

def whois(host):
	output = os.popen('whois ' + host.strip('http://').strip('https://').strip('www.'))
	return output.read()

def toJson(result):
	js = {}
	start_index = result.index('Domain Name:')
	end_index = result.index('DNSSEC: unsigned')
	if result.find('Domain Name:', start_index + 1) != -1:
		start_index = result.find('Domain Name:', start_index + 1)
	text = result[start_index:end_index]
	tmp = 0
	while tmp != -1:
		index = text.find('\n', tmp + 1)
		line = text[tmp:index].strip('\n').split(': ')
		if len(line) == 2:
			js[line[0]] = line[1]
		tmp = index
	return  js

if __name__ == '__main__':
	print toJson(whois(sys.argv[1]))['Domain Name']

