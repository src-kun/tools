#! usr/bin/python 
#coding=utf-8 
from lib.utils.common import current_path

#项目基本信息
VERSION = "1.1.9.3"
author = """zk
"""
#项目路径
bash_obj_path = "%s/../../"%current_path()

#定义http请求头
headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
 "Referer":"https://baidu.com",
 "Cookie":" dc_session_id=1502790073620_0.12930882713190395",
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

class Maseting():
	
	
	def __init__(self):
		#masscan
		#执行脚本
		self.masscan_shell = '%s %s -p%s --banners --rate 10000 --adapter-ip 192.168.1.105 -oJ %s --wait=3 > /dev/null 2>&1'
		#物理路径
		self.masscan_path = "%sbin/masscan/masscan"%bash_obj_path
		#输出的报告路径
		self.masscan_report_path = "%sdata/masscan_report/"%bash_obj_path
		#扫描记录map文件
		self.masscan_report_map_path = "%sdata/masscan_report/.masscan"%bash_obj_path
		self.map_handle = None
		self.main()

	def main(self):
		self.__check_env()
		self.__init_var()
	
	#检查调用时的所需环境
	def __check_env(self):
		from lib.utils.common import chk_file
		from lib.utils.common import chk_dir
		#检测masscan report 文件夹 不存在则创建
		chk_dir(self.masscan_report_path)
		#检查map文件 不存在则创建
		chk_file(self.masscan_report_map_path)

	def __init_var(self):
		self.map_handle = open(self.masscan_report_map_path, 'a')
		

maseting = Maseting()