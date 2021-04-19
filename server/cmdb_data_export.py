#!/usr/bin/python
#coding=utf8

import os
import sys
import MySQLdb
from xlsxwriter import workbook
from log.views import logging

class ExportData:
    def __init__(self,field):
        self.dbHost = '127.0.0.1'
        self.dbUser = 'root'
        self.dbPassword = 'Fuliao10086'
        self.field = field
        self.argsDict = {"server_type":"类型", "hostname":"主机", "ip":"内网IP","other_ips":"外网IP","cpu_info":"cpu","memory_info":"内存","disk_info":"磁盘","sn":"机器码","usage":"用途"}
        self.file = "/data/scripts/cmdb.xls"

    def queryData(self):
        conn=MySQLdb.connect(host=self.dbHost,user=self.dbUser,port=3306,passwd=self.dbPassword,charset="utf8")
        cur=conn.cursor()
        b=[ '`'+i+'`' for i in self.field.split(",") ]
        c=",".join(b)
        selectSql = "select %s from cmdb.server_server" %(c)
        logging.info(selectSql)
        rows = cur.execute(selectSql)
        if rows == 0 :
            return ''
        else:
            return cur.fetchall()

    def judge_file_exist(self):
        if os.path.exists(self.file):
            os.remove(self.file)

    def exportExcel(self,data):
        work = workbook.Workbook(self.file)
        worksheet = work.add_worksheet()
        format_title = work.add_format({'bold': True, 'font_size': 16})
        # 设置水平对齐、垂直对齐
        format_title.set_align('center')
        format_title.set_align('vcenter')
        format_body = work.add_format({'font_size': 14})
        filedList = self.field.split(",")
        i=0
        for item in filedList :
            try:
                sheet_titile = self.argsDict[item]
                worksheet.write(0,i,item)
                i+=1
            except Exception as e:
                logging.info(e)
                return 1

        for row in range(1,len(data)+1):
            for col in range(0,len(data[row-1])):
                worksheet.write(row,col,data[row-1][col])
                col+=1
            row+=1
        work.close()
        return 0
        
