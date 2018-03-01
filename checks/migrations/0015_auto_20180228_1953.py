# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0014_auto_20180227_1918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settimana',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Planning settimanali'},
        ),
    ]
