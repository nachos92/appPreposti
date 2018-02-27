# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_ggchiusura'),
        ('checks', '0013_auto_20180227_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='giovedi',
            field=models.ForeignKey(related_name='giovedi', to='setup.Orario', null=True),
        ),
        migrations.AddField(
            model_name='settimana',
            name='mercoledi',
            field=models.ForeignKey(related_name='mercoledi', to='setup.Orario', null=True),
        ),
        migrations.AddField(
            model_name='settimana',
            name='venerdi',
            field=models.ForeignKey(related_name='venerdi', to='setup.Orario', null=True),
        ),
    ]
