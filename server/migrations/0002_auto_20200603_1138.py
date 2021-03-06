# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2020-06-03 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('router_name', models.CharField(max_length=256, verbose_name='\u4ee3\u7406\u540d\u79f0')),
                ('databases', models.CharField(max_length=4096, verbose_name='\u6570\u636e\u5e93')),
                ('position', models.IntegerField(choices=[(b'0', 'Master'), (b'1', 'Slave')], default=1, verbose_name='\u6570\u636e\u5e93\u8eab\u4efd')),
                ('real_server', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u540e\u7aef\u771f\u5b9e\u5730\u5740')),
            ],
        ),
    ]
