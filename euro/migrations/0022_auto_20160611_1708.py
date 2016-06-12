# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('euro', '0021_auto_20160610_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rencontre',
            options={'ordering': ['date']},
        ),
    ]
