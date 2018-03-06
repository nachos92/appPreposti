from django.db import models
from setup.models import Preposto, Impiego, Dipendente, Impostazione,Orario
import datetime
from datetime import date
from setup.views import lista_scelte





"""

@ <giorno>_fatto: viene reso True quando il preposto finisce la giornata.
@ <giorno>_check: viene reso True dopo il primo controllo fatto da crontab. 
"""
class Settimana(models.Model):
    cod_preposto = models.ForeignKey(Preposto)
    creazione = models.DateTimeField(auto_now_add=True)
    data_inizio = models.DateField(help_text="Deve essere un lunedi'.")
    area = models.ForeignKey(Impiego)

    lunedi = models.ForeignKey(Orario, null=True, related_name='lunedi')
    martedi = models.ForeignKey(Orario, null=True, related_name='martedi')
    mercoledi = models.ForeignKey(Orario, null=True, related_name='mercoledi')
    giovedi = models.ForeignKey(Orario, null=True, related_name='giovedi')
    venerdi = models.ForeignKey(Orario, null=True, related_name='venerdi')

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
    debug = models.BooleanField(default=True)

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
    def getOrario_oggi(self):
        k = date.today().weekday()
        if k==0:
            return self.lunedi.orario
        if k==1:
            return self.martedi.orario
        if k==2:
            return self.mercoledi.orario
        if k==3:
            return self.giovedi.orario
        if k==4:
            return self.venerdi.orario


    '''
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
        return self.martedi
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
    '''

    def periodo_attivo(self):
        """
        Ritorna true quando mi trovo nel periodo di tempo in cui posso eseguire i controlli,
        ovvero a partire dall'orario di inizio ed entro la soglia max (es. 1 ora).

        :return:
        """
        imp = Impostazione.objects.get(pk=1)
        dnow = datetime.datetime.now().time()
        if (dnow > self.getOrario_oggi() and dnow <= (
            datetime.datetime.combine(
                datetime.date(1,1,1),
                self.getOrario_oggi()
            ) + datetime.timedelta(
                    hours=imp.getSogliaControllo_ore(),
                    minutes=imp.getSogliaControllo_minuti()
                )).time()
        ):
            return True
        else:
            return False


    class Meta:
        ordering = [
            '-id'
        ]
        verbose_name_plural = 'Planning settimanali'

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
