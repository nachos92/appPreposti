# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_auto_20171219_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impostazione',
            name='messaggio',
            field=models.CharField(default=b'Il preposto non ha eseguito il giro controlli in data odierna.', help_text=b"Contenuto dell'email inviata quando un preposto non esegue un giro di controlli.", max_length=150),
        ),
    ]
