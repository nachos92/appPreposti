# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0008_auto_20171219_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='impostazione',
            name='nuovo',
            field=models.BooleanField(default=True),
        ),
    ]
