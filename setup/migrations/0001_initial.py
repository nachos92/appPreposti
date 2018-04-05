# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


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
                'verbose_name_plural': 'Controlli extra',
            },
        ),
        migrations.CreateModel(
            name='Dipendente',
            fields=[
                ('n_matricola', models.CharField(help_text=b'Lunghezza max: 10.', max_length=10, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=15)),
                ('cognome', models.CharField(max_length=15)),
                ('fatto', models.BooleanField(default=False)),
                ('controlli_extra', models.ManyToManyField(help_text=b'Controlli specifici.', to='setup.ControlloAggiuntivo', blank=True)),
            ],
            options={
                'ordering': ['cognome'],
                'verbose_name_plural': 'Dipendenti',
            },
        ),
        migrations.CreateModel(
            name='GiornoChiusura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(unique=True)),
            ],
            options={
                'ordering': ['data'],
                'verbose_name': 'Giorno chiusura',
                'verbose_name_plural': 'Giorni chiusura',
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
            name='Impostazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=20)),
                ('nuovo', models.BooleanField(default=True)),
                ('attiva', models.BooleanField(default=False)),
                ('creazione', models.DateTimeField(auto_now_add=True)),
                ('data_inizio', models.DateField(help_text=b"Inserire data dell'entrata in vigore delle impostazioni.", verbose_name=b'Data attivazione')),
                ('messaggio', models.TextField(default=b'Il preposto non ha eseguito il giro controlli in data odierna.', help_text=b"Contenuto dell'email inviata quando un preposto non esegue un giro di controlli.", max_length=150)),
                ('sogliaControllo_ore', models.IntegerField(default=1, help_text=b'Ore a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia ore')),
                ('sogliaControllo_minuti', models.IntegerField(default=0, help_text=b'Minuti a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia minuti')),
                ('lunedi', models.BooleanField(default=True)),
                ('martedi', models.BooleanField(default=True)),
                ('mercoledi', models.BooleanField(default=True)),
                ('giovedi', models.BooleanField(default=True)),
                ('venerdi', models.BooleanField(default=True)),
                ('sabato', models.BooleanField(default=True)),
                ('domenica', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'Impostazioni',
            },
        ),
        migrations.CreateModel(
            name='Orario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=20)),
                ('orario', models.TimeField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Orari dei controlli',
            },
        ),
        migrations.CreateModel(
            name='Preposto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('n_matr', models.CharField(unique=True, max_length=8, verbose_name=b'Num. matricola')),
                ('nome', models.CharField(max_length=20, verbose_name=b'nome')),
                ('cognome', models.CharField(max_length=20, verbose_name=b'cognome')),
                ('sottoposti', models.ManyToManyField(to='setup.Impiego', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Preposti',
            },
        ),
        migrations.CreateModel(
            name='Responsabile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('passw', models.CharField(default=b'password', help_text=b"Default: 'password'", max_length=20, verbose_name=b'Password')),
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
            field=models.ForeignKey(verbose_name=b'responsabile', to='setup.Responsabile'),
        ),
        migrations.AddField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(blank=True, to='setup.Impiego', null=True),
        ),
    ]
