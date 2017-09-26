#! usr/bin/python 
#coding=utf-8
import sys
import socket
import os

import tldextract
import urllib

#from lib.core.log import logger

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
	
def current_path():
	 return os.path.split(os.path.realpath(__file__))[0]

#检查文件夹 不存在创建
def chk_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)