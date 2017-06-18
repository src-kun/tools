#! usr/bin/python 
#coding=utf-8 
import os,sys
import json

suffix = {'.cn':'','.cx':'','.com.cn':'','.wang':'','.cc':'','.xin':'','.com':'','.net':'','.top':'','tech':'','.org':'','red':'','.pub':'','.ink':'','.info':'','.xyz':'','.win':''}

def whois(host):
	hts = host.strip('http://').strip('https://').strip('www.').split('.')
	lens = len(hts)
	#排除.com.cn
	if cmp(hts[lens - 2],'com') == 0:
		host = hts[lens - 3] + '.' + hts[lens - 2] + '.' + hts[lens - 1]
	else:
		host = hts[lens - 2] + '.' + hts[lens - 1]
	output = os.popen('whois ' + host)
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
			try:
				if cmp(line[0], 'Name Server') == 0 and js[line[0]] == None:
						js[line[0]] = line[1]
			except Exception,e:
				print e
				
			else:
				js[line[0]] = line[1]
		tmp = index
	return  js

if __name__ == '__main__':
	print toJson(whois(sys.argv[1]))['Domain Name']

