# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='area',
            field=models.ForeignKey(to='setup.Impiego'),
        ),
        migrations.AddField(
            model_name='settimana',
            name='cod_preposto',
            field=models.ForeignKey(to='setup.Preposto'),
        ),
        migrations.AddField(
            model_name='segnalazioneprep',
            name='matricola',
            field=models.ForeignKey(to='setup.Preposto'),
        ),
        migrations.AddField(
            model_name='segnalazione',
            name='matricola',
            field=models.ForeignKey(to='setup.Dipendente'),
        ),
    ]
