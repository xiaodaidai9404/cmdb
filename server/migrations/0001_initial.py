# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2019-07-19 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_type', models.CharField(max_length=16, verbose_name='\u670d\u52a1\u5668\u7c7b\u578b')),
                ('hostname', models.CharField(max_length=512, verbose_name='\u670d\u52a1\u5668\u540d\u79f0')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='IP\u5730\u5740')),
                ('other_ips', models.CharField(max_length=512, verbose_name='\u5176\u4ed6IP\u5730\u5740')),
                ('usage', models.CharField(max_length=4096, null=True, verbose_name='\u7528\u9014')),
                ('port', models.CharField(max_length=2048, null=True, verbose_name='\u7aef\u53e3')),
                ('cpu_info', models.CharField(max_length=128, verbose_name='CPU\u4fe1\u606f')),
                ('memory_info', models.CharField(max_length=128, verbose_name='\u5185\u5b58\u4fe1\u606f')),
                ('disk_info', models.CharField(max_length=128, verbose_name='\u78c1\u76d8\u4fe1\u606f')),
                ('config', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u914d\u7f6e\u4fe1\u606f')),
                ('desc', models.CharField(max_length=512, verbose_name='\u5907\u6ce8')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u5df2\u5220\u9664')),
                ('buy_date', models.CharField(blank=True, default=b'2099-01-01', max_length=128, null=True, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('service_action', models.IntegerField(choices=[(b'0', 'test'), (b'1', 'online')], default=1, verbose_name='\u670d\u52a1\u5668\u7ebf\u4e0aor\u6d4b\u8bd5')),
                ('service_app', models.IntegerField(choices=[(b'0', 'fuliao'), (b'1', 'midao')], default=0, verbose_name='\u670d\u52a1\u5668\u5f52\u5c5eapp')),
            ],
        ),
    ]
