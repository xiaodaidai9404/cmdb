#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
# import json
import simplejson as json
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import Server
import time
from api.views import output_all_server,usage_query_server,output_all_server_for_server_type_num,all_server_num,\
    output_all_server_for_server_type,output_all_server_type,output_all_server_zabbix_info,\
    memory_echarts_info,upload_echarts_info,output_one_server_ip,output_one_server_usage,api_output_server_for_database,\
    api_output_int_server, api_output_ext_server,api_output_test_env

from server.models import RouterInfo
from log.views import logging
from server.cmdb_data_export import ExportData

from django.shortcuts import render_to_response

from user_manager.auth import require_http_users
import datetime


def page_not_found(request):
    return render_to_response('404.html')


def page_error(request):
    return render_to_response('500.html')


@csrf_exempt
def insert_server_info(request):
    """
    处理了一下允许json格式
    正常code:200,异常code:500
    must_value_list不允许为空,返回异常code
    sn默认传空字符串
    """
    must_value_list = ["int_ip","config","disk","cpu","memory","server_type","hostname","service_action"]

    if request.method == 'POST':
        logging.info(request.body)
        req = json.loads(request.body)
        logging.info(req)

    for key in must_value_list:
        if key not in req.keys():
            msg = "%s key没有传入数据,post失败"%(key)
            return HttpResponse(json.dumps({"code": 500, "msg": msg}))

    if Server.objects.filter(ip=req['int_ip']):
        # print "执行更新sql"

        modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        modified_time_stamp = time.mktime(time.strptime(modified_time,"%Y-%m-%d %H:%M:%S"))

        if 'usage' in req.keys():
            Server.objects.filter(ip=req['int_ip']).update(config=req['config'],
                                                           disk_info=req['disk'], memory_info=req['memory'],
                                                           cpu_info=req['cpu'],
                                                           usage=req['usage'], server_type=req['server_type'],
                                                           hostname=req['hostname'], gmt_modified=modified_time,
                                                           service_action=req['service_action'],sn=req['sn'])
        else:
            Server.objects.filter(ip=req['int_ip']).update(config=req['config'],
                                                           disk_info=req['disk'], memory_info=req['memory'],
                                                           cpu_info=req['cpu'],
                                                           server_type=req['server_type'],
                                                           hostname=req['hostname'], gmt_modified=modified_time,
                                                           service_action=req['service_action'],sn=req['sn'])

        database_time = Server.objects.get(ip=req['int_ip']).gmt_modified
        # print database_time,type(database_time)
        database_modified_time = str(database_time).split('+')[0]
        database_modified_time_stamp = time.mktime(time.strptime(database_modified_time,"%Y-%m-%d %H:%M:%S"))

        if  modified_time_stamp == database_modified_time_stamp:
            msg = u"更新数据成功"
            return HttpResponse(json.dumps({"code": 200, "msg": msg}))
        else:
            msg = u"更新数据失败"
            return HttpResponse(json.dumps({"code": 500, "msg": msg}))

    else:
        print "插入数据"
        if 'usage' in req.keys():
            Server.objects.create(ip=req['int_ip'],
                                  config=req['config'], disk_info=req['disk'],
                                  server_type=req['server_type'], memory_info=req['memory'],
                                  cpu_info=req['cpu'], hostname=req['hostname'],
                                  service_action=req['service_action'], usage=req['usage'])
        else:
            Server.objects.create(ip=req['int_ip'],
                                  config=req['config'], disk_info=req['disk'],
                                  server_type=req['server_type'], memory_info=req['memory'],
                                  cpu_info=req['cpu'], hostname=req['hostname'],
                                  service_action=req['service_action'])

        if Server.objects.filter(ip=req['int_ip']):
            msg = u"插入数据成功"
            return HttpResponse(json.dumps({"code": 200, "msg": msg}))
        else:
            msg = u"插入数据失败"
            return HttpResponse(json.dumps({"code": 500, "msg": msg}))


