#!/usr/bin/python env
#coding=utf-8
from django.db import models

# Create your models here.
class Server(models.Model):
    """
    服务器
    """
    #aliyun,idc
    server_type = models.CharField(u'服务器类型', max_length=16)
    hostname = models.CharField(u'服务器名称', max_length=512)

    ip = models.GenericIPAddressField(u'IP地址', unique=True, max_length=16)
    other_ips = models.CharField(u'其他IP地址', max_length=512)  # 多条记录以','分割
    usage = models.CharField(u'用途', max_length=4096, null=True) #多个服务以','分割
    port = models.CharField(u'端口', max_length=2048, null=True) #多个端口以','分割
    cpu_info = models.CharField(u'CPU信息', max_length=128)
    memory_info = models.CharField(u'内存信息', max_length=128)
    disk_info = models.CharField(u'磁盘信息', max_length=128)
    # 配置信息(形如4C8G格式)
    config = models.CharField(u'配置信息', max_length=64, null=True, blank=True)
    desc = models.CharField(u'备注', max_length=512)
    OTHER_USE_STATE = {'1': u'使用', '2': u'未使用', '3': u'禁用'}
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)
    sn = models.CharField(u'sn',max_length=256,null=True, blank=True)
    buy_date = models.CharField(u'购买日期', null=True, blank=True, default="2099-01-01",max_length=128)
    service_CHOICE = (
        ('0', u'test'),
        ('1', u'online'),
    )
    service_action = models.IntegerField(u'服务器线上or测试', default=1, choices=service_CHOICE)
    server_app_choice = (
        ('0', u'fuliao'),
        ('1', u'midao'),
    )
    server_app = models.IntegerField(u'服务器归属app', default=0, choices=server_app_choice)

class RouterInfo(models.Model):
    """
    数据库代理
    """
    router_name = models.CharField(u'代理名称', max_length=256)
    databases = models.CharField(u'数据库', max_length=4096)
    position_choice = (
        ('0', u'Master'),
        ('1', u'Slave'),
    )
    position = models.IntegerField(u'数据库身份', default=1, choices=position_choice)
    real_server = models.CharField(u'后端真实地址', null=True, blank=True, max_length=128)