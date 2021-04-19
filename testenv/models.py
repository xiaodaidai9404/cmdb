#!/usr/bin/python env
#coding=utf-8
from django.db import models


#测试环境名称,项目名称,项目经理,开发人员,申请时间,使用时长,当前状态 按钮:DB同步,java同步,IM同步

# Create your models here.
class test_env_info(models.Model):
    env_name = models.CharField(u'测试环境名', max_length=128, primary_key=True)
    project_name = models.CharField(u'项目名', max_length=128, null=True)
    project_leader = models.CharField(u'项目经理', max_length=128, null=True)
    project_developer = models.CharField(u'开发人员', max_length=512, null=True)
    start_time = models.DateTimeField(u'申请时间', null=True)
    end_time = models.DateTimeField(u'结束时间', null=True)
    status_CHOICE = (
        ('0', u'use'),
        ('1', u'not_use'),
    )
    status = models.IntegerField(u'使用or没在使用', default=1, choices=status_CHOICE)
    java_jenkins_id = models.IntegerField(u'java环境的当前构建id', max_length=128, null=True)
    im_jenkins_id = models.IntegerField(u'im环境的当前构建id', max_length=128, null=True)
    db_jenkins_id = models.IntegerField(u'db环境的当前构建id', max_length=128, null=True)


class test_env_history(models.Model):
    env_name = models.CharField(u'测试环境名', max_length=128, null=True)
    project_name = models.CharField(u'项目名', max_length=128, primary_key=True)
    project_leader = models.CharField(u'项目经理', max_length=128)
    project_developer = models.CharField(u'开发人员', max_length=512, null=True)
    spend_time = models.IntegerField(u'开发花费时间', max_length=8, null=True)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)