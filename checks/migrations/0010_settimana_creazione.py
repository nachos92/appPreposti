# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0009_auto_20180227_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='creazione',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 27, 17, 31, 58, 902331, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
