#!/usr/bin/python env
#coding=utf-8
from django.db import models

# Create your models here.
class Zabbix(models.Model):
    ip = models.GenericIPAddressField(u'IP地址', unique=True, max_length=16)
    upload_max =  models.CharField(u'一天内最高的负载值', max_length=16)
    memory_free_min = models.CharField(u'一天内最少的剩余内存值',max_length=16)
    upload_10min_max =  models.CharField(u'10分钟内最高的负载值', max_length=16,blank=True,null=True)
    memory_10min_min = models.CharField(u'10分钟内最少的剩余内存值',max_length=16,blank=True,null=True)
    server_type = models.CharField(u'服务器类型', max_length=16)
    zabbix_url = models.CharField(u'监控地址', max_length=108,blank=True,null=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
