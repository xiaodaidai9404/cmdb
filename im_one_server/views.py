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
from api.views import api_output_server_for_usage,im_output_server_for_usage
from ssh import flssh

from log.views import logging

from django.shortcuts import render_to_response

from user_manager.auth import require_http_users


# @csrf_exempt
# def im_one_server_info(request):
#     return render(request,'homepage/im_one_update.html')


def output_all_software(request):
    if 'server_app' in request.GET:
        server_app = request.GET['server_app']
    else:
        server_app = 0

    if int(server_app) == 0:
        software_list = ['web_proxy', 'billing_analyser', 'billing_refresh', 'fortune_center', 'center',
                'msg_analyser', 'live_center', 'live_pk', 'common_room', 'lucky_center', 'quiz_game', 'group_chat',
                    'user_center', 'gate', 'logon', 'multi_people_room', 'wealth', 'bonus', 'msg_sender','media_agent','media_billing_corotine','bonus_wallet','time_server','im_grpc_agent']
    elif int(server_app) == 1:
        software_list = ['gate', 'web_proxy', 'user_center', 'billing_analyser', 'msg_analyser', 'media_billing',
                        'fortune_center', 'flow_analyser', 'chat_filter_center', 'billing_refresh', 'audit_center',
                        'lucky_center', 'center', 'wealth', 'media_agent']

    response = HttpResponse(json.dumps({"all_software": software_list}))
    # response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def output_ip_for_usage(request):
    if 'usage' in request.GET:
        logging.info(request.GET)
        soft = request.GET['usage']
        server_app = request.GET['server_app']
        server_list = api_output_server_for_usage(soft, server_app)

        return_dict = {}

        ip_list = [item['ip'] for item in server_list]
        return_dict['ip_list'] = ip_list

        usage_list = [ item['usage'] for item in server_list ]

        r_net_proxy_net = '%s_1_net_proxy_net' % (soft)
        p_net_proxy_net = re.compile(r_net_proxy_net)

        r_net_proxy_intranet = '%s_1_net_proxy_intranet' % (soft)
        p_net_proxy_intranet = re.compile(r_net_proxy_intranet)

        if len(p_net_proxy_net.findall(usage_list[0])) > 0:
            return_dict['net_proxy_net'] = 1
        else:
            return_dict['net_proxy_net'] = 0

        if len(p_net_proxy_intranet.findall(usage_list[0])) > 0:
            return_dict['net_proxy_intranet'] = 1
        else:
            return_dict['net_proxy_intranet'] = 0

        response = HttpResponse(json.dumps({"server": return_dict}))
        # response['Access-Control-Allow-Origin'] = '*'
        return response


@csrf_exempt
def output_im_ip_for_usage(request):
    if 'usage' in request.GET:
        logging.info(request.GET)
        soft = request.GET['usage']
        server_app = request.GET['server_app']
        server_list = im_output_server_for_usage(soft, server_app)

        return_dict = {}

        ip_list = [item['ip'] for item in server_list]
        return_dict['ip_list'] = ip_list

        usage_list = [ item['usage'] for item in server_list ]

        r_net_proxy_net = '%s_1_net_proxy_net' % (soft)
        p_net_proxy_net = re.compile(r_net_proxy_net)

        r_net_proxy_intranet = '%s_1_net_proxy_intranet' % (soft)
        p_net_proxy_intranet = re.compile(r_net_proxy_intranet)

        if len(p_net_proxy_net.findall(usage_list[0])) > 0:
            return_dict['net_proxy_net'] = 1
        else:
            return_dict['net_proxy_net'] = 0

        if len(p_net_proxy_intranet.findall(usage_list[0])) > 0:
            return_dict['net_proxy_intranet'] = 1
        else:
            return_dict['net_proxy_intranet'] = 0

        response = HttpResponse(json.dumps({"server": return_dict}))
        # response['Access-Control-Allow-Origin'] = '*'
        return response

@csrf_exempt
def get_im_branch(request):
    """
    返回im所有分支
    :return:
    """
    ip = "10.0.2.1"
    ssh_port = 32022
    ssh_user = 'root'
    package_command = "/bin/bash /data/scripts/im_branch.sh"

    branch = flssh(ip=ip, port=ssh_port, Command=package_command, user=ssh_user)
    branch_list = branch.split()

    response = HttpResponse(json.dumps({"all_branch": branch_list}))
    return response


@csrf_exempt
def server_go_online(request):
    data = request.POST

    server_name = data['server_name']
    branch_name = data['branch_name']
    ip_list = data['ip'].split(',')
    net_statu = data['net']
    config_statu = data['config_statu']

    response = HttpResponse(json.dumps({"status": "传入参数正常"}))
    return response
