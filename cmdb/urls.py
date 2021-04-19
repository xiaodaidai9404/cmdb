"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from user_manager.views import logout,regist,forget,user_manager,system_user_update,system_user_del,reset_password,create_password,ldap_auth_v1,change_permission,write_permission


from server.views import insert_server_info,http_query_usage,index,server_info,check_server_info,\
    all_zabbix_server_info,select_server_type_list,update_server_info,del_server,server_load_info,\
    page_error,page_not_found,output_ip_for_hostname,add_server,output_usage_for_ip,search_database\
    ,output_int_ip,output_ext_ip,output_test_ip,add_mysql_router,router_info,export_excel,excel_download

from testenv.views import test_env_page,test_env_add,test_env_release,env_time_add,update_env_info,apply_test_env,\
    test_env_allot, sync_db, job_db_log, job_db_status,stop_sync_db, search_java_status, restart_java_software

from im_one_server.views import output_ip_for_usage,output_all_software,get_im_branch,output_im_ip_for_usage

from testenv.java_sync import job_java_log, job_java_status, sync_java, stop_sync_java

from tech_stack.views import tech_stack_page,add_stack,del_stack,update_stack

from mysql_submeter.views import mysql_submeter_page, mysql_auto_sql, download_sql, syncdb_list, add_syncdb, delete_records

from domain.views import action_domain, action_one_domain, domain_info

from celeryadmin.views import *
from django.contrib import admin

handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^login/$', ldap_auth_v1),
    url(r'^logout/$', logout),
    url(r'^regist/$', regist),
    url(r'^password/forget/$', forget),
    url(r'^password/reset/$', reset_password),
    url(r'^user/manager/$', user_manager),
    # url(r'^add/systemuser/$', system_user_add),
    url(r'^del/systemuser/$', system_user_del),
    url(r'^update/systemuser/$', system_user_update),
    url(r'^upload/server_info/$',insert_server_info),
    url(r'^query/usage/$',http_query_usage),
    url(r'^check/server_info/$',check_server_info),
    url(r'^search/database/$',search_database),
    url(r'^server_info/$',server_info),
    url(r'^zabbix_info/$',all_zabbix_server_info),
    url(r'^server_load_info/$',server_load_info),
    # url(r'^im_server_info/$',im_one_server_info),
    url(r'^select/server_type/$',select_server_type_list),
    url(r'^update/server/$',update_server_info),
    url(r'^del/server/$',del_server),
    url(r'^add/server/$',add_server),
    url(r'^tech/stack/$',tech_stack_page),
    url(r'^add/stack/$',add_stack),
    url(r'^del/stack/$',del_stack),
    url(r'^update/stack/$',update_stack),
    url(r'^get/server_ip/$',output_ip_for_hostname),
    url(r'^get/usage/$',output_usage_for_ip),
    url(r'^get/usage/int_ip/$',output_ip_for_usage),
    url(r'^get/all_software/$',output_all_software),
    url(r'^get/im_usage/int_ip/$',output_im_ip_for_usage),
    url(r'get/im_branch/$', get_im_branch),
    url(r'^env/test/$',test_env_page),
    url(r'^env/add/$',test_env_add),
    url(r'^env/release/$',test_env_release),
    url(r'^env/addtime/$',env_time_add),
    url(r'^env/update/$',update_env_info),
    url(r'^env/apply/$',apply_test_env),
    url(r'^env/allot/$',test_env_allot),
    url(r'^sync/db/$', sync_db),
    url(r'^job/db/log/$', job_db_log),
    url(r'^job/db/status/$', job_db_status),
    url(r'^sync/stop/db/$', stop_sync_db),
    url(r'^sync/java/$', sync_java),
    url(r'^job/java/log/$', job_java_log),
    url(r'^job/java/status/$', job_java_status),
    url(r'^sync/stop/java/$', stop_sync_java),
    url(r'^change/permission$', change_permission),
    url(r'^write/permission$', write_permission),
    url(r'^mysql/submeter/$', mysql_submeter_page),
    url(r'^mysql/auto_sql/$', mysql_auto_sql),
    url(r'^download/', download_sql, name='download'),
    # url(r'^env/java/', output_java_status),
    url(r'^env/search/', search_java_status),
    url(r'^env/restart/', restart_java_software),
    url(r'^syncdb_list', syncdb_list),
    url(r'^add_syncdb', add_syncdb),
    url(r'^delete_records', delete_records),
    url(r'^periodictask_list/$', periodictask_list, name='periodictask_list'),
    url(r'^crontab_list/$', crontab_list, name='crontab_list'),
    url(r'^interval_list/$', interval_list, name='interval_list'),
    url(r'^period_task_open/$', period_task_open, name='period_task_open'),
    url(r'^period_task_forbidden/$', period_task_forbidden, name='period_task_forbidden'),
    url(r'^period_task_delete/$', period_task_delete, name='period_task_delete'),
    url(r'^add_crontab/$', add_crontab, name='add_crontab'),
    url(r'^delete_crontab/$', delete_crontab, name='delete_crontab'),
    url(r'^add_interval/$', add_interval, name='add_interval'),
    url(r'^delete_interval/$', delete_interval, name='delete_interval'),
    url(r'^domain_info/$', domain_info),
    url(r'^domain/$', action_domain),
    url(r'^domain/(\d+)/$', action_one_domain),
    url(r'^get/int_ip$', output_int_ip),
    url(r'^get/ext_ip$', output_ext_ip),
    url(r'^get/test_ip$', output_test_ip),
    url(r'^router_info$', add_mysql_router),
    url(r'^router_info_html$',router_info),
    url(r'^cmdb_export$',export_excel),
    url(r'^download_excel$',excel_download),
]
