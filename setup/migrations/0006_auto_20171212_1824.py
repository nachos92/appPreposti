# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0005_auto_20171129_1928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impostazione',
            options={'ordering': ['creazione'], 'verbose_name_plural': 'Impostazioni'},
        ),
        migrations.AddField(
            model_name='impostazione',
            name='creazione',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 12, 17, 24, 36, 832658, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
