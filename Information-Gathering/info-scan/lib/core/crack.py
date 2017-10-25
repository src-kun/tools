#! usr/bin/python 
#coding=utf-8

import os

from lib.core.settings import hydseting

class Hydra():

	def __init__(self):
		pass
		
	# target = None, targets_path = None, user_dict_path = None, password_dict_path = None, userpass_dict_path = None, format = None, report_path = None
	# 目标			目标文件批量扫描		用户名字典		密码字典				用户名:密码字典		输出类型		报告路径
	def start(self, 
				target = None, 
				targets_path = None, 
				user = None, 
				user_dict_path = None, 
				password = None,
				password_dict_path =None, 
				userpass_dict_path = None,
				port = None,
				proto = None,
				format = 'json', 
				report_path = None):
		bash = hydseting.hydra_path + ' '
		
		#设置爆破目标
		if targets_path:
			bash += '-M %s '%targets_path
		else:
			bash += '%s '%target
		
		#设置用户:密码字典
		if userpass_dict_path:
			bash += '-C %s '%userpass_dict_path
		else:
			#设置用户字典
			if user_dict_path:
				bash += '-L %s '%user_dict_path
			elif user:
				bash += '-l %s '%user
			
			#设置密码字典
			if password_dict_path:
				bash += '-P %s '%password_dict_path
			elif password:
				bash += '-p %s '%password
		
		if report_path:
			bash += '-o %s '%hydseting.report_path
			if format:
				bash += '-b %s '%format
		
		if port:
			bash += '-s %s '%port
			
		if proto:
			bash += '%s'%proto
		bash = 'cd ' + hydseting.restore + ' && ' + bash
		os.system(bash)
	
	def restore(self, restore_path):
		bash = hydseting.hydra_path + ' ' + '-R ' + restore_path
		os.system(bash)