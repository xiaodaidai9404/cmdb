#!/usr/bin/python env
#coding=utf-8
from django.db import models

# Create your models here.
class tech_stack_info(models.Model):
    name = models.CharField(u'技术栈名称', max_length=128)
    download_url = models.CharField(u'下载链接', max_length=512)
    info = models.CharField(u'描述', max_length=512, null=True)