#!/usr/bin/python
#coding=utf-8
from django.http import HttpResponse
import sys
import json
import datetime
import uuid
import time
import hashlib
from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.models import User
from Users.models import UserProfile as User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sendmail import send_mail
from user_manager.auth import require_http_users
from log.views import logging
import string
import random
from django.template import RequestContext
from ldap_auth import LdapAuthAPI
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from Users.models import UserProfile as User


def login(request):
    if request.method == 'POST':
        if "login" in request.POST.keys():
            username = str(request.POST['username'])
            password = request.POST['password']
            print username
            print password
            # user = User.objects.filter(username=username,password=password)
            user = auth.authenticate(username = username, password = password)
            print user
            if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'homepage/login.html',{'alert_msg': 2})
    return render(request, 'homepage/login.html',{'alert_msg': 0})


def regist(request):
    if request.method == 'POST':
        if "regist" in request.POST.keys():
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                print username,password,email
                logging.info(username,password,email)
                userResult = User.objects.filter(username=username)
                print userResult
                if len(userResult) > 0:
                    return render(request, 'homepage/regist.html', {'alert_msg': 4})
                else:
                    userid = uuid.uuid4()
                    user = User()
                    user.username = username
                    user.set_password(password)
                    user.email = email
                    user.uuid = userid
                    user.save()
                    # return HttpResponseRedirect('/login?alert_msg=5')
                    return render(request, 'homepage/regist.html', {'alert_msg': 5})
    return render(request, 'homepage/regist.html', {'alert_msg': 0})


def forget(request):
    if request.method == 'POST':
        if "forget" in request.POST.keys():
            username = request.POST['username']
            # print username
            email = request.POST['email']
            # print email
            user = User.objects.filter(username=username).values()[0]
            # print user
            d_email = user['email']
            # print d_email
            id = user['uuid']
            # print id
            if email == d_email:
                timestamp = int(time.time())
                value = 'str(%s) + str(%s) + %s' %(id,timestamp,'abc')
                print value
                hash = hashlib.md5(value)
                hash_encode = hash.hexdigest()
                print hash_encode
                msg = u"""
                Hi %s, 请点击下面链接重设密码！
                http://atpk.ipaychat.com/password/reset/?uuid=%s&timestamp=%s&hash=%s
                """ % (username, id, timestamp, hash_encode)
                alert_msg = 6
                send_mail(email,'忘记自动打包平台密码',msg)
                return render(request,'homepage/forget.html',{'alert_msg':alert_msg})
            else:
                alert_msg = 7
                return render(request, 'homepage/forget.html', {'alert_msg': alert_msg})
        return render(request, 'homepage/forget.html')
    return render(request, 'homepage/forget.html')


def reset_password(request):
    uuid_r = request.GET['uuid']
    timestamp = request.GET['timestamp']
    hash_encode = request.GET['hash']
    value = 'str(%s) + str(%s) + %s' % (uuid_r, timestamp, 'abc')
    hash = hashlib.md5(value)
    hash_dest_encode = hash.hexdigest()
    print value
    print hash_encode
    print hash_dest_encode
    # action = '/juser/password/reset/?uuid=%s&timestamp=%s&hash=%s' % (uuid_r, timestamp, hash_encode)

    if hash_encode == hash_dest_encode:
        if int(time.time()) - int(timestamp) > 600:
            return HttpResponse(u'链接已超时')
    else:
        return HttpResponse(u'hash值比对失败')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        print password, password_confirm
        if password != password_confirm:
            return HttpResponse('密码不匹配')
        else:
            userResult = User.objects.filter(uuid=uuid_r).values('username')
            if len(userResult) > 0:
                user = User.objects.get(uuid=uuid_r)
                user.set_password(password)
                user.save()
                alert_msg = 3
                # 密码重设成功
                return render(request,'homepage/reset_password.html',{'alert_msg':alert_msg})
            else:
                return HttpResponse('用户不存在')

    else:
        return render(request,'homepage/reset_password.html')

    return http_error(request, u'错误请求')


def ldap_auth_v1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['username']
        obj = LdapAuthAPI(username, password)
        if obj.auth():
            userResult = User.objects.filter(username=username)
            print userResult
            if len(userResult) > 0:
                pass
            else:
                userid = uuid.uuid4()
                user = User()
                user.username = username
                user.set_password('Fuliao123456')
                user.email = email
                user.uuid = userid
                user.save()
            login_user = auth.authenticate(username=username, password='Fuliao123456')
            auth.login(request, login_user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'homepage/login.html', {'alert_msg': 6})
    return render(request, 'homepage/login.html', {'alert_msg': 0})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@require_http_users(['ops'])
