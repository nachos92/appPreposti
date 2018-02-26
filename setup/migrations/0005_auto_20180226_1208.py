# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_auto_20180212_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impostazione',
            name='port',
        ),
        migrations.RemoveField(
            model_name='impostazione',
            name='smtp_password',
        ),
        migrations.RemoveField(
            model_name='impostazione',
            name='smtp_server',
        ),
        migrations.RemoveField(
            model_name='impostazione',
            name='smtp_username',
        ),
    ]
