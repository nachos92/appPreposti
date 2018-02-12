# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_impostazione_titolo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impostazione',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Impostazioni'},
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='titolo',
            field=models.CharField(max_length=20),
        ),
    ]
