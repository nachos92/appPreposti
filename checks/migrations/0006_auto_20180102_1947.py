# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0005_remove_settimana_gg_prova'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='gio_festivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settimana',
            name='lun_festivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settimana',
            name='mar_festivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settimana',
            name='mer_festivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settimana',
            name='ven_festivo',
            field=models.BooleanField(default=False),
        ),
    ]
