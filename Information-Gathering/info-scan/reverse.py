#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2 
from html.parser import HTMLParser

test = {'status':'Success','domain':'sdzk.cn', 'register name':'山东省教育招生考试院', 'pthone': '', 'register trader':'北京中科三方网络技术有限公司', 'register date':'2003-03-10', 'over date':'2021-04-22'}
	

def open(url, values):
	headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' ,'Referer': 'https://baidu.com', 'Cookie': 'Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1497505637,1498033165,1498120062;' }  
	try:
		data = urllib.urlencode(values)   
		req = urllib2.Request(url, data, headers)   
		response = urllib2.urlopen(req)   
		return response.read()
	except Exception,e:
		return {"status":"Fail", 'message': e}
"""
ip: 需要反查域名的IP地址

return format {'status': 'Success', 'domain': ['http://bizreg.winshang.com', 'http://winshang.com', ...]}
"""
def ip(ip):
	try:
		response = eval(open('http://www.webscan.cc', {'action':'query', 'ip':ip}))
		domains = []
		for res in response:
			if res['domain'] != None:
				domains.append(res['domain'].replace("\\",""))
		return {'status':'Success', 'domain':domains}
	except Exception,e:
		return {"status":"Fail", 'message': e}
	
def name(name):
	text = open('http://whois.chinaz.com/reverse', {'host':'e37_laisq@sdzs.gov.cn', 'ddlSearchMode':'1'})
	return text
	
def email(email):
	print test
	
def phone(name):
	print test
	
if __name__ == '__main__':
	print name('124.172.243.59')