#! usr/bin/python 
#coding=utf-8

import logging  
import logging.config
import os  
import time

level = logging.DEBUG
#level = logging.ERROR #发布版本

def getFiltName():
	ISOTIMEFORMAT='%Y-%m-%d'
	return time.strftime( ISOTIMEFORMAT, time.localtime())
	
def getLogger():  
    # 创建一个logger,可以考虑如何将它封装  
    logger = logging.getLogger('mylogger')  
    logger.setLevel(level)  
      
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler(os.path.join(os.getcwd(), '../log/' + getFiltName() + '.log'))  
    fh.setLevel(level)  
      
    # 再创建一个handler，用于输出到控制台  
    ch = logging.StreamHandler()  
    ch.setLevel(level)  
      
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  
      
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)  
      
    # test  
    #logger.info('hello world, i\'m log helper in python, may i help you')  
    return logger  