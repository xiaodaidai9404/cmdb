#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
import json
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
import datetime

from server.models import Server
from zabbix.models import Zabbix
from tech_stack.models import tech_stack_info
from testenv.models import test_env_info,test_env_history


def output_all_server():
    """
    返回所有服务器
    :return:
    """
    Server_list = list(Server.objects.all().values('ip','other_ips','config','port','usage','disk_info',
                                                   'hostname','sn','buy_date'))
    return Server_list


def output_all_stack():
    """
    返回所有技术栈
    :return:
    """
    stack_list = list(tech_stack_info.objects.all().values('id','name','download_url','info'))
    return stack_list


def output_all_server_ip():
    """
    返回所有服务器的ip和server_type,用于zabbix定时任务
    :return:
    """
    Server_list = list(Server.objects.exclude(server_type__in=['db','test']).values('ip', 'server_type'))
    return Server_list


def output_one_server_ip(name):
    """
    根据传入的hostname返回对应主机的ip
    :param name:
    :return:
    """
    Server_list = list(Server.objects.filter(hostname=name).values('ip'))
    return Server_list


def output_one_server_usage(int_ip):
    """
    根据传入的hostname返回对应主机的ip
    :param name:
    :return:
    """
    Server_list = list(Server.objects.filter(ip=int_ip).values('usage'))
    return Server_list


def output_all_server_type():
    """
    返回所有类型用于申请服务器选择select列表
    :return:
    """
    Server_list = list(Server.objects.all().values('server_type'))
    L1 = list(set([ x['server_type'] for x in Server_list ]))
    return L1


def output_all_server_for_server_type(server_type):
    """
    返回某个类型的服务器
    :return:
    """
    Server_list = list(Server.objects.filter(server_type=server_type).values('ip','other_ips','config','port','usage','disk_info','hostname','buy_date'))
    return Server_list


def output_all_server_for_server_type_num(server_type):
    """
    返回某个类型的服务器总数,如aliyun或者idc
    :param server_type:
    :return:
    """
    Server_list = Server.objects.filter(server_type=server_type).values('ip')
    num = len(Server_list)
    return num


def all_server_num():
    """
    返回服务器总量
    :return:
    """
    Server_list = Server.objects.all().values('ip')
    num = len(Server_list)
    return num


def usage_query_server(usage):
    """
    传入服务器应用,返回该应用的所有服务器ip
    :param usage:
    :return:
    """
    Server_list = output_all_server()
    usage_server_list = [ x['ip'] for x in Server_list if usage in x['usage'].split(',') ]
    return usage_server_list


def outip_query_server(outip):
    """
    传入外网ip,返回该服务器内网ip
    :param outip:
    :return:
    """
    Server_list = output_all_server()
    for x in Server_list:
        if outip in x['other_ips']:
            ip = x['ip']
    if ip:
        return ip
    else:
        return "error"


def output_one_server_upload(ip):
    """
    传入ip，返回ip和upload最大值
    :param ip:
    :return:
    """
    Server_list = list(Zabbix.objects.filter(ip=ip).values('ip', 'upload_max'))
    return Server_list


def output_all_server_zabbix_info():
    """
    返回ip,upload_max,memory_free_min列表用于展示
    :return:
    """
    Server_list = list(Zabbix.objects.all().values('ip','memory_free_min','upload_max','zabbix_url','memory_10min_min','upload_10min_max'))
    return Server_list


def output_zabbix_url(ip):
    Server_list = list(Zabbix.objects.filter(ip=ip).values('zabbix_url'))
    return Server_list[0]['zabbix_url']


def add_stack_api(name,download_url,info):
    """
    先检查脚本是否存在,不存在则添加
    :param domain_name:
    :param domain_expire_date:
    :param ssl_expire_date:
    :return:
    """
    if tech_stack_info.objects.filter(name=name):
        return "500"
    else:
        tech_stack_info.objects.create(name=name,download_url=download_url,info=info)
        if tech_stack_info.objects.filter(name=name):
            return "200"
        else:
            return "404"


