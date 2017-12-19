# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_impostazione_nuovo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impostazione',
            name='data_inizio',
            field=models.DateField(help_text=b"Inserire data dell'entrata in vigore delle impostazioni.", verbose_name=b'Data attivazione'),
        ),
    ]
