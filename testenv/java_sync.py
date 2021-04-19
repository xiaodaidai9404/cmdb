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
from api.views import api_env_insert_java_jenkins_build_number,api_env_select_java_jenkins_build_number

from log.views import logging
from jenkins_api import PythonJenkins


@csrf_exempt
def sync_java(request):
    data = request.POST

    env_name = data['env_name']
    job_name = env_name+"-java-sync"

    server = PythonJenkins()

    number = server.build_job_next_number(job_name)

    server.build_job(job_name)

    return_code = api_env_insert_java_jenkins_build_number(env_name, number)

    if return_code == 200:
        msg = "触发构建成功,请关注日志以及构建状态"
    else:
        msg = "触发构建失败,联系运维处理"
    return HttpResponse(json.dumps({"msg": msg}))


@csrf_exempt
def job_java_log(request):
    data = request.POST

    env_name = data['env_name']
    job_name = env_name+"-java-sync"

    number = int(api_env_select_java_jenkins_build_number(env_name))

    server = PythonJenkins()

    print "日志刷新"
    logging.info("日志刷新")

    make_log = server.build_job_log(job_name, number)

    return HttpResponse(json.dumps({"make_log": make_log}))


@csrf_exempt
def job_java_status(request):
    data = request.POST
    env_name = data['env_name']
    job_name = env_name+"-java-sync"

    server = PythonJenkins()

    number = int(api_env_select_java_jenkins_build_number(env_name))

    code = server.get_build_info(job_name, number)

    return HttpResponse(json.dumps({"code": code}))


@csrf_exempt
def stop_sync_java(request):
    data = request.POST
    env_name = data['env_name']
    job_name = env_name + "-java-sync"

    server = PythonJenkins()

    number = int(api_env_select_java_jenkins_build_number(env_name))

    try:
        server.stop_build_job(job_name, number)
        return HttpResponse(json.dumps({"msg": '停止成功'}))
    except Exception as e:
        return HttpResponse(json.dumps({"msg": str(e)}))
