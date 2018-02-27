# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_ggchiusura'),
        ('checks', '0012_auto_20180227_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='lunedi',
            field=models.ForeignKey(related_name='lunedi', to='setup.Orario', null=True),
        ),
        migrations.AddField(
            model_name='settimana',
            name='martedi',
            field=models.ForeignKey(related_name='martedi', to='setup.Orario', null=True),
        ),
    ]
