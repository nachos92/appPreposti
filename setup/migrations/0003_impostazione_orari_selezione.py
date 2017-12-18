# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_impostazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='impostazione',
            name='orari_selezione',
            field=models.ManyToManyField(to='setup.Orario'),
        ),
    ]
