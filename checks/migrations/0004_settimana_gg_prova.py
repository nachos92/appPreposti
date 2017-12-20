# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_auto_20171219_1945'),
        ('checks', '0003_remove_settimana_gg_prova'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='gg_prova',
            field=models.ForeignKey(to='setup.Orario', null=True),
        ),
    ]
