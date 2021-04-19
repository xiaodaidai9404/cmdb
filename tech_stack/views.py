#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import time
from api.views import output_all_server,usage_query_server,output_all_server_for_server_type_num,all_server_num,\
    output_all_server_for_server_type,output_all_server_type,output_all_server_zabbix_info,\
    memory_echarts_info,upload_echarts_info
from log.views import logging
from django.shortcuts import render_to_response
from tech_stack.models import tech_stack_info
from api.views import add_stack_api,update_stack_api,output_all_stack
from user_manager.auth import require_http_users

@csrf_exempt
def tech_stack_page(request):
    result = output_all_stack()
    return render(request, 'homepage/tech_stack.html', {'result': result})


@require_http_users(['ops'])
@login_required()
def del_stack(request):
    data = request.POST
    id = data['id']

    tech_stack_info.objects.get(id=id).delete()
    if tech_stack_info.objects.filter(id=id):
        msg = '删除失败'
        return HttpResponse(json.dumps({"code": 500, "msg": msg}))
    else:
        msg = '删除成功'
        return HttpResponse(json.dumps({"code": 200, "msg": msg}))

@require_http_users(['ops'])
@login_required()
def add_stack(request):
    data = request.POST

    name = data['name']
    download_url = data['download_url']
    info = data['info']

    return_code = add_stack_api(name=name,download_url=download_url,info=info)

    if return_code == "200":
        msg = '新增成功'
    elif return_code == "404":
        msg =  '新增失败'
    elif return_code == "500":
        msg = '技术栈已存在'
    else:
        msg = '未知错误'
    return HttpResponse(json.dumps({"code": return_code, "msg": msg}))


@require_http_users(['ops'])
@login_required()
def update_stack(request):
    data = request.POST

    name = data['name']
    download_url = data['download_url']
    info = data['info']

    return_code = update_stack_api(name,download_url,info)
    if return_code == "200":
        msg = "修改成功"
        return HttpResponse(json.dumps({"code": return_code, "msg": msg}))
    else:
        msg = "修改失败"
        return HttpResponse(json.dumps({"code": 404, "msg": msg}))




