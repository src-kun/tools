#! usr/bin/python 
#coding=utf-8 

from pybloom import BloomFilter

from lib.core import scrawler
from lib.connection import connect
from lib.core.log import logger


def crawlerApi(crawler):
	 scrawler.t_crawlerApi(crawler)
	
def test_CrawlerApi():
	#http://csdn.netn
	bloom = BloomFilter(capacity=100000, error_rate=0.001)
	crawler = scrawler.Crawler(bloom)
	crawler.filter = "eastmoney.com"
	crawler.level = 2
	crawler.start_url = "http://www.eastmoney.com/"
	#crawler.proxies = {"type":"socks5", "ip":"192.168.1.206", "port":1080}
	crawlerApi(crawler)
	print crawler.host
	#print crawler.url

test_CrawlerApi()