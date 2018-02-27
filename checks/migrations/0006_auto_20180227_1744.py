# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0005_auto_20180227_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settimana',
            name='lun',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