def update_stack_api(name,download_url,info):
    """
    更新技术栈
    :param name:
    :param download_url:
    :param info:
    :return:
    """
    tech_stack_info.objects.filter(name=name).update(download_url=download_url,info=info)
    return "200"


def memory_echarts_info():
    """
    返回最小内存,用于饼图
    :return:
    """
    server_list = list(Zabbix.objects.all().values('memory_free_min'))
    server_dict = {"memory_gt_8g": 0, "memory_gt_4g": 0, "memory_le_4g": 0}
    print server_list
    for item in server_list:
        if int(item['memory_free_min']) > 8589934592:
            server_dict['memory_gt_8g'] = int(server_dict['memory_gt_8g'])+1
        elif int(item['memory_free_min']) > 4294967296 and int(item['memory_free_min']) < 8589934592:
            server_dict['memory_gt_4g'] = int(server_dict['memory_gt_4g'])+1
        else:
            server_dict['memory_le_4g'] = int(server_dict['memory_le_4g'])+1

    return server_dict


def upload_echarts_info():
    """
    返回最大负载,用于饼图
    :return:
    """
    server_list = list(Zabbix.objects.all().values('upload_max'))
    server_dict = {"upload_gt_5": 0, "upload_gt_1": 0, "upload_le_1": 0}
    for item in server_list:
        if int(float(item['upload_max'])) >= 5:
            server_dict['upload_gt_5'] = int(server_dict['upload_gt_5'])+1
        elif int(float(item['upload_max'])) >=1 and int(float(item['upload_max'])) < 5:
            server_dict['upload_gt_1'] = int(server_dict['upload_gt_1'])+1
        else:
            server_dict['upload_le_1'] = int(server_dict['upload_le_1'])+1

    return server_dict


def output_test_env_info():
    """
    返回测试环境信息用于页面展示
    :return:
    """
    env_list = list(test_env_info.objects.filter(status=0).values('env_name', 'project_name', 'project_leader', 'project_developer',
                                                       'end_time', 'status'))
    return env_list


def output_env_info_for_history(env_name):
    """
    返回测试环境信息用于项目结束时记录进日志
    :return:
    """
    env_list = list(test_env_info.objects.filter(env_name=env_name).values('project_name', 'project_leader',
                                                                           'project_developer', 'start_time'))
    return env_list


def api_test_env_release(env_name):
    test_env_info.objects.filter(env_name=env_name).update(project_name='', project_leader='',
                                                           project_developer='', status=1,
                                                           start_time='2099-01-01 00:00:00', end_time='1999-01-01 00:00:00')
    return 200


def api_test_env_allow(env_name, project_name, project_leader, project_developer, start_time, end_time):
    status = list(test_env_info.objects.filter(env_name=env_name).values('status'))[0]['status']
    if status == 0:
        return "500"
    else:
        test_env_info.objects.filter(env_name=env_name).update(project_name=project_name,
                                                               project_leader=project_leader,
                                                               project_developer=project_developer,
                                                               start_time=start_time,
                                                               end_time=end_time,
                                                               status=0)
        return "200"


def api_test_env_add(env_name):
    """
    新增测试环境
    :param env_name:
    :param project_name:
    :param project_leader:
    :param project_developer:
    :param start_time:
    :param end_time:
    :return:
    """
    if test_env_info.objects.filter(env_name=env_name):
        return "500"
    else:
        test_env_info.objects.create(env_name=env_name, status=0)
        if tech_stack_info.objects.filter(env_name=env_name):
            return "200"
        else:
            return "404"


def api_update_test_env_info(env_name,project_name,project_leader,project_developer):
    """
    修改项目名称,项目经理,开发人员
    :param env_name:
    :param project_name:
    :param project_leader:
    :param project_developer:
    :return:
    """
    test_env_info.objects.filter(env_name=env_name).update(project_name=project_name, project_leader=project_leader,
                                                           project_developer=project_developer)
    return 200


