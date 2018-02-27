# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_ggchiusura'),
        ('checks', '0010_settimana_creazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='settimana',
            name='lunedi',
            field=models.ForeignKey(related_name='lunedi', default=datetime.datetime(2018, 2, 27, 18, 12, 44, 407232, tzinfo=utc), to='setup.Orario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settimana',
            name='martedi',
            field=models.ForeignKey(related_name='martedi', default=datetime.datetime(2018, 2, 27, 18, 12, 52, 4008, tzinfo=utc), to='setup.Orario'),
            preserve_default=False,
        ),
    ]
