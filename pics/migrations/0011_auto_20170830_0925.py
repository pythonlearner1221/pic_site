# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-30 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0010_auto_20170829_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pics',
            name='created_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pics',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
