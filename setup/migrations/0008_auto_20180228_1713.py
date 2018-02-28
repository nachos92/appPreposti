# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0007_remove_impostazione_orari_selezione'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(to='setup.Impiego', null=True),
        ),
    ]
