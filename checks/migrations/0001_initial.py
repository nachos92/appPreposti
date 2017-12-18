# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segnalazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('dettaglio', models.TextField(max_length=200, blank=True)),
                ('matricola', models.ForeignKey(to='setup.Dipendente')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'segnalazioni (dipendenti)',
            },
        ),
        migrations.CreateModel(
            name='SegnalazionePrep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('dettaglio', models.TextField(max_length=200, blank=True)),
                ('matricola', models.ForeignKey(to='setup.Preposto')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'segnalazioni (preposti)',
            },
        ),
        migrations.CreateModel(
            name='Settimana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_inizio', models.DateField(help_text=b"Deve essere un lunedi'.")),
                ('lun', models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')])),
                ('mar', models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')])),
                ('mer', models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')])),
                ('gio', models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')])),
                ('ven', models.CharField(default=b'', max_length=10, choices=[(b'09:00', b'09:00'), (b'18:00', b'18:00')])),
                ('lun_fatto', models.BooleanField(default=False)),
                ('mar_fatto', models.BooleanField(default=False)),
                ('mer_fatto', models.BooleanField(default=False)),
                ('gio_fatto', models.BooleanField(default=False)),
                ('ven_fatto', models.BooleanField(default=False)),
                ('lun_check', models.BooleanField(default=False)),
                ('mar_check', models.BooleanField(default=False)),
                ('mer_check', models.BooleanField(default=False)),
                ('gio_check', models.BooleanField(default=False)),
                ('ven_check', models.BooleanField(default=False)),
                ('completato', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='setup.Impiego')),
                ('cod_preposto', models.ForeignKey(to='setup.Preposto')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'settimane',
            },
        ),
    ]
