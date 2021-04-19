#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
# import json
import simplejson as json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import test_env_info,test_env_history
import time
import datetime
from api.views import output_test_env_info,api_test_env_add,output_env_info_for_history,api_test_env_histroy_insert,\
    api_test_env_release,api_env_select_end_time,api_env_insert_end_time,\
    api_update_test_env_info,free_test_env_api,api_test_env_allow,\
    api_env_insert_db_jenkins_build_number,api_env_insert_java_jenkins_build_number,\
    api_env_select_db_jenkins_build_number,output_one_server_ip

from log.views import logging
from jenkins_api import PythonJenkins
from test_env_data_api import search_testenv_java_status
from ssh import flssh

from django.shortcuts import render_to_response


@csrf_exempt
def test_env_page(request):
    result = output_test_env_info()
    return render(request, 'homepage/test_env.html', {'result': result})


@csrf_exempt
def test_env_add(request):
    """
    新增测试环境
    :param request:
    :return:
    """
    data = request.POST
    env_name = data['env_name']

    return_code = api_test_env_add(env_name)

    if return_code == "200":
        msg = '新增成功'
    elif return_code == "404":
        msg = '新增失败'
    elif return_code == "500":
        msg = '该测试环境已存在'
    else:
        msg = '未知错误'
    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


def test_env_allot(request):
    """
    分配测试环境
    :param request:
    :return:
    """
    data = request.POST
    env_name = data['env_name']
    project_name = data['project_name']
    project_leader = data['project_leader']
    project_developer = data['project_developer']
    use_day = int(data['use_day'])

    """
    通过use_day获取当前日期和结束日期
    """
    now_time = datetime.datetime.now()
    end_time = now_time + datetime.timedelta(days=use_day)

    start_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    return_code = api_test_env_allow(env_name, project_name, project_leader, project_developer, start_time, end_time)

    if return_code == "200":
        msg = '分配成功'
    elif return_code == "500":
        msg = '该测试环境已被使用'
    else:
        msg = '未知错误'
    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


@csrf_exempt
def test_env_release(request):
    """
    释放环境,先将项目开发信息保存到历史表当中,再清除数据库环境信息
    :param request:
    :return:
    """
    data = request.POST
    env_name = data['env_name']

    env_list = output_env_info_for_history(env_name)

    print env_list
    logging.info(str(env_list))

    project_name = env_list[0]['project_name']
    project_leader = env_list[0]['project_leader']
    project_developer = env_list[0]['project_developer']
    start_time = env_list[0]['start_time']

    # dt_format = "%Y-%m-%d %H:%M:%S"
    # start_dt = time.strptime(start_time, dt_format)
    # start_timestamp = int(time.mktime(start_time))
    start_timestamp = int(time.mktime(start_time.timetuple()))
    end_timestamp = int(time.time())
    spend_time = (end_timestamp - start_timestamp)/86400 + 1

    api_test_env_histroy_insert(env_name, project_name, project_leader, project_developer, spend_time)

    return_code = api_test_env_release(env_name)

    if return_code == "200":
        msg = "该环境已释放"
    else:
        msg = "环境释放失败"

    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


@csrf_exempt
def env_time_add(request):
    data = request.POST

    env_name = data['env_name']
    add_use_day = int(data['add_use_day'])

    end_time = api_env_select_end_time(env_name)[0]['end_time']
    new_time = end_time + datetime.timedelta(days=add_use_day)

    new_end_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

    return_code = api_env_insert_end_time(env_name,new_end_time)

    if return_code == "200":
        msg = "延时成功"
    else:
        msg = "延时失败"

    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


@csrf_exempt
def update_env_info(request):
    data = request.POST

    env_name = data['update_env_name']
    project_name = data['update_project_name']
    project_leader = data['update_project_leader']
    project_developer = data['update_project_developer']

    return_code = api_update_test_env_info(env_name, project_name, project_leader, project_developer)

    if return_code == "200":
        msg = "修改项目信息成功"
    else:
        msg = "修改项目信息失败"

    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))

