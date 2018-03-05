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
                'verbose_name_plural': 'Controlli extra',
            },
        ),
        migrations.CreateModel(
            name='Dipendente',
            fields=[
                ('n_matricola', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=15)),
                ('cognome', models.CharField(max_length=15)),
                ('controlli_extra', models.ManyToManyField(help_text=b'Selezionare o inserire ulteriori controlli specifici.', to='setup.ControlloAggiuntivo', blank=True)),
            ],
            options={
                'ordering': ['cognome'],
                'verbose_name_plural': 'Dipendenti',
            },
        ),
        migrations.CreateModel(
            name='ggChiusura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(unique=True)),
            ],
            options={
                'ordering': ['data'],
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
                ('messaggio', models.CharField(default=b'Il preposto non ha eseguito il giro controlli in data odierna.', help_text=b"Contenuto dell'email inviata quando un preposto non esegue un giro di controlli.", max_length=150)),
                ('sogliaControllo_ore', models.IntegerField(default=1, help_text=b'Ore a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia ore')),
                ('sogliaControllo_minuti', models.IntegerField(default=0, help_text=b'Minuti a disposizione per concludere il giro dei controlli.', verbose_name=b'Soglia minuti')),
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
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('n_matr', models.CharField(unique=True, max_length=8)),
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
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=15)),
                ('nome', models.CharField(max_length=20)),
                ('cognome', models.CharField(max_length=20)),
                ('n_matr', models.CharField(max_length=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='preposto',
            name='superiore',
            field=models.ForeignKey(to='setup.Responsabile', blank=True),
        ),
        migrations.AddField(
            model_name='dipendente',
            name='impiego',
            field=models.ForeignKey(blank=True, to='setup.Impiego', null=True),
        ),
    ]
