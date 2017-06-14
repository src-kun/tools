#! usr/bin/python 
#coding=utf-8 

"""
getip.py url.txt

url.txt 每个域名占据一行
"""
import sys, socket  

def getIP(path):
	file_object = open(path)
	try:
		for line in file_object:
			url = line.rstrip().strip('http://').strip('\n')
			if len(url) == 0:
				break
			try:
				myaddr = socket.getaddrinfo(url,'http')[0][4][0]
				print(myaddr + '\t' + url)
			except Exception,e:
				continue
				
	finally:
		file_object.close( )
	

def main():
	getIP(sys.argv[1])

if __name__ == '__main__':
	main()