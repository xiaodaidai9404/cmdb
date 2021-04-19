#!/usr/bin/python env
#coding=utf-8

import jenkins
from django.conf import settings

class PythonJenkins(object):
    def __init__(self):
        url = settings.JENKINS_URL
        user = settings.JENKINS_USER
        password = settings.JENKINS_PASSWORD
        timeout = 2
        self.server = self.connect(url, user, password, timeout)

    def connect(self, url, user, password, timeout):
        self.server = jenkins.Jenkins(url, user, password, timeout)
        return self.server

    def build_job(self, job_name):
        """
        构建项目,返回该次构建ID
        :param job_name:
        :return:
        """
        number = self.server.build_job(job_name)
        return number

    def stop_build_job(self, job_name, number):
        """
        停止构建
        :param job_name:
        :param number:
        :return:
        """
        self.server.stop_build(job_name, number)

    def build_job_next_number(self, job_name):
        """
        通过构建前取下一次的构建id确定此次构建的id
        :param job_name:
        :return:
        """

        number = self.server.get_job_info(job_name)['nextBuildNumber']
        return number

    def build_job_log(self, job_name, number):
        result = self.server.get_build_console_output(job_name, number)
        return result

    def get_build_info(self, job_name, number):
        """
        0代表构建中
        1构建成功
        2构建失败
        :param job_name:
        :param number:
        :return:
        """
        result = self.server.get_build_info(job_name, number)['result']
        if result == None:
            return 0
        elif result == 'SUCCESS':
            return 1
        else:
            return 2