def api_test_env_histroy_insert(env_name,project_name,project_leader,project_developer,spend_time):
    """
    项目结束释放环境时，将项目信息插入历史表
    :param env_name:
    :param project_name:
    :param project_leader:
    :param project_developer:
    :param spend_time:
    :return:
    """
    spend_time = int(spend_time)
    test_env_history.objects.create(env_name=env_name, project_name=project_name, project_leader=project_leader,
                                    project_developer=project_developer, spend_time=spend_time)


def free_test_env_api():
    """
    返回空闲的环境列表
    :return:
    """
    free_env_list = list(test_env_info.objects.filter(status=1).values('env_name'))
    return free_env_list


def api_env_select_end_time(env_name):
    """
    返回该项目环境的时间
    :param env_name:
    :return:
    """
    env_list = list(test_env_info.objects.filter(env_name=env_name).values('end_time'))
    return env_list


def api_env_insert_end_time(env_name, end_time):
    """
    项目延时
    :param env_name:
    :param end_time:
    :return:
    """
    test_env_info.objects.filter(env_name=env_name).update(end_time=end_time)
    return 200


def api_env_insert_db_jenkins_build_number(env_name, build_number):
    """
    修改db_jenkins当前构建number
    :param env_name:
    :param build_number:
    :return:
    """
    test_env_info.objects.filter(env_name=env_name).update(db_jenkins_id=build_number)
    return 200


def api_env_insert_java_jenkins_build_number(env_name, build_number):
    """
    修改java_jenkins当前构建number
    :param env_name:
    :param build_number:
    :return:
    """
    test_env_info.objects.filter(env_name=env_name).update(java_jenkins_id=build_number)
    return 200


def api_env_select_db_jenkins_build_number(env_name):
    """
    返回dbjenkins当前的构建id
    :param env_name:
    :return:
    """
    number = list(test_env_info.objects.filter(env_name=env_name).values('db_jenkins_id'))[0]['db_jenkins_id']
    return number


def api_env_select_java_jenkins_build_number(env_name):
    """
    返回javajenkins当前的构建id
    :param env_name:
    :return:
    """
    number = list(test_env_info.objects.filter(env_name=env_name).values('java_jenkins_id'))[0]['java_jenkins_id']
    return number


def api_output_server_for_usage(soft, server_app):
    """
    根据服务器作用返回服务器
    :param soft:
    :return:
    """
    con_str = ","+str(soft)
    server_list = list(Server.objects.filter(Q(usage__startswith=soft) | Q(usage__contains=con_str)).filter(server_app=server_app).values('ip','usage'))
#    Server_list = list(Server.objects.filter(usage__contains=soft).values('ip','usage'))
    return server_list


def api_output_server_for_database(database):
    """
    根据数据库返回对应的服务器
    :param database:
    :return:
    """
    regex_str_1 = database+"$"
    regex_str_2 = database+","
    print regex_str_1,regex_str_2
    db_server_list = output_all_server_for_server_type('db')
    server_list = [[item for item in db_server_list if re.search('%s|%s' % (regex_str_1, regex_str_2), item['usage'])]][0]
    return server_list


def api_output_int_server():
    """
    返回所有内网ip
    :return:
    """
    Server_list = list(Server.objects.filter(~Q(server_type='db')).values('ip'))
    return Server_list


def api_output_ext_server():
    """
    返回所有外网ip
    :return:
    """
    Server_list = list(Server.objects.filter(~Q(other_ips='')).values('other_ips'))
    return Server_list

def api_output_test_env():
    """
    返回测试环境int_ip
    """
    Server_list = list(Server.objects.filter(server_type="test").filter(hostname__contains='test').values("ip"))
    return Server_list


def im_output_server_for_usage(soft, server_app):
    if soft != "msg_sender":
        soft = str(soft)+"_1"
    con_str = ","+str(soft)
    server_list = list(Server.objects.filter(Q(usage__startswith=soft) | Q(usage__contains=con_str)).filter(server_app=server_app).values('ip','usage'))
#    Server_list = list(Server.objects.filter(usage__contains=soft).values('ip','usage'))
    return server_list
