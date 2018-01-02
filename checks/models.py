from django.db import models
from setup.models import Preposto, Impiego, Dipendente, Impostazione,Orario
import datetime


"""
Orari in formato: datetime.time(HH,MM)
"""
inizio_turno = datetime.time(9, 0)
fine_turno = datetime.time(18, 0)

"""
Ogni orario che si vuole aggiungere alle scelte
deve essere prima creato come sopra, per poi essere aggiunto
alla tupla degli orari, rispettando il formato.
"""
orari = (
    (inizio_turno.strftime('%H:%M'), inizio_turno.strftime('%H:%M')),
    (fine_turno.strftime('%H:%M'), fine_turno.strftime('%H:%M')),
)




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

    lun_festivo = models.BooleanField(default=False)
    mar_festivo = models.BooleanField(default=False)
    mer_festivo = models.BooleanField(default=False)
    gio_festivo = models.BooleanField(default=False)
    ven_festivo = models.BooleanField(default=False)

    completato = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    def getId(self):
        return str(self.id)
    def getCod_preposto(self):
        return str(self.cod_preposto)
    def getPreposto(self):
        return self.cod_preposto

    def getArea(self):
        return str(self.area)
    def getDataInizio(self):
        return str(self.data_inizio)

    def getGiornoInizio(self):
        return self.data_inizio.strftime("%d")
    def getMeseInizio(self):
        return self.data_inizio.strftime("%m")
    def getAnnoInizio(self):
        return self.data_inizio.strftime("%Y")


    def getLun_orario(self):
        return self.lun
    def getLun_HH(self):
        return self.lun[:2]
    def getLun_MM(self):
        return self.lun[-2:]

    def getMar_orario(self):
        return self.mar
    def getMar_HH(self):
        return self.mar[:2]
    def getMar_MM(self):
        return self.mar[-2:]

    def getMer_orario(self):
        return self.mer
    def getMer_HH(self):
        return self.mer[:2]
    def getMer_MM(self):
        return self.mer[-2:]

    def getGio_orario(self):
        return self.gio
    def getGio_HH(self):
        return self.gio[:2]
    def getGio_MM(self):
        return self.gio[-2:]

    def getVen_orario(self):
        return self.ven
    def getVen_HH(self):
        return self.ven[:2]
    def getVen_MM(self):
        return self.ven[-2:]

    def periodo_attivo(self):
        '''
        Se mi trovo dopo l'orario di inizio.

        :return:
        '''

        d = datetime.datetime.strptime(self.getMar_HH()+':'+self.getMar_MM(),'%H:%M').time()
        dnow = datetime.datetime.now().time()
        if dnow > d:
            print "Posso eseguire i controlli"
            return True
        else:
            print "Non posso eseguire i controlli"
            return False

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