@csrf_exempt
def apply_test_env(request):
    free_env_list = free_test_env_api()
    if len(free_env_list) > 0:
        return_code = "200"
        return HttpResponse(json.dumps({"code": return_code, "result": free_env_list}))
    else:
        return_code = "500"
        msg = "没有空余的测试环境"
        return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


@csrf_exempt
def sync_db(request):
    data = request.POST

    env_name = data['env_name']
    job_name = env_name+"-db-sync"

    server = PythonJenkins()

    number = server.build_job_next_number(job_name)

    server.build_job(job_name)

    return_code = api_env_insert_db_jenkins_build_number(env_name, number)

    if return_code == 200:
        msg = "触发构建成功,请关注日志以及构建状态"
    else:
        msg = "触发构建失败,联系运维处理"
    return HttpResponse(json.dumps({"msg": msg}))


@csrf_exempt
def job_db_log(request):
    data = request.POST

    env_name = data['env_name']
    job_name = env_name + "-db-sync"

    number = int(api_env_select_db_jenkins_build_number(env_name))

    server = PythonJenkins()

    print "日志刷新"
    logging.info("日志刷新")

    make_log = server.build_job_log(job_name, number)

    return HttpResponse(json.dumps({"make_log": make_log}))


@csrf_exempt
def job_db_status(request):
    data = request.POST
    env_name = data['env_name']
    job_name = env_name + "-db-sync"

    server = PythonJenkins()

    number = int(api_env_select_db_jenkins_build_number(env_name))

    code = server.get_build_info(job_name, number)

    return HttpResponse(json.dumps({"code": code}))


@csrf_exempt
def stop_sync_db(request):
    data = request.POST
    env_name = data['env_name']
    job_name = env_name + "-db-sync"

    server = PythonJenkins()

    number = int(api_env_select_db_jenkins_build_number(env_name))

    try:
        server.stop_build_job(job_name, number)
        return HttpResponse(json.dumps({"msg": '停止成功'}))
    except Exception as e:
        return HttpResponse(json.dumps({"msg": str(e)}))


# def output_java_status(request):
#     java_testenv_status = output_testenv_java_status()
#     testenv_data_list = sorted(java_testenv_status, key=lambda item: item['software_status'], reverse=True)
#     response = HttpResponse(json.dumps({"java_testenv_status": testenv_data_list}))
#     return response


@csrf_exempt
def search_java_status(request):
    logging.info(request.method)
    data = request.POST
    logging.info(data)
    data_dict = {}
    if 'search_testenv' in data.keys():
        data_dict['env_name'] = data['search_testenv']

    if 'search_software' in data.keys():
         data_dict['software_name'] = data['search_software']

    logging.info(data_dict)
    java_testenv_status = search_testenv_java_status(**data_dict)
    testenv_data_list = sorted(java_testenv_status, key=lambda item: item['software_status'], reverse=True)
    response = HttpResponse(json.dumps({"java_testenv_status": testenv_data_list}))
    return response


@csrf_exempt
def restart_java_software(request):
    independent_env = ['test01', 'test02', 'test03', 'test04']
    data = request.POST
    env_name = data['env_name']
    java_env_name = data['env_name']
    software_name = data['software_name']

    if env_name in independent_env:
        java_env_name = env_name+"-java"

    server_ip = output_one_server_ip(java_env_name)[0]['ip']
    python_path = "/usr/bin/python"
    if server_ip == "10.0.0.175":
        python_path = "/usr/local/python-2.7.9/bin/python"

    remote_command = "{python_path} /data/scripts/test_env/restart_software.py {env_name} {software_name}".format\
        (python_path=python_path, env_name=env_name, software_name=software_name)
    logging.info(server_ip,remote_command)
    flssh(server_ip, remote_command, 'root', 32022)

    response = HttpResponse(json.dumps({"info": "OK"}))

    return response
