#! usr/bin/python 
#coding=utf-8

import os
import platform

from lib.core.settings import hydseting

class Hydra():

	def __init__(self):
		self.__bin_check()
		
	def __bin_check(self):
		os.system('sh %s'%hydseting.install_path)

	def start(self, report_path = None):
		os.system('%s -h '%hydseting.hydra_path);