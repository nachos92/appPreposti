# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0008_auto_20180228_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(default=False, blank=True, to='setup.Impiego'),
            preserve_default=False,
        ),
    ]
