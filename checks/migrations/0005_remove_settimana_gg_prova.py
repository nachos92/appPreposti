# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0004_settimana_gg_prova'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settimana',
            name='gg_prova',
        ),
    ]
