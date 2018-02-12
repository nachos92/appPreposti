# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_auto_20180212_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='impostazione',
            name='titolo',
            field=models.CharField(default='Prova', max_length=10),
            preserve_default=False,
        ),
    ]