@require_http_users(['ops'])
@login_required()
@csrf_exempt
def add_server(request):
    """
    用于页面上增加服务器
    :param request:
    :return:
    """
    data = request.POST
    server_type = data['server_type']
    hostname = data['hostname']
    ip = data['ip']
    other_ips = data['other_ips']
    config = data['config']
    usage = data['usage']
    disk_info = data['disk_info']
    buy_date =  data['buy_date']
    service_action = data['service_action']

    if service_action == 'test':
        service_action_num = 0
    else:
        service_action_num = 1

    cpu_info = config.split('C')[1].split('G')[0]
    memory_info = config.split('C')[1].split('G')[0]

    return_code = add_server_api(server_type=server_type,hostname=hostname,ip=ip,
                                 other_ips=other_ips,config=config,usage=usage,
                                 disk_info=disk_info,buy_date=buy_date,service_action=service_action_num,
                                 cpu_info=cpu_info,memory_info=memory_info)

    if return_code == "200":
        msg = '新增成功'
    elif return_code == "404":
        msg = '新增失败'
    elif return_code == "500":
        msg = '技术栈已存在'
    else:
        msg = '未知错误'
    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))




@csrf_exempt
def update_server_info(request):
    data = request.POST
    print data
    hostname = data['hostname']
    ip = data['ip']
    other_ips = data['other_ips']
    config = data['config']
    usage = data['usage']
    disk_info = data['disk_info']
    buy_date = data['buy_date']


    if Server.objects.filter(ip=ip):
        # print "执行更新sql"

        modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        modified_time_stamp = time.mktime(time.strptime(modified_time,"%Y-%m-%d %H:%M:%S"))

        print ip,other_ips,config,usage,disk_info
        Server.objects.filter(ip=ip).update(hostname=hostname, other_ips=other_ips, config=config,
                          disk_info=disk_info,
                          usage=usage,gmt_modified=modified_time,buy_date=buy_date )

        database_time = Server.objects.get(ip=ip).gmt_modified
        # print database_time,type(database_time)
        database_modified_time = str(database_time).split('+')[0]
        database_modified_time_stamp = time.mktime(time.strptime(database_modified_time,"%Y-%m-%d %H:%M:%S"))

        if modified_time_stamp == database_modified_time_stamp:
            msg = u"更新数据成功"
            return HttpResponse(json.dumps({"code": 200, "msg": msg}))
        else:
            msg = u"更新数据失败"
            return HttpResponse(json.dumps({"code": 500, "msg": msg}))

    else:
        print ip, other_ips, config, usage, disk_info
        msg = u"更新数据失败"
        return HttpResponse(json.dumps({"code": 500, "msg": msg}))


@require_http_users(['ops'])
@login_required()
@csrf_exempt
def del_server(request):
    data = request.POST
    ip = data['ip']

    Server.objects.get(ip=ip).delete()
    if Server.objects.filter(ip=ip):
        msg = '删除失败'
        return HttpResponse(json.dumps({"code": 500, "msg": msg}))
    else:
        msg = '删除成功'
        return HttpResponse(json.dumps({"code": 200, "msg": msg}))


@csrf_exempt
def http_query_usage(request):
    usage = request.GET['usage']
    List = usage_query_server(usage)
    print List
    return HttpResponse(json.dumps({"data":List}))


@csrf_exempt
def check_server_info(request):
    if "server_type" in request.POST.keys():
        type = request.POST["server_type"]
        if type == "all":
            result = output_all_server()
        else:
            result = output_all_server_for_server_type(type)
        # print result
        return HttpResponse(json.dumps({"code": 200, "result": result}))
    result = output_all_server()
    logging.info(result)
    return HttpResponse(json.dumps({"code": 200, "result": result}))
    # return render(request,"homepage/server_info.html",{'result':result})


def server_info(request):
    return render(request, "homepage/server_info.html")


@login_required()
@csrf_exempt
def index(request):
    all_num = all_server_num()
    im_num = output_all_server_for_server_type_num('im')
    test_num = output_all_server_for_server_type_num('test')
    db_num = output_all_server_for_server_type_num('db')
    result = {'im_num':im_num,'all_num':all_num,'test_num':test_num,'db_num':db_num}
    data = memory_echarts_info()
    upload = upload_echarts_info()

    return render(request, "homepage/index.html",{'result': result,'data': data,'upload': upload})


