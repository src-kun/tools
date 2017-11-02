#! usr/bin/python 
#coding=utf-8 
from lib.utils.common import current_path
from lib.utils.common import chk_file
from lib.utils.common import chk_dir

#项目基本信息
VERSION = "1.1.9.3"
author = """zk
"""
#项目路径
bash_obj_path = "%s/../../"%current_path()

CONTENT_TYPE = "Content-Type"
CONTENT_JSON = {'Content-Type':'application/json'}
COOKIE = "Cookie"
#定义http请求头
headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
 CONTENT_TYPE:"",
 "Referer":"https://baidu.com",
 COOKIE:" dc_session_id=1502790073620_0.12930882713190395",
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"}

# colorful banner
BANNER = "scrawler"


#ip138 token
token = ""
token = "3340a497676dd872014dff6f3214a8d0"
ip_api = "http://api.ip138.com/query/?"

#logger
import logging 
#TODO 数字
#level = logging.DEBUG
level = logging.INFO
#level = logging.ERROR #发布版本
#路径
log_path = "%slog/"%bash_obj_path

#censys
UID = "dcd61cfe-36b9-40a6-8a8a-21d7f9ccc37d"
SECRET = "HFtjvpfa5vJ0pVY4mZIOWxMfmm4sCr9E"

class Wvseting():
	def __init__(self):
		self.api_key = '1986ad8c0a5b3df4d7028d5f3c06e936c10a743b8beb644cd852d9320bd0e3a4e'
		self.base_url = 'https://10.102.16.196:3443/'
		#self.base_url = 'http://127.0.0.1:8080/'
		
wvseting = Wvseting()

class Maseting():

	ALL_HISTORY = 0
	ALL_GROUP = 0
	#最常见端口
	QUICK_SCAN = '80,8080,3128,8081,9080,1080,21,23,443,69,22,25,110,7001,9090,3389,1521,1158,2100,1433'
	#TODO 全部常见端口
	COMPLEX_SCAN = '80,8080,3128,8081,9080,1080,21,23,443,69,22,25,110,7001,9090,3389,1521,1158,2100,1433'
	#全端口
	FULL_SCAN = '1-65535'
	
	def __init__(self):
		self.bin = bash_obj_path + 'bin/masscan/'
		self.data =  "%sdata/masscan/"%bash_obj_path
		self.lock_path = self.bin + 'lock'
		self.install_path = self.bin + 'install'
		#执行脚本
		self.masscan_shell = '%s %s -p%s --banners --rate 10000 --adapter-ip 192.168.1.105 -oJ %s --wait=3 > /dev/null 2>&1'
		#物理路径
		self.masscan_path = self.bin + 'masscan'
		#输出的报告路径
		self.report_path = self.data + 'report/'
		#扫描记录map文件
		self.map_path = self.data + '.masscan'
		self.group_path =  self.data + '.group'
		self.history_format = "{'name':'%s', 'scan':{'token':'%s', 'target':{'ip':'%s', 'port':'%s'},'time':%s}, 'group:{id':'%s','name':'%s'}}\n"
		self.group_format = "{'id':'%s', 'name':'%s', 'time':%s}\n"
		self.map_handle = None
		self.group_handle = None
		self.main()

	def main(self):
		self.__check_env()
		self.__init_var()
	
	#检查调用时的所需环境
	def __check_env(self):
		#检测masscan文件夹
		chk_dir(self.data)
		#检查结果导出路径
		chk_dir(self.report_path)
		#检查map文件
		chk_file(self.map_path)
		#检查group文件
		chk_file(self.group_path)


	def __init_var(self):
		self.map_handle = open(self.map_path, 'r+')
		self.group_handle = open(self.group_path, 'r+')

	def __del__( self ):
		self.map_handle.close()
		self.group_handle.close()

maseting = Maseting()

class Hydseting():
	
	def __init__(self):
		self.data =  bash_obj_path + 'data/hydra/'
		self.bin = bash_obj_path + 'bin/hydra/'
		self.install_path = self.bin + 'install'
		self.hydra_path = self.bin + 'hydra'
		self.hydra_path = 'hydra'
		self.lock_path = self.bin + 'lock'
		self.restore =  self.data + 'restore/'
		self.report_path = self.data + 'report'
		self.user_dict_path = self.data + 'dict/user.list'
		self.password_dict_path =  self.data + 'dict/password.list'
		chk_dir(self.report_path)
		chk_dir(self.restore)
		
hydseting = Hydseting()