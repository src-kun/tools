import urllib 
import urllib2 
from cookielib import CookieJar


#https://www.apnic.net/
def get_same(host):
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
		return {"status":"Fail", 'message': e}

if __name__ == '__main__':
	print get_same('www.sdzk.cn')