# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro', '0018_auto_20160606_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='sort_id',
            field=models.IntegerField(default=0),
        ),
    ]
