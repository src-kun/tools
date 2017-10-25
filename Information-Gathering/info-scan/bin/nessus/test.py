#! usr/bin/python 
#coding=utf-8 

import time

from ness6scan import NessusScan
from settings import neseting
targets = ['127.0.0.1', '10.102.16.196', '10.102.16.197', '10.102.16.198', '192.168.230.140']
nesscan = NessusScan('test', neseting.access, neseting.secret)
nesscan.set_text_targets(targets)
nesscan.set_template(nesscan.BASIC_NETWORK_SCAN)
nesscan.set_policy('complex')
nesscan.scan()
print nesscan.is_running()
time.sleep(6)
nesscan.pause()
print nesscan.is_running()
nesscan.resume()
time.sleep(6)
print nesscan.is_running()
nesscan.stop()
print nesscan.is_running()
time.sleep(6)
#print nesscan.get_folders()
#id = nesscan.create_folder('test')['id']
#nesscan.del_floder(id = id)
time.sleep(6)
nesscan.download['path'] = '/tmp/'
nesscan.download['name'] = 'test'
nesscan.download_export()