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
    data_inizio = models.DateField(help_text="Selezionare un lunedi'.")
    area = models.ForeignKey(Impiego)

    creazione = models.DateTimeField(auto_now_add=True)

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

    def periodo_attivo(self):
        """
        Ritorna TRUE se l'ora attuale e' compresa tra l'orario di inizio
        e l'orario massimo entro cui si possono eseguire i controlli
        (ora inizio+soglia_ore+soglia_minuti).

        """
        try:
            imp = Impostazione.objects.get(pk=1)
        except:
            print "-> periodo_attivo(): errore get Impostazione (pk=1)."
            return False
        else:
            ora_attuale = datetime.datetime.now().time()


            if (ora_attuale > self.getOrario_oggi()
                    and ora_attuale <= (
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
        verbose_name = 'Planning settimanale'

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
