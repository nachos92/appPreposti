# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0012_auto_20180228_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impostazione',
            name='sogliaControllo_minuti',
            field=models.IntegerField(default=0, help_text=b'Minuti a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia minuti'),
        ),
        migrations.AlterField(
            model_name='impostazione',
            name='sogliaControllo_ore',
            field=models.IntegerField(default=1, help_text=b'Ore a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia ore'),
        ),
    ]
