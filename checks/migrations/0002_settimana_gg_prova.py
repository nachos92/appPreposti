# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_auto_20171219_1945'),
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='gg_prova',
            field=models.ForeignKey(default=datetime.datetime(2017, 12, 20, 15, 32, 1, 11883, tzinfo=utc), to='setup.Orario'),
            preserve_default=False,
        ),
    ]
