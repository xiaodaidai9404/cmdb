#/usr/bin/env python
#coding=utf-8

import paramiko
import time

def flssh(ip,Command,user,port):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, port, user)

        print "ssh连接成功"

        stdin, stdout, stderr = ssh.exec_command(Command)

        # print stdin.readlines()
        # item_total = stdout.readlines()
        item_total = ''

        for item in stdout.readlines():
            item_total = item_total + item
        return item_total

        ssh.close()

        return item_total

    except Exception, e:
        return False,e.__str__()