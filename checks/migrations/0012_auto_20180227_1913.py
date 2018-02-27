# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0011_auto_20180227_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settimana',
            name='lunedi',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='martedi',
        ),
    ]
