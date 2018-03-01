# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0011_auto_20180228_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controlloaggiuntivo',
            options={'verbose_name_plural': 'Controlli extra'},
        ),
        migrations.AlterModelOptions(
            name='orario',
            options={'verbose_name_plural': 'Orari dei controlli'},
        ),
    ]
