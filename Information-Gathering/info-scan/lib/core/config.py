#encoding:utf-8
#name:mod_config.py

import ConfigParser
import os

#获取config配置文件
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
	#得到当前文件模块目录
    path = os.path.split(os.path.realpath(__file__))[0] + '/../../config/config.ini'
    config.read(path)
    return config.get(section, key)


#print getConfig("http_header", "header")