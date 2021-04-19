#!/usr/bin/python env
#coding=utf-8

from zabbix.views import zabbix_api
from api.views import output_all_server_ip
from zabbix.models import Zabbix
from clry.celery import Celery
# from clry.celery import Celery, group, chain
from zabbix.views import auth,monitory_url_make
from clry.celery import app
from log.views import logging
import time


@app.task
def zabbix_cron():
    """
    内存剩余取最小值
    负载取最大值,所以分开处理
    :return:
    """
#    logging.info("aaa")
    zabbix_url = "http://zabbix.ipaychat.com/api_jsonrpc.php"
    fuliao_auth_code = auth()
    memory_item = "vm.memory.size[available]"
    load_item = "system.cpu.load[percpu,avg1]"
    server_list = output_all_server_ip()
    white_iplist = ['127.0.0.1']
    for item in server_list:
        ip = item['ip']
        print 'ip{ip}开始执行'.format(ip=ip)
        #logging.info('ip{ip}开始执行'.format(ip=ip))
        if ip not in white_iplist:
         #   logging.info('ip{ip}'.format(ip=ip))
            zabbix = zabbix_api(ip, memory_item, fuliao_auth_code, zabbix_url)
            try:
                memory_list = zabbix.get_memory_history_data()
                memory = sorted([memory_list[i]['value'] for i in range(0, len(memory_list))])[0]
                memory_10min_list = zabbix.get_memory_history_data_10min()
                memory_10min = sorted([memory_10min_list[i]['value'] for i in range(0, len(memory_10min_list))])[0]
          #      logging.info('ip{ip}内存{memory}'.format(ip=ip, memory=memory))
                zabbix = zabbix_api(ip, load_item, fuliao_auth_code, zabbix_url)
                load_list = zabbix.get_load_history_data()
                load = sorted([load_list[i]['value'] for i in range(0, len(load_list))])[-1]
                load_10min_list = zabbix.get_load_history_data_10min()
                load_10min = sorted([load_10min_list[i]['value'] for i in range(0, len(load_10min_list))])[-1]
           #     logging.info('ip{ip}负载{load}'.format(ip=ip, load=load))
                server_type = item['server_type']
                print 'ip{ip}的内存剩余为{memory},负载为{load}'.format(ip=ip, memory=memory, load=load)
            #    logging.warning('ip{ip}的内存剩余为{memory},负载为{load}'.format(ip=ip, memory=memory, load=load))
                modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if Zabbix.objects.filter(ip=ip):
                    Zabbix.objects.filter(ip=ip).update(server_type=server_type, memory_free_min=memory,
                                                        upload_max=load,memory_10min_min=memory_10min,
                                                        upload_10min_max=load_10min,gmt_modified=modified_time)
                else:
                    Zabbix.objects.create(ip=ip, server_type=server_type,
                                          memory_10min_min=memory_10min,upload_10min_max=load_10min,
                                          memory_free_min=memory, upload_max=load)
            except Exception as e:
                print e


@app.task
def zabbix_url_cron():
    """
    往数据库里插入监控url
    :return:
    """
    server_list = output_all_server_ip()
    for item in server_list:
        ip = item['ip']
        try:
            monitor_url = monitory_url_make(ip)
            modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            Zabbix.objects.filter(ip=ip).update(zabbix_url=monitor_url,gmt_modified=modified_time)
        except Exception as e:
            logging.info(e)
        print 'ip{ip}的监控url已生成'.format(ip=ip)
        #logging.info('ip{ip}的监控url已生成'.format(ip))
