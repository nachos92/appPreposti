# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0007_auto_20180227_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settimana',
            name='lun',
            field=models.CharField(max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
    ]
