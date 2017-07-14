#! usr/bin/python 
#coding=utf-8 

import urllib 
import urllib2 
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import sys
sys.path.append("../../")
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
		
#return <a herf> list		
def parser(html_code):
	json = []
	soup = BeautifulSoup(str(html_code).decode('utf-8'),  "html.parser")
	
	for a in soup.find_all('a'):
		try:
			print a
		except Exception,e:
			logger.warn(e)
			pass
	return json
		
	
if __name__ == '__main__':
	#4903885@qq.com  lifei  1985sc.com 1059928888
	#print ip('124.172.243.59')
	print parser(open("http://blog.csdn.net"))
	#print email('4903885@qq.com')
	#print phone('1059928888')

	

	
	
	
	

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
