# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro', '0016_tag_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='avatar',
            field=models.FileField(blank=True, default=None, null=True, upload_to='euro/avatars'),
        ),
    ]
