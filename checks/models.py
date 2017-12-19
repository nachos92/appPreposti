from django.db import models
from setup.models import Preposto, Impiego, Dipendente
from parametri import *



"""

@ <giorno>_fatto: viene reso True quando il preposto finisce la giornata.
@ <giorno>_check: viene reso True dopo il primo controllo fatto da crontab. 
"""
class Settimana(models.Model):
    cod_preposto = models.ForeignKey(Preposto)
    data_inizio = models.DateField(help_text="Deve essere un lunedi'.")
    area = models.ForeignKey(Impiego)

    lun = models.CharField(max_length=10, choices=orari, default='', null=False)
    mar = models.CharField(max_length=10, choices=orari, default='', null=False)
    mer = models.CharField(max_length=10, choices=orari, default='', null=False)
    gio = models.CharField(max_length=10, choices=orari, default='', null=False)
    ven = models.CharField(max_length=10, choices=orari, default='', null=False)

    lun_fatto = models.BooleanField(default=False)
    mar_fatto = models.BooleanField(default=False)
    mer_fatto = models.BooleanField(default=False)
    gio_fatto = models.BooleanField(default=False)
    ven_fatto = models.BooleanField(default=False)

    lun_check = models.BooleanField(default=False)
    mar_check = models.BooleanField(default=False)
    mer_check = models.BooleanField(default=False)
    gio_check = models.BooleanField(default=False)
    ven_check = models.BooleanField(default=False)

    completato = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    def getCod_preposto(self):
        return str(self.cod_preposto)

    def getArea(self):
        return str(self.area)
    def getDataInizio(self):
        return str(self.data_inizio)
    def getLun_orario(self):
        return self.lun
    def getMar_orario(self):
        return self.mar
    def getMer_orario(self):
        return self.mer
    def getGio_orario(self):
        return self.gio
    def getVen_orario(self):
        return self.ven


    class Meta:
        ordering = [
            '-id'
        ]
        verbose_name_plural = 'settimane'

class SegnalazionePrep(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    matricola = models.ForeignKey(Preposto)
    dettaglio = models.TextField(max_length=200, blank=True)

    @classmethod
    def create(cls, matr, dett):
        segnalazione = cls(matricola=matr, dettaglio=dett)
        return segnalazione

    def getMatricola(self):
        return str(self.matricola)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = [
            '-id'
        ]
        verbose_name_plural = 'segnalazioni (preposti)'


class Segnalazione(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    matricola = models.ForeignKey(Dipendente)
    dettaglio = models.TextField(max_length=200, blank=True)

    @classmethod
    def create(cls, matr, dett):
        segnalazione = cls(matricola=matr, dettaglio=dett)
        return segnalazione

    def getMatricola(self):
        return str(self.matricola)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = [
            '-id'
        ]
        verbose_name_plural = 'segnalazioni (dipendenti)'
