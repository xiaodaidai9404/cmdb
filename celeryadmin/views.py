from django.shortcuts import render, HttpResponse

# Create your views here.
from django.db import connection
from celery.task.control import  inspect
import socket
import json
import commands
# Create your views here.
def periodictask_list(request):
    cursor = connection.cursor()
    cursor.execute('''select * from djcelery_periodictask''')
    periodictasks = cursor.fetchall()
    #i = inspect()
    #hostname = socket.gethostname()
    #registed_tasks = i.registered_tasks()['celery@192_168_10_10']
    #print registed_tasks
    mydict = {'nav_celery': True, 'nav_celery_periodictasks': True, "periodictasks": periodictasks}
    return render(request, 'homepage/celeryadmin/periodictask.html', mydict)

def crontab_list(request):
    cursor = connection.cursor()
    cursor.execute('''select * from djcelery_crontabschedule''')
    crontabs = cursor.fetchall()
    mydict = {'nav_celery': True, 'nav_celery_crontabs': True, "crontabs": crontabs}
    return render(request, 'homepage/celeryadmin/crontabschedule.html', mydict)

def interval_list(request):
    cursor = connection.cursor()
    cursor.execute('''select * from djcelery_intervalschedule''')
    intervals = cursor.fetchall()
    mydict = {'nav_celery': True, 'nav_celery_intervals': True, "intervals": intervals}
    return render(request, 'homepage/celeryadmin/intervalschedule.html', mydict)

def period_task_open(request):
    task_id = request.POST.get('task_id', None)
    cursor = connection.cursor()
    sql = "update djcelery_periodictask set enabled = 1 where id = %s" %(task_id)
    cursor.execute(sql)
    restart_celery()
    code = "200"
    return HttpResponse(json.dumps({"code": code}))

def period_task_forbidden(request):
    task_id = request.POST.get('task_id', None)
    cursor = connection.cursor()
    sql = "update djcelery_periodictask set enabled = 0 where id = %s" %(task_id)
    cursor.execute(sql)
    restart_celery()
    code = "200"
    return HttpResponse(json.dumps({"code": code}))

def period_task_delete(request):
    task_id = request.POST.get('task_id', None)
    cursor = connection.cursor()
    sql = "delete from djcelery_periodictask where id = %s" %(task_id)
    cursor.execute(sql)
    restart_celery()
    code = "200"
    return HttpResponse(json.dumps({"code": code}))

def restart_celery():
    cmd = 'supervisorctl restart celery_worker'
    print "Restarting celery worker ......"
    commands.getoutput(cmd)
    cmd = 'supervisorctl restart celery_beat'
    print "Restarting celery beat ......"
    commands.getoutput(cmd)

def add_crontab(request):
    add_crontab_minute = request.POST.get("add_crontab_minute", None)
    add_crontab_hour = request.POST.get("add_crontab_hour", None) 
    add_crontab_dayweek = request.POST.get("add_crontab_dayweek", None)
    add_crontab_daymonth = request.POST.get("add_crontab_daymonth", None)
    add_crontab_monthyear = request.POST.get("add_crontab_monthyear", None)
    cursor = connection.cursor()
    sql = "insert into djcelery_crontabschedule(minute, hour, day_of_week, day_of_month, month_of_year) values('%s', '%s', '%s', '%s', '%s')" %(add_crontab_minute, add_crontab_hour, add_crontab_dayweek, add_crontab_daymonth, add_crontab_monthyear)
    cursor.execute(sql)
    code = "200"
    return HttpResponse(json.dumps({"code": code}))

def delete_crontab(request):
    crontab_id = request.POST.get("crontab_id", None) 
    cursor = connection.cursor()
    sql = "delete from djcelery_crontabschedule where id = %s" %(crontab_id)
    cursor.execute(sql)
    code = "200"
    return HttpResponse(json.dumps({"code": code})) 

def add_interval(request):
    add_interval_every = request.POST.get("add_interval_every", None)
    add_interval_period = request.POST.get("add_interval_period", None)
    cursor = connection.cursor()
    sql = "insert into djcelery_intervalschedule(every, period) values('%s', '%s')" %(add_interval_every, add_interval_period)
    cursor.execute(sql)
    code = "200"
    return HttpResponse(json.dumps({"code": code}))

def delete_interval(request):
    interval_id = request.POST.get("interval_id", None)
    cursor = connection.cursor()
    sql = "delete from djcelery_intervalschedule where id = %s" %(interval_id)
    cursor.execute(sql)
    code = "200"
    return HttpResponse(json.dumps({"code": code}))
