#! usr/bin/python 
#coding=utf-8 
import os,sys
import json
from time import sleep

suffix = {'.cn':'','.cx':'','.com.cn':'','.wang':'','.cc':'','.xin':'','.com':'','.net':'','.top':'','.tech':'','.org':'','.red':'','.pub':'','.ink':'','.info':'','.xyz':'','.win':''}

def whois(host, mutex):
	hts = host.strip('http://').strip('https://').strip('www.').split('.')
	lens = len(hts)
	#排除.com.cn
	if cmp(hts[lens - 2],'com') == 0:
		host = hts[lens - 3] + '.' + hts[lens - 2] + '.' + hts[lens - 1]
	elif cmp(hts[lens - 2],'edu') == 0 or cmp(hts[lens - 2],'gov') == 0:
		return ' .gov .edu is not supported '
	else:
		host = hts[lens - 2] + '.' + hts[lens - 1]
	mutex.acquire()#取得锁  
	output = os.popen('whois ' + host)
	result = output.read()
	mutex.release()#释放锁
	return result
	
def toJson(result):
	js = {}
	name_server = {}
	
	start_index = result.find('Domain Name:')
	end_index = result.find('DNSSEC: ')
	if start_index == -1 or end_index == -1:
		end_index = result.find('>>> Last update of whois database:')
		if end_index != -1:
			return [-1, result[0,end_index]]
		return [-1, result]
	if result.find('Domain Name:', start_index + 1) != -1:
		start_index = result.find('Domain Name:', start_index + 1)
	text = result[start_index:end_index]
	tmp = 0
	count = text.count("Name Server:")
	while tmp != -1:
		index = text.find('\n', tmp + 1)
		line = text[tmp:index].strip('\n').split(': ')
		if len(line) == 2:
			if cmp(line[0],'Name Server') == 0 and count > 0:
					name_server[line[0] + str(count)] = line[1]
					count -= 1
			else:
				js[line[0]] = line[1]
		tmp = index
	js['Name Server'] = name_server
	if js['Domain Name'].find('.cn') != -1:
		js['type'] = 0#国内域名
	else:
		js['type'] = 1
	return [0, js]

if __name__ == '__main__':
	print toJson(whois(sys.argv[1]))['Domain Name']

