#! usr/bin/python 
#coding=utf-8 

from awvscan import WvsScan

base_url = 'https://10.102.16.196:3443/'
api_key = '1986ad8c0a5b3df4d7028d5f3c06e936c10a743b8beb644cd852d9320bd0e3a4e'

wvscan = WvsScan(api_key, base_url)
#wvscan.scan(targets, wvscan.FULL_SCAN, '28pc.com', launch_now = True)
#wvscan.clean_targets()
#wvscan.clean_scans(group_name = '28pc.com')
#print wvscan.getGroupByName('test')
#print len(wvscan.get_targets(group_id = '28pc.com', text = '.me'))
#print wvscan.get_scans(group_name = '28pc.com', status = wvscan.SCAN_STATUS_PROCESSING)
#wvscan.stop()