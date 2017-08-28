#!/usr/bin/env python
import subprocess


result_file = "result.txt"
func = 'cmd func'

def write_file(func, result):
    f = file(result_file, "a")
    f.writelines('-'*50+'\n')
    f.writelines(func+'\n')
    f.writelines('-'*50+'\n')
    f.writelines(result+'\n')
    f.writelines('-'*50+'\n')
    f.close()


def exc_cmd(func, cmd):
    try:
        exc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        result = exc.stdout.read()
        write_file(func, result)
    except Exception,e:
        pass


def get_current_user():
    func = '[+] getting current user'
    print func
    cmd = "whoami"
    exc_cmd(func, cmd)


def get_login_user():
    func = '[+] getting current login user'
    print func
    cmd = "who |awk -F ' ' '{print $1,$5}'"
    exc_cmd(func, cmd)


def get_address():
    func = '[+] getting ip address information'
    print func
    cmd = "ifconfig |grep inet |grep -v 127.0.0.1| awk -F ' ' '{print $2}'"
    exc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE )
    result = exc.stdout.readlines()
    for i in result:
        if len(i) < 10:
            result.remove(i) 
    result = str(result)
    write_file(func, result)


def get_release():
    func = '[+] getting system release'
    print func
    cmd = "lsb_release -a"
    exc = exc_cmd(func, cmd)


def get_core_info():
    func = '[+] getting core infomation'
    print func
    cmd = '/usr/bin/uname -a'
    exc = exc_cmd(func, cmd)


def get_passwd():
    func = '[+] getting valid /etc/passwd user'
    print func
    cmd = "cat /etc/passwd | grep /bin/bash"
    exc_cmd(func, cmd)
 

def get_shadow():
    func = '[+] getting valid /etc/shadow content'
    print func
    cmd = "cat /etc/shadow | grep -v '\!\!' | grep -v '\*'"
    exc = exc_cmd(func, cmd)



def get_process():
    func = '[+] getting valid process name'
    print func
    cmd = "netstat -tnlp|grep LISTEN|awk -F ' ' '{print $7}'| cut -d '/' -f 2| cut -d ':' -f 1 | sort -u"
    exc = exc_cmd(func, cmd)



def get_last():
    func = '[+] getting last'
    print func
    cmd = "/usr/bin/last |grep -v reboot | awk -F ' ' '{print $1,$3}'| sort -u | grep -v pts | grep -v :"
    exc_cmd(func, cmd)


def get_crond():
    func = '[+] getting crond'
    print func
    cmd = "/usr/bin/crontab -l"
    exc_cmd(func, cmd)

def get_hosts():
    func = '[+] getting hosts'
    print func
    cmd = "cat /etc/hosts | grep -v 127.0.0.1 | grep -v ::"
    exc_cmd(func, cmd)

    
def get_route():
    func = '[+] getting route table'
    print func
    cmd = "route -n"
    exc_cmd(func, cmd)


def connect_google():
    func = '[+] test to connect google'
    print func
    cmd = "ping -c 2 google.com"
    exc_cmd(func, cmd)


def main():
    try:
        get_current_user()
        get_login_user()
        get_address()
        get_release()
        get_core_info()
        get_passwd()
        get_shadow()
        get_process()
        get_last()
        get_crond()
        get_hosts()
        get_route()
        connect_google() 
    except Exception,e:
        pass 
    
if __name__ == "__main__":
    main()
    print 'result file is ./'+ result_file
