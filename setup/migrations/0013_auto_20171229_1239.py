# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0012_auto_20171229_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preposto',
            name='n_matr',
            field=models.CharField(unique=True, max_length=8),
        ),
    ]
