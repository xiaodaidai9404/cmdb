#!/usr/bin/python
#coding=utf-8
from datetime import datetime
#导入django中的响应扩展
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.http import QueryDict
from django.forms.models import model_to_dict
from models import DomainInfo
import simplejson as json
from log.views import logging
from user_manager.auth import require_http_users
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
def domain_info(request):
    result = list(DomainInfo.objects.all().values('id', 'domain_name', 'start_date', 'end_date', 'usage', 'ssl_domain_name',
                                                  'ssl_start_date', 'ssl_end_date'))
    return render(request, 'homepage/domain_info.html', {"result": result})


# @require_http_users(['ops'])
# @login_required()
@csrf_exempt
def action_domain(request):
    if request.method == 'GET':
        queryset = DomainInfo.objects.all()
        domain_list = []
        for domain in queryset:
            domain_list.append({
                'id': domain.id,
                'domain_name': domain.domain_name,
                'start_date': domain.start_date,
                'end_date': domain.end_date,
                'usage': domain.usage,
                'ssl_domain_name': domain.ssl_domain_name,
                'ssl_start_date': domain.ssl_start_date,
                'ssl_end_date': domain.ssl_end_date
            })
            return JsonResponse(domain_list, safe=False)

    if request.method == 'POST':
        domain_dict = request.POST
        item_list = ['usage', 'ssl_domain_name', 'ssl_start_date', 'ssl_end_date']
        for item in item_list:
            if item not in domain_dict.keys():
                domain_dict[item] = ""
        domain = DomainInfo.objects.create(domain_name=domain_dict.get('domain_name'),
                                           start_date=domain_dict.get('start_date'),
                                           end_date=domain_dict.get('end_date'),
                                           usage=domain_dict.get('usage'),
                                           ssl_domain_name=domain_dict.get('ssl_domain_name'),
                                           ssl_start_date=domain_dict.get('ssl_start_date'),
                                           ssl_end_date=domain_dict.get('ssl_end_date'))

        return JsonResponse({
            'id': domain.id,
            'domain_name': domain.domain_name,
            'start_date': domain.start_date,
            'end_date': domain.end_date,
            'usage': domain.usage,
            'ssl_domain_name': domain.ssl_domain_name,
            'ssl_start_date': domain.ssl_start_date,
            'ssl_end_date': domain.ssl_end_date
        }, status=201)

#(\d+)
# @require_http_users(['ops'])
# @login_required()
@csrf_exempt
def action_one_domain(request, pk):
    try:
        domain = DomainInfo.objects.get(id=pk)
    except DomainInfo.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        return JsonResponse({
            'id': domain.id,
            'domain_name': domain.domain_name,
            'start_date': domain.start_date,
            'end_date': domain.end_date,
            'usage': domain.usage,
            'ssl_domain_name': domain.ssl_domain_name,
            'ssl_start_date': domain.ssl_start_date,
            'ssl_end_date': domain.ssl_end_date
        }, safe=False)

    if request.method == 'PUT':
        logging.info(request.body)
        json_bytes = request.body
        json_str = json_bytes.decode()
        domain_dict = json.loads(json_str)
        logging.info(domain_dict)
        item_list = ['usage', 'ssl_domain_name', 'ssl_start_date', 'ssl_end_date']
        for item in item_list:
            if item not in domain_dict.keys():
                domain_dict[item] = ""
        DomainInfo.objects.filter(id=pk).update(
            domain_name=domain_dict.get("domain_name"),
            end_date=domain_dict.get("end_date"),
            usage=domain_dict.get("usage"),
            ssl_start_date=domain_dict.get("ssl_start_date"),
            ssl_domain_name=domain_dict.get("ssl_domain_name"),
            ssl_end_date=domain_dict.get("ssl_end_date")
        )
        return HttpResponse(status=204)

    if request.method == 'DELETE':
        domain.delete()
        return HttpResponse(status=204)

