#!/usr/bin/python env
#coding=utf-8

from clry.celery import Celery
from clry.celery import app
from celery import shared_task
import os

@app.task
def test_cron():
    print("test crontab")

@app.task
def sync_db(from_dbhost, from_dbport, to_dbhost, to_dbport, from_database, to_database, tables="", pattern="test", issyncdata=""):
    os.system('sh /data/scripts/sync_db.sh %s %s %s %s %s %s "%s" %s "%s"'%(from_dbhost, from_dbport, to_dbhost, to_dbport, from_database, to_database, tables, pattern, issyncdata))
