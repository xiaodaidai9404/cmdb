#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
# import json
import simplejson as json
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import time
from django.http import JsonResponse, FileResponse

from log.views import logging

from django.shortcuts import render_to_response

import commands
import os
from models import DbSyncRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")


@csrf_exempt
@login_required()
def mysql_submeter_page(request):
    return render(request, 'homepage/mysql_submeter.html')


@csrf_exempt
@login_required()
def mysql_auto_sql(request):
    data = request.POST

    #sql = data['sql']
    sql = request.POST.getlist("sql")
    sql = "\n".join(sql)
    logging.info(type(sql))
    sql_type = data['sql_type']
    start = data['start']
    end = data['end']

    #logging.info(str(sql)+','+str(sql_type))
    sql = sql.replace('`', '')

    #logging.info('/bin/bash /data/scripts/mysql_submeter/database.sh "%s" "%s" "%s" "%s"' % (sql_type, start, end, sql))
    logging.info('/usr/bin/python3 /data/scripts/mysql_submeter/database.py -t "%s" -st "%s" -et "%s" -sql "%s"' % (sql_type, start, end, sql))
    filename = commands.getoutput('/usr/bin/python3 /data/scripts/mysql_submeter/database.py -t "%s" -st "%s" -et "%s" -sql "%s"' % (sql_type, start, end, sql))

    return HttpResponse(json.dumps({"code": 200, "filename": filename}))


@login_required()
def download_sql(request):
    data = request.GET
    filename = data['filename']
    the_filename = filename.split('/')[-1]
    sql_file = open(filename, 'rb')
    response = FileResponse(sql_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_filename)
    return response

#同步数据库界面
@login_required()
def syncdb_list(request):
    perpage = request.POST.get("perpage", None)
    if perpage is None:
        perpage = 10
    print type(perpage)
    record_list = DbSyncRecord.objects.get_queryset().order_by('-create_time')
    #获取crontab表记录
    cursor = connection.cursor()
    cursor.execute('''select * from djcelery_crontabschedule''')
    crontabs = cursor.fetchall()
    cursor.execute('''select * from djcelery_intervalschedule''')
    intervals = cursor.fetchall()
    if perpage is not None:
         paginator = Paginator(record_list, perpage)  # 每页25条
    else:
         paginator = Paginator(record_list, 10)
    page = request.GET.get('page')
    try:
        records = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)
    mydict = {"records": records, "crontabs": crontabs, "intervals": intervals}
    return render(request, 'homepage/sync_db.html', mydict)

#添加数据库同步
#@login_required()
#def add_syncdb(request):
#    add_fromdb_host = request.POST.get("add_fromdb_host", "")
#    add_fromdb_port = request.POST.get("add_fromdb_port", "") 
#    add_todb_host = request.POST.get("add_todb_host", "")
#    add_todb_port = request.POST.get("add_todb_port", "")
#    issyncdata = request.POST.get("issyncdata", "")
#    add_fromdatabase = request.POST.get("add_fromdatabase", "")
#    add_fromdb_tables = request.POST.get("add_fromdb_tables", '')
#    add_todatabase = request.POST.get("add_todatabase", "")
#    pattern = request.POST.get("add_pattern", "")
#    crontab_task = request.POST.get("add_crontab_task", "")
#    operator = request.POST.get("add_operator", "")
#    sync_commands = 'sh /data/scripts/sync_db.sh %s %s %s %s %s %s "%s" %s "%s"' %(add_fromdb_host, add_fromdb_port, add_todb_host, add_todb_port, add_fromdatabase, add_todatabase, add_fromdb_tables, pattern, issyncdata)
#    #return_detail = commands.getoutput(sync_commands)
#    return_detail = ""
#    print sync_commands
#    #定时执行不为空，则向crontab添加任务
#    if crontab_task != "":
#        sync_commands = crontab_task + ' /bin/bash /data/scripts/sync_db.sh %s %s %s %s %s %s "%s" %s "%s"' %(add_fromdb_host, add_fromdb_port, add_todb_host, add_todb_port, add_fromdatabase, add_todatabase, add_fromdb_tables, pattern, issyncdata)
#        #final_commands = 'sh /data/scripts/addcrontabtask.sh ' + "'" + sync_commands + "'"
#        #print final_commands
#        return_detail = os.system("sh /data/scripts/addcrontabtask.sh " + "'" + sync_commands + "'")
#        if int(return_detail) == 0:
#            return_detail = "success"
#        else:
#            return_detail = "error"
#    else:
#        return_detail = commands.getoutput(sync_commands)    
#    #print return_detail
#    if re.search('error', return_detail, re.IGNORECASE):
#        code = "404"
#    else:
#        DbSyncRecord.objects.create(from_dbhost=add_fromdb_host, from_dbport=add_fromdb_port, to_dbhost=add_todb_host, to_dbport=add_todb_port, from_database=add_fromdatabase, to_database=add_todatabase, tables=add_fromdb_tables, pattern=pattern, crontab_task=crontab_task, operator=operator)
#        code = "200" 
#    print code
#    return HttpResponse(json.dumps({"code": code, "return_detail": return_detail})) 

