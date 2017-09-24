#! usr/bin/python 
#coding=utf-8
import sys,socket
from lib.core.log import logger
import tldextract
import urllib

#分解url
#return ('协议', '子域名', '域名', '资源路径', '域名类型')
def separate(url):
	proto, position = urllib.splittype(url)
	domain, resources = urllib.splithost(position)
	tldext = tldextract.extract(url)
	if not tldext.domain:
		domain = None
	elif tldext.suffix:
		if tldext.subdomain:
			domain = '%s.%s.%s'%(tldext.subdomain, tldext.domain, tldext.suffix)
		else:
			domain = '%s.%s'%(tldext.domain, tldext.suffix)
	return (proto, tldext.subdomain, domain, resources, tldext.suffix)