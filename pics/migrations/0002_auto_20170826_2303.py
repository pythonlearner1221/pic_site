# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-26 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pics',
            name='created_time',
            field=models.DateField(),
        ),
    ]
