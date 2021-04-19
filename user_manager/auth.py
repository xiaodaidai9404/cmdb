#coding: utf-8


import logging
from functools import wraps
from django.http import HttpResponseNotAllowed
from django.utils.decorators import available_attrs
from Users.models import UserProfile as User
from django.http import HttpResponse
import json

def require_http_users(allow_user_list):
    """访问用户的限制"""
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            user = request.user
            group = return_group(user)
            if group not in allow_user_list:
                # return HttpResponseNotAllowed(allow_user_list)
                msg = "用户没有权限执行"
                return HttpResponse(json.dumps({"code": 405, "msg": msg}))
            return func(request, *args, **kwargs)
        return inner
    return decorator

def return_group(user):
    group = User.objects.filter(username=user).values()[0]['group']
    return group
