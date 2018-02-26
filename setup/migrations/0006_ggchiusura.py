# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0005_auto_20180226_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='ggChiusura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(unique=True)),
            ],
            options={
                'ordering': ['data'],
                'verbose_name_plural': 'Giorni chiusura',
            },
        ),
    ]
