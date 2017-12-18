# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_impostazione_orari_selezione'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orario',
            name='nome',
            field=models.CharField(max_length=20),
        ),
    ]
