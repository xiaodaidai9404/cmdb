#!/usr/bin/python env
#coding=utf-8
from django.db import models


class DomainInfo(models.Model):
    """
    域名以及证书信息
    """
    domain_name = models.CharField(u'名称', max_length=128)
    start_date = models.CharField(u'开始日期', null=False, blank=True, max_length=128)
    end_date = models.CharField(u'过期日期', null=False, blank=True, max_length=128)
    usage = models.CharField(u'域名作用', max_length=512)
    ssl_domain_name = models.CharField(u'证书检测域名', max_length=512)
    ssl_start_date = models.CharField(u'证书开始日期', null=True, blank=True, max_length=128)
    ssl_end_date = models.CharField(u'证书开始日期', null=True, blank=True, max_length=128)