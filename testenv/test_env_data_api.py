#!/usr/bin/python
import MySQLdb
from log.views import logging


# def output_testenv_java_status():
#     conn = MySQLdb.connect(host='127.0.0.1', user='root', db='testenv_software_statu', port=3306, passwd='Fuliao10086',
#                            charset="utf8")
#     cur = conn.cursor()
#     sql = 'select testenv,software_name,software_status from testenv_software_error'
#     cur.execute(sql)
#     testenv_data_list = []
#     for item in cur.fetchall():
#         testenv_data_dict = {}
#         testenv_data_dict['testenv'] = item[0]
#         testenv_data_dict['software_name'] = item[1]
#         testenv_data_dict['software_status'] = item[2]
#         testenv_data_list.append(testenv_data_dict)
#     return testenv_data_list


def search_testenv_java_status(**data):
    env_name = ""
    software_name = ""
    if 'env_name' in data.keys():
        env_name = data['env_name']

    if 'software_name' in data.keys():
        software_name = data['software_name']

    conn = MySQLdb.connect(host='127.0.0.1', user='root', db='testenv_software_statu', port=3306,
                           passwd='Fuliao10086',
                           charset="utf8")

    if env_name != "" and software_name != "":
        sql = 'select testenv,software_name,software_status from testenv_software_error where testenv="%s" and ' \
              'software_name="%s"' %(env_name,software_name)

    if env_name == "" and software_name != "":
        sql = 'select testenv,software_name,software_status from testenv_software_error where software_name="%s"'\
              %(software_name)

    if env_name != "" and software_name == "":
        sql = 'select testenv,software_name,software_status from testenv_software_error where testenv="%s"' \
              % (env_name)

    if env_name == "" and software_name == "":
        sql = 'select testenv,software_name,software_status from testenv_software_error'

    cur = conn.cursor()
    logging.info(sql)
    cur.execute(sql)
    testenv_data_list = []
    for item in cur.fetchall():
        testenv_data_dict = {}
        testenv_data_dict['testenv'] = item[0]
        testenv_data_dict['software_name'] = item[1]
        testenv_data_dict['software_status'] = item[2]
        testenv_data_list.append(testenv_data_dict)
    return testenv_data_list