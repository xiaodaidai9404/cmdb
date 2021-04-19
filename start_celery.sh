#!/bin/bash
nohup /usr/local/python2.7/bin/python manage.py celery beat > logs/beat.log 2>&1 &
nohup /usr/local/python2.7/bin/python manage.py celery worker > logs/worker.log 2>&1 &
