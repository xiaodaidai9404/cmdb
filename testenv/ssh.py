#/usr/bin/env python
#coding=utf-8

import paramiko
from log.views import logging



def flssh(ip,Command,user,port):
    pkey = paramiko.RSAKey.from_private_key_file('/etc/ansible/id_rsa')
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=ip, port=port, username=user,pkey=pkey)

        logging.info(Command)
        logging.info("ssh connect success")

        stdin, stdout, stderr = ssh.exec_command(Command)

        item_total = ''

        for item in stdout.readlines():
            item_total = item_total + item
        return item_total

        ssh.close()

        return item_total

    except Exception, e:
        return False,e.__str__()