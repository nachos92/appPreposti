# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_auto_20171212_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impostazione',
            options={'ordering': ['-creazione'], 'verbose_name_plural': 'Impostazioni'},
        ),
        migrations.AddField(
            model_name='impostazione',
            name='messaggio',
            field=models.TextField(default=b'Il preposto non ha eseguito il giro controlli in data odierna.', help_text=b"Contenuto dell'email inviata quando un preposto non esegue un giro di controlli."),
        ),
        migrations.AddField(
            model_name='impostazione',
            name='port',
            field=models.IntegerField(default=587, help_text=b'Porta da usare (default=587).'),
        ),
        migrations.AddField(
            model_name='impostazione',
            name='sogliaControllo_minuti',
            field=models.IntegerField(default=0, help_text=b"Entro quanti minuti dopo l'orario di inizio si puo' concludere il giro controlli."),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impostazione',
            name='sogliaControllo_ore',
            field=models.IntegerField(default=1, help_text=b"Entro quante ore dopo l'orario di inizio si puo' concludere il giro controlli."),
            preserve_default=False,
        ),
    ]
