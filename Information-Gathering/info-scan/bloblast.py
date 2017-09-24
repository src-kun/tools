#! usr/bin/python 
#coding=utf-8 

import sys

from pybloom import BloomFilter

from lib.core import scrawler
from lib.core.scrawler import Crawler
from lib.core.scrawler import t_crawlerApi
from lib.core.log import logger
from lib.core.domain import Network
from lib.core.domain import Censysio
from lib.utils.common import separate

bloom = BloomFilter(capacity=100000, error_rate=0.001)

blob = {'domain':[]}

#域名收集
def domain_collect(filter, url):
	
	crawler = Crawler(bloom)
	(proto, substr, domain, resources, suffix) = separate(url)
	domains = []#Censysio().certificates(filter)['domain']
	crawler.filter = filter
	crawler.level = 3
	crawler.appendDomain(url)
	crawler.start()
	
	#对比两个集合，确认爬虫收集的域名与syscen搜索引擎搜索的域名是否存在差异，如果存在继续爬一次差异的域名
	if domains and crawler.appendDomain(domains):
		crawler.level += 1
		infoMsg = "censys and crawler diff ==> %s"%str(domains)
		logger.info(infoMsg)
		crawler.start()
	return crawler.getHost()['domain']
	
#ip 采集
def ip_collect(domain_arry):
	return Network().ip(domain_arry)

'''file = open('domain')
 
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        print domain_collect(['http', line.replace('\n','')])'''

#print domain_collect('csdn.net','http://www.csdn.net')
blob['domain'].extend(domain_collect('csdn.net','http://www.csdn.net'))
#test = ['www.csdn.net', u'passport.csdn.net', u'passport.csdn.net', u'geek.csdn.net', u'edu.csdn.net', u'bbs.csdn.net', u'blog.csdn.net', u'download.csdn.net', u'ask.csdn.net', u'mall.csdn.net', u'job.csdn.net', u'huiyi.csdn.net', u'cto.csdn.net', u'special.csdncms.csdn.net', u'aws.csdn.net', u'hadoop.csdn.net', u'openstack.csdn.net', u'docker.csdn.net', u'database.csdn.net', u'server.csdn.net', u'security.csdn.net', u'storage.csdn.net', u'special.csdn.net', u'programmer.csdn.net', u'so.csdn.net', u'lib.csdn.net', u'code.csdn.net', u'ems.csdn.net', u'student.csdn.net', u'club.csdn.net', u'visualstudio2017.csdn.net', u'huawei.csdn.net', u'intel.csdn.net', u'ibmuniversity.csdn.net', u'primeton.csdn.net', u'qualcomm.csdn.net', u'qcloud.csdn.net', u'g.csdn.net', u'bss.csdn.net', u'task.csdn.net', u'hc.csdn.net', u'powerlinux.csdn.net', u'ibm.csdn.net', u'vuforia.csdn.net', u'atlassian.csdn.net', u'xamarin.csdn.net', u'ea.csdn.net', u'msdn.csdn.net', u'newsletter.csdn.net', u'letter.csdn.net', u'subject.csdn.net', u'cloud.csdn.net', u'news.csdn.net', u'order.csdn.net', u'www.csdncms.csdn.net', u'photo.csdncms.csdn.net', u'video.csdncms.csdn.net', u'talk.csdncms.csdn.net', u'space.csdncms.csdn.net', u'app.csdncms.csdn.net', u'my.csdn.net', u'events.csdn.net', u'tencent_qcloud.csdn.net', u'articles.csdn.net', u'wiki.csdn.net', u'Atlassian.csdn.net', u'mailfeed.csdn.net', u'hardware.csdn.net', u'con2.csdn.net', u'msg.csdn.net', u'write.blog.csdn.net', u'biz.csdn.net', u'api.csdn.net', u'mobile.csdn.net', u'sd.csdn.net']
blob.update(ip_collect(blob['domain']))
print blob