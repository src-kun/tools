#! usr/bin/python 
#coding=utf-8 
import urllib 
import urllib2 
from cookielib import CookieJar
import log

logger = log.getLogger()

#https://www.apnic.net/
def get_same(host):
	if cmp(host,'5aaa.com') == 0:
		return {'status': 'Success', 'domainArray': [['5aaa.com', ''], ['job.5aaa.com', ''], ['www.5aaa.com', ''], ['www.5aaa.edu.cn', ''], ['zs.5aaa.com', ''], ['zs.5aaa.edu.cn', '']], 'lastScrape': '2017-06-21 07:02:24', 'remoteAddress': '5aaa.com', 'resultsMethod': 'database', 'remoteIpAddress': '114.247.160.100', 'domainCount': '6'}
	elif cmp(host,'github.com') == 0:
		return {'status': 'Success', 'domainArray': [['github.com', '']], 'lastScrape': '2017-03-28 09:27:51', 'remoteAddress': 'github.com', 'resultsMethod': 'database', 'remoteIpAddress': '192.30.255.113', 'domainCount': '1'}
	elif cmp(host,'baidu.com') == 0:
		return {'status': 'Success', 'domainArray': [['arsel.thecrazyfeed.com', ''], ['baidu.com', ''], ['baidu.com.cn', ''], ['ipv6.baidu.com', ''], ['wn.com', ''], ['www.cheapbags.co', ''], ['www.justforcamping.com', ''], ['www.ksangphotography.com', ''], ['www.realestatecroatia.com', ''], ['www.sciencedirect.com', ''], ['www.sunnymob.com', '']], 'lastScrape': '2017-05-15 04:56:55', 'remoteAddress': 'baidu.com', 'resultsMethod': 'database', 'remoteIpAddress': '220.181.57.217', 'domainCount': '11'}
	url = 'http://domains.yougetsignal.com/domains.php'   
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
	values = {'remoteAddress' : host,   
			  'key' : '' }
	headers = { 'User-Agent' : user_agent }  
	try:
		data = urllib.urlencode(values)   
		req = urllib2.Request(url, data, headers)   
		response = urllib2.urlopen(req)   
		return eval(response.read())
	except Exception,e:
		logger.error('get ' + host + ' same domains error')
		return {"status":"Fail", 'message': e}

if __name__ == '__main__':
	print get_same('www.sdzk.cn')