# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_ggchiusura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impostazione',
            name='orari_selezione',
        ),
    ]
