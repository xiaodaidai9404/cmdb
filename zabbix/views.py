#!/usr/bin/python
#coding=utf-8
import json
import urllib2
import time
from models import Zabbix

class zabbix_api():
    def __init__(self,ip,key,auth_code,url):
        self.auth = auth_code
        self.ip = ip
        self.key = key
        self.url = url
        self.header = {"Content-Type":"application/json"}

    def get_response(self,data):
        request = urllib2.Request(self.url, data=data, headers=self.header)
        result = urllib2.urlopen(request)
        response = json.loads(result.read())
        result.close()
        return response

    def get_hostid(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostinterface.get",
                "params": {
                    "output": "extend",
                    "filter": {
                        "ip": [
                            self.ip,
                        ]
                    }
                },
                "auth": self.auth,
                "id": 0
            }
        )
        response = zabbix_api.get_response(self,data)['result'][0]['hostid']
        return response

    def get_item_id(self):
        hostids = zabbix_api.get_hostid(self)
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": "extend",
                    "hostids": hostids,
                    "search": {
                        "key_": self.key,
                    },
                    "sortfield": "name"
                },
                "auth": self.auth,
                "id": 0
            }
        )
        response = zabbix_api.get_response(self, data)['result'][0]['itemid']
        return response

    def get_graph_id(self):
        hostids = zabbix_api.get_hostid(self)
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": "graphid",
                    "hostids": hostids,
                    "filter": {
                        "name": "CPU load",
                    }
                },
                "auth": self.auth,
                "id": 0
            }
        )
        response = zabbix_api.get_response(self, data)['result'][0]['graphid']
        return response

    def get_memory_history_data(self):
        itemid = zabbix_api.get_item_id(self)
        # print itemid
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": itemid,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 1440
                },
                "auth": self.auth,
                "id": 0
            }
        )
        List = zabbix_api.get_response(self, data)['result']
        return List

    def get_memory_history_data_10min(self):
        itemid = zabbix_api.get_item_id(self)
        # print itemid
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": itemid,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 10
                },
                "auth": self.auth,
                "id": 0
            }
        )
        List = zabbix_api.get_response(self, data)['result']
        return List

    def get_load_history_data(self):
        itemid = zabbix_api.get_item_id(self)
            # print itemid
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 0,
                    "itemids": itemid,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 1440
                },
                "auth": self.auth,
                "id": 0
            }
        )
        List = zabbix_api.get_response(self, data)['result']
        return List

    def get_load_history_data_10min(self):
        itemid = zabbix_api.get_item_id(self)
            # print itemid
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 0,
                    "itemids": itemid,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 10
                },
                "auth": self.auth,
                "id": 0
            }
        )
        List = zabbix_api.get_response(self, data)['result']
        return List


def auth():
    url = "http://zabbix.ipaychat.com/api_jsonrpc.php"
    header = {"Content-Type":"application/json"}
    # auth user and password
    data = json.dumps(
    {
       "jsonrpc": "2.0",
       "method": "user.login",
       "params": {
       "user": "wuliang@ipaychat.com",
       "password": "xiongqian0610"
    },
    "id": 0
    })
    # create request object
    request = urllib2.Request(url,data)
    for key in header:
       request.add_header(key,header[key])
    result = urllib2.urlopen(request)
    response = json.loads(result.read())['result']
    result.close()
    return response

def monitory_url_make(ip):
    auth_code = auth()
    zabbix_url = "http://zabbix.floa.vip/api_jsonrpc.php"
    zabbix = zabbix_api(ip=ip,url=zabbix_url,auth_code=auth_code,key="null")
    graph_id = zabbix.get_graph_id()
    monitor_url = 'http://zabbix.floa.vip/charts.php?fullscreen=0&graphid={graph_id}'.format(graph_id=graph_id)
    return monitor_url



