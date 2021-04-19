#!/bin/bash
ps -ef|grep -w "uwsgi.ini"|grep -v "auto_package_uwsgi.ini"|grep -v grep|awk '{if($3==1)print "kill -9 "$2}'|sh
/usr/local/python2.7/bin/uwsgi --ini uwsgi.ini
