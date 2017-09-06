#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import log
  
logger = log.getLogger()

def open(url, values):
	headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' ,'Referer': 'https://baidu.com', 'Cookie': 'Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1497505637,1498033165,1498120062;' }  
	try:
		data = urllib.urlencode(values)   
		req = urllib2.Request(url, data, headers)   
		response = urllib2.urlopen(req)   
		return response.read()
	except Exception,e:
		logger.error('opne '+ url + 'error')
		logger.exception("Exception Logged")  
		return {"status":"Fail", 'message': e}
		
		
def parser(html_code):
	#json = {'w30':'', 'domain':'', 'man':'', 'phone':'', 'trader':'', 'dns':[]}
	json = []
	soup = BeautifulSoup(str(html_code).decode('utf-8'),  "html.parser")
	
	for li in soup.find_all('li', 'WhoListCent Wholist clearfix bor-b1s02'):
		for div in  li.find_all('div'):
			try:
				if cmp(div['class'][0], 'listOther') != 0:
					logger.debug(div.get_text())
					json.append(div.get_text())
			except Exception,e:
				logger.warn(e)
				pass
				
	for li in soup.find_all('li', 'WhoListCent Wholist clearfix bor-b1s02 bg-list'):
		for div in  li.find_all('div'):
			try:
				if cmp(div['class'][0], 'listOther') != 0:
					logger.debug(div.get_text())
					json.append(div.get_text())
			except Exception,e:
				logger.warn(e)
				pass
	return json
		
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
		logger.error("reverse ip to host error")
		logger.exception("Exception Logged")
		return {"status":"Fail", 'message': e}
	
def name(n):
	return parser(open('http://whois.chinaz.com/reverse', {'host':n, 'ddlSearchMode':'2'}))
	
def email(e):
	return parser(open('http://whois.chinaz.com/reverse', {'host':e, 'ddlSearchMode':'1'}))
	
def phone(p):
	return parser(open('http://whois.chinaz.com/reverse', {'host':p, 'ddlSearchMode':'3'}))
	
if __name__ == '__main__':
	#4903885@qq.com  lifei  1985sc.com 1059928888
	#print ip('124.172.243.59')
	nam = u'宁夏教育考试院'
	print name(nam) 
	#print email('4903885@qq.com')
	#print phone('1059928888')

	

	
	
	
	

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			