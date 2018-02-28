# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_auto_20180228_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(to='setup.Impiego'),
        ),
    ]
