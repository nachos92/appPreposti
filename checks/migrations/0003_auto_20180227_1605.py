# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0002_auto_20180212_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settimana',
            name='gio_festivo',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='lun_festivo',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='mar_festivo',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='mer_festivo',
        ),
        migrations.RemoveField(
            model_name='settimana',
            name='ven_festivo',
        ),
    ]
