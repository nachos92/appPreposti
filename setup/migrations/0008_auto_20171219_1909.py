# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0007_auto_20171212_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='impostazione',
            name='data_inizio',
            field=models.DateField(default=datetime.datetime(2017, 12, 19, 18, 9, 13, 100448, tzinfo=utc), help_text=b"Inserire data dell'entrata in vigore delle impostazioni.", verbose_name=b'Inizio applicazione delle impostazioni.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='orari_selezione',
            field=models.ManyToManyField(help_text=b'Orari disponibili nella compilazione del piano settimanale.', to='setup.Orario'),
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='sogliaControllo_minuti',
            field=models.IntegerField(help_text=b'Minuti a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia minuti'),
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='sogliaControllo_ore',
            field=models.IntegerField(help_text=b'Ore a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia ore'),
        ),
    ]
