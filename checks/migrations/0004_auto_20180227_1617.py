# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0003_auto_20180227_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settimana',
            name='gio',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='lun',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='mar',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='mer',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='ven',
        ),
    ]