@login_required()
@csrf_exempt
def user_manager(request):
    result = User.objects.all().values()
    print result
    return render(request, 'homepage/user_manager.html', {'result': result}, context_instance=RequestContext(request))


def system_user_add(request):
    if request.method == 'POST':
        system_user = request.user.username
        username = request.POST['username']
        group = request.POST['group']
        password = request.POST['password']
        email = request.POST['email']
        print username, password, email
        userResult = User.objects.filter(username=username)
        print userResult
        if len(userResult) > 0:
            logging.warning('系统用户{system_user}添加系统用户{user}失败'.format(system_user=system_user, user=username))
            return HttpResponse(json.dumps({"code": 500, "msg": "用户已存在"}))
        else:
            userid = uuid.uuid4()
            user = User()
            user.group = group
            user.username = username
            user.set_password(password)
            user.email = email
            user.uuid = userid
            user.save()
            logging.info('系统用户{system_user}添加系统用户{user}成功'.format(system_user=system_user, user=username))
            msg = u"""
            Hi %s, 欢迎访问打包平台！
            地址:http://atpk.ipaychat.com/
            用户:%s
            密码:%s
            """ % (username,username,password)
            send_mail(email,"新增用户",msg)
            return HttpResponse(json.dumps({"code": 200, "msg": "添加成功"}))





@require_http_users(['ops'])
@login_required()
@csrf_exempt
def system_user_del(request):
    post_data = request.POST
    system_user = request.user.username
    username = post_data.get("username")
    try:
        User.objects.get(username=username).delete()
        if len(check_systemuser_exists(username)) < 1:
            logging.info('系统用户{system_user}删除系统用户{user}成功'.format(system_user=system_user, user=username))
            return HttpResponse(json.dumps({"code": 200, "msg": "删除成功"}))
    except Exception as e:
        logging.warning('系统用户{system_user}删除系统用户{user}失败'.format(system_user=system_user, user=username))
        return HttpResponse(json.dumps({"code": 500, "msg": "删除用户失败：%s" % str(e)}))


@require_http_users(['ops'])
@login_required()
@csrf_exempt
def system_user_update(request):
    if request.method == 'POST':
        post_data = request.POST
        system_user = request.user.username
        username = post_data.get("username")
        group = post_data.get("group")
        print username
        print group
        try:
            update_systemuser(username, group)
            logging.info(
                '系统用户{system_user}修改了用户{username}的权限为{group}'.format(system_user=system_user, username=username,
                                                                     group=group))
            return HttpResponse(json.dumps({"code": 200, "msg": "修改权限成功"}))
        except Exception as e:
            logging.warning('系统用户{system_user}修改用户{username}权限失败'.format(system_user=system_user, username=username))
            return HttpResponse(json.dumps({"code": 500, "msg": "修改权限失败：%s" % str(e)}))




def update_systemuser(username,group):
    User.objects.filter(username=username).update(group=group)

def check_systemuser_exists(username):
    return User.objects.filter(username=username)

def create_password(request):
    password = make_password()
    return HttpResponse(json.dumps({"password":password}))

def make_password():
    body = string.digits+string.ascii_letters+string.punctuation
    i = 0
    password = ''
    while i < 16:
        item = random.choice(body)
        password = password + item
        i = i+1
    return password

@require_http_users(['ops'])
@login_required()
@csrf_exempt
def change_permission(request):
    if request.method == 'POST':
        post_data = request.POST
        permission_list = post_data['permissions'].split(',')
        logging.info(str(permission_list))
        username = post_data['username']
        user = User.objects.get(username=username)
        code_list = [Permission.objects.filter(codename=code_name).values('id')[0]['id'] for code_name in permission_list]
        user.user_permissions = code_list
        msg = "权限修改成功"
    return HttpResponse(json.dumps({"code": 200, "msg": msg}))


@require_http_users(['ops'])
@login_required()
@csrf_exempt
def write_permission(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        post_data = request.POST
        username = post_data['username']
        msg = [item.split('.')[1] for item in list(User.objects.get(username=username).get_all_permissions())]

    return HttpResponse(json.dumps({"msg": msg}))
