# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-28 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailypost', '0004_auto_20170828_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='类别'),
        ),
    ]
