# coding:utf-8
from __future__ import absolute_import
from celery import Celery, platforms
from cmdb import settings
platforms.C_FORCE_ROOT = True  # 允许用root用户运行
app = Celery('clry')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  #貌似只能针对app目录下的tasks.py自动发现
