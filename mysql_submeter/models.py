#!/usr/bin/python env
#coding=utf-8
from django.db import models

# Create your models here.

class DbSyncRecord(models.Model):
    '''数据库同步记录表'''
    from_dbhost = models.CharField(max_length=512, default='', verbose_name='被同步数据库host')
    from_dbport = models.IntegerField(max_length=512, default='', verbose_name='被同步数据库port')
    to_dbhost = models.CharField(max_length=512, default='', verbose_name='同步数据库port')
    to_dbport = models.IntegerField(max_length=512, default='', verbose_name='同步数据库port')
    from_database = models.CharField(max_length=512, default='', verbose_name='被同步数据库名称')
    to_database = models.CharField(max_length=512, default='', verbose_name='同步数据库名称')
    tables = models.CharField(max_length=512, default='', verbose_name='被同步数据库表，空格分隔')
    pattern_CHOICE = (
        ('test', u'测试环境同步'),
        ('product', u'线上环境同步'),
        ('testtoproduct', u'测试同步线上'),
        ('producttotest', u'线上同步测试'),
    )
    pattern = models.CharField(max_length=512, default='test', choices=pattern_CHOICE, verbose_name='同步模式')
    crontab_task = models.CharField(max_length=512, default='', verbose_name='定时执行')
    operator = models.CharField(max_length=512, default='', verbose_name='操作人')
    create_time = models.DateTimeField(auto_now_add=True)
    
    