def add_syncdb(request):
    add_fromdb_host = request.POST.get("add_fromdb_host", "")
    add_fromdb_port = request.POST.get("add_fromdb_port", "")
    add_todb_host = request.POST.get("add_todb_host", "")
    add_todb_port = request.POST.get("add_todb_port", "")
    issyncdata = request.POST.get("issyncdata", "")
    add_fromdatabase = request.POST.get("add_fromdatabase", "")
    add_fromdb_tables = request.POST.get("add_fromdb_tables", '')
    add_todatabase = request.POST.get("add_todatabase", "")
    pattern = request.POST.get("add_pattern", "")
    add_task_name = request.POST.get("add_task_name", "")
    add_task_name = add_task_name + "-" + add_fromdb_host +":"+ add_fromdb_port + "->" + add_todb_host +":"+ add_todb_port
    add_task = request.POST.get("add_task", "")
    enabled = "1"
    total_run_count = "0"
    date_changed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    add_task_description = request.POST.get("add_task_description", " ")
    add_type = request.POST.get("add_type", " ") #0循环 1定时 2立即 
    add_crontab = request.POST.get("crontab_id", None)
    add_interval = request.POST.get("interval_id", None)
    if len(add_crontab) != 0:
        add_crontab_id = add_crontab.split("-")[0]
        crontab_task = add_crontab.split("-")[1]
    if len(add_interval) !=0:
        add_interval_id = add_interval.split("-")[0]
        internal_task = add_interval.split("-")[1]
    args = "[" + "\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"" %(add_fromdb_host, add_fromdb_port, add_todb_host, add_todb_port, add_fromdatabase, add_todatabase, add_fromdb_tables, pattern, issyncdata) + "]"
    kwargs = "{}"
    operator = request.POST.get("add_operator", "")
    if add_type == "2":
        #立即执行
        sync_commands = 'sh /data/scripts/sync_db.sh %s %s %s %s %s %s "%s" %s "%s"' %(add_fromdb_host, add_fromdb_port, add_todb_host, add_todb_port, add_fromdatabase, add_todatabase, add_fromdb_tables, pattern, issyncdata)
        return_detail = commands.getoutput(sync_commands)
    elif add_type == "0":
        #循环执行
        sql = "insert into djcelery_periodictask(name, task, args, kwargs, enabled, total_run_count, date_changed, description, crontab_id, interval_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)" %(add_task_name, add_task, args, kwargs, enabled, total_run_count, date_changed, add_task_description, 'NULL', add_interval_id)
        cursor = connection.cursor()
        cursor.execute(sql)
        return_detail = "success"
    elif add_type == "1":
        #定时执行
        sql = "insert into djcelery_periodictask(name, task, args, kwargs, enabled, total_run_count, date_changed, description, crontab_id, interval_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)" %(add_task_name, add_task, args, kwargs, enabled, total_run_count, date_changed, add_task_description, add_crontab_id, 'NULL')
        cursor = connection.cursor()
        cursor.execute(sql)
        return_detail = "success"
    else:
        return_detail = "add_type paras error"

    if re.search('error', return_detail, re.IGNORECASE):
        code = "404"
    else:
        if add_type == "2":
            crontab_task = ''
        else:
            if len(add_crontab) != 0:
                crontab_task = add_crontab.split("-")[1]
            if len(add_interval) !=0:
                crontab_task = add_interval.split("-")[1]
        DbSyncRecord.objects.create(from_dbhost=add_fromdb_host, from_dbport=add_fromdb_port, to_dbhost=add_todb_host, to_dbport=add_todb_port, from_database=add_fromdatabase, to_database=add_todatabase, tables=add_fromdb_tables, pattern=pattern, crontab_task=crontab_task, operator=operator)
        code = "200"
    return HttpResponse(json.dumps({"code": code, "return_detail": return_detail}))

#删除同步记录
def delete_records(request):
    delete_id = request.POST.get("delete_id", "") 
    DbSyncRecord.objects.filter(id=delete_id).delete()
    code = "200"
    return HttpResponse(json.dumps({"code": code}))