def select_server_type_list(request):
    result = output_all_server_type()
    print result
    return HttpResponse(json.dumps({"result": result}))


@csrf_exempt
def server_load_info(request):
    return render(request,'homepage/zabbix_info.html')


def all_zabbix_server_info(request):
    result = output_all_server_zabbix_info()
    for item in result:
        item['memory_free_min'] = round(int(item['memory_free_min'])/1024/1024/1024.0, 2)
        item['memory_10min_min'] = round(int(item['memory_10min_min'])/1024/1024/1024.0, 2)
    logging.info("访问zabbix页面")
    return HttpResponse(json.dumps({"code": 200, "result": result}))


@csrf_exempt
def output_ip_for_hostname(request):
    if 'hostname' in request.GET:
        hostname = request.GET['hostname']
        ip = output_one_server_ip(hostname)[0]['ip']
        response = HttpResponse(json.dumps({"hostname": hostname, "ip": ip}))
        return response


@csrf_exempt
def output_usage_for_ip(request):
    if 'int_ip' in request.GET:
        int_ip = request.GET['int_ip']
        usage = output_one_server_usage(int_ip)
        response = HttpResponse(json.dumps({"usage": usage}))
        return response

def add_server_api(server_type,hostname,ip,other_ips,config,usage,disk_info,buy_date,cpu_info,memory_info,service_action):
    """
    先检查脚本是否存在,不存在则添加
    :param domain_name:
    :param domain_expire_date:
    :param ssl_expire_date:
    :return:
    """
    if Server.objects.filter(ip=ip):
        return "500"
    else:
        Server.objects.create(ip=ip,other_ips=other_ips,config=config,
                          disk_info=disk_info,server_type=server_type,
                          memory_info=memory_info,cpu_info=cpu_info,usage=usage,hostname=hostname,
                          buy_date=buy_date,service_action=service_action)

        if Server.objects.filter(ip=ip):
            return "200"
        else:
            return "404"


@login_required()
@csrf_exempt
def search_database(request):
    data = request.POST
    database = data['database']

    result = api_output_server_for_database(database)
    logging.info(result)
    return HttpResponse(json.dumps({"code": 200, "result": result}))


def output_int_ip(request):
    result = api_output_int_server()
    return HttpResponse(json.dumps({"code":200, "result": result}))


def output_ext_ip(request):
    result = api_output_ext_server()
    return HttpResponse(json.dumps({"code": 200, "result": result}))


def output_test_ip(request):
    result = api_output_test_env()
    return HttpResponse(json.dumps({"code": 200, "result": result}))


@csrf_exempt
def add_mysql_router(request):
    if request.method == "POST":
        data = json.loads(request.body)
        logging.info(data.keys())
        router_name = data['router_name']
        databases = data['databases']
        position = int(data['position'])

        if RouterInfo.objects.filter(router_name=router_name):
            RouterInfo.objects.filter(router_name=router_name).update(databases=databases,position=position)
        else:
            RouterInfo.objects.create(router_name=router_name,databases=databases,position=position)

        return HttpResponse(json.dumps({"code":200}))
    
    if request.method == "GET":
        result = list(RouterInfo.objects.all())
        return HttpResponse(json.dumps({"code":200},{"result":result}))

def router_info(request):
    result = list(RouterInfo.objects.all())
    return render(request, "homepage/router_info.html",{'result': result})

@csrf_exempt
def  export_excel(request):
    if request.method == "POST":
        """
        导出 表格
        """
        data = request.POST
        export_value = data['export_value']
        obj = ExportData(export_value)
        res = obj.queryData()
        obj.judge_file_exist()
        return_code = obj.exportExcel(res)
        if return_code == 1:
            return HttpResponse(json.dumps({"code":500},{"result":"参数错误"}))
        else:
            return HttpResponse(json.dumps({"code":200},{"result":"生成成功"}))
    else:
        return HttpResponse(json.dumps({"code":304},{"result":"方法错误"}))

@login_required()
def excel_download(request):
    filename = "/data/scripts/cmdb.xls"
    the_filename = filename.split("/")[-1]
    excel_file = open(filename, 'rb')
    response = FileResponse(excel_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_filename)
    return response    