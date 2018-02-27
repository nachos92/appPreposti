# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0004_auto_20180227_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='gio',
            field=models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
        migrations.AddField(
            model_name='settimana',
            name='lun',
            field=models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
        migrations.AddField(
            model_name='settimana',
            name='mar',
            field=models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
        migrations.AddField(
            model_name='settimana',
            name='mer',
            field=models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
        migrations.AddField(
            model_name='settimana',
            name='ven',
            field=models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')]),
        ),
    ]
