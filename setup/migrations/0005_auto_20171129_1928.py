# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_auto_20171129_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impostazione',
            name='smtp_password',
            field=models.CharField(max_length=30, verbose_name=b'Password (server smtp)'),
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='smtp_username',
            field=models.CharField(max_length=30, verbose_name=b'Username (server smtp)'),
        ),
    ]
