#!/bin/bash
ps -ef|grep celery|grep -v grep|awk '{print "kill -9 " $2}'|sh
