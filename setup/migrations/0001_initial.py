# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controllo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=40)),
                ('descrizione', models.CharField(default=b'', max_length=250, blank=True)),
                ('check', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Controlli',
            },
        ),
        migrations.CreateModel(
            name='ControlloAggiuntivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=40)),
                ('descrizione', models.CharField(default=b'', max_length=250, blank=True)),
                ('check', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Controlli aggiuntivi',
            },
        ),
        migrations.CreateModel(
            name='Dipendente',
            fields=[
                ('n_matricola', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=15)),
                ('cognome', models.CharField(max_length=15)),
                ('controlli_adhoc', models.ManyToManyField(help_text=b'Selezionare o inserire ulteriori controlli specifici.', to='setup.ControlloAggiuntivo', blank=True)),
            ],
            options={
                'ordering': ['cognome'],
                'verbose_name_plural': 'Dipendenti',
            },
        ),
        migrations.CreateModel(
            name='Impiego',
            fields=[
                ('impiego', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('controlli', models.ManyToManyField(to='setup.Controllo', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Impieghi',
            },
        ),
        migrations.CreateModel(
            name='Orario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=10)),
                ('orario', models.TimeField()),
            ],
            options={
                'verbose_name_plural': 'Orari',
            },
        ),
        migrations.CreateModel(
            name='Preposto',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('n_matr', models.CharField(default=b'empty', max_length=10)),
                ('sottoposti', models.ManyToManyField(to='setup.Impiego', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Preposti',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Responsabile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Responsabili',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='preposto',
            name='superiore',
            field=models.ForeignKey(to='setup.Responsabile', blank=True),
        ),
        migrations.AddField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(to='setup.Impiego'),
        ),
    ]
