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
		
#检查文件 不存在创建
def chk_file(path):
	if not os.path.exists(path):
		os.mknod(path)

def list_dir(path):
	return os.listdir(path)

def list_dir_nohidden(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			yield f

def read(path):
	lines_arry = []
	file = open(path)
	while True:
		lines = file.readlines(100000)
		if not lines:
			break
		lines_arry.extend(lines)
	return lines_arry

#写文件 text不存在则返回文件句柄
def write(path = None, text = None, pattern = 'a'):
	file_handle = open(path, 'a')
	file_handle.write(text)
	file_handle.close()
	return file_handle