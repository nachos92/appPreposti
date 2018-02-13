from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import signals
from datetime import date


'''
IDEA:
Ad un impiego si associano n controlli.
Ad un dipendente si associa 1 impiego.

'''
class Controllo(models.Model):

    titolo = models.CharField(max_length=40)
    descrizione = models.CharField(default='', max_length=250, blank=True)
    check = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titolo

    def getTitolo(self):
        return self.titolo
    def getDescrizione(self):
        return self.descrizione

    class Meta:
        verbose_name_plural = "Controlli"

'''
class ControlloAggiuntivo(Controllo):
    class Meta:
        verbose_name_plural = "Controlli aggiuntivi"

'''
class ControlloAggiuntivo(models.Model):
    titolo = models.CharField(max_length=40)
    descrizione = models.CharField(default='', max_length=250, blank=True)
    check = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titolo
    def getTitolo(self):
        return self.titolo


    class Meta:
        verbose_name_plural = "Controlli aggiuntivi"


class Impiego(models.Model):
    impiego = models.CharField(primary_key=True, max_length=20)
    controlli = models.ManyToManyField(Controllo, blank=True)

    def __unicode__(self):
        return self.impiego

    def getControlli(self):
        return self.controlli.all()

    class Meta:
        verbose_name_plural = "Impieghi"


class Responsabile(User):
    class Meta:
        verbose_name_plural = "Responsabili"
    def __unicode__(self):
        return self.last_name

    def getEmail(self):
        return self.email



class Preposto(User):
    n_matr = models.CharField(unique=True,max_length=8)
    sottoposti = models.ManyToManyField(Impiego, blank=True)
    superiore = models.ForeignKey(Responsabile, blank=True)

    class Meta:
        verbose_name_plural = "Preposti"
    def __unicode__(self):
        return (self.getID()+' - '+self.last_name)
    def getSuperiore(self):
        return str(self.superiore)
    def getN_matr(self):
        return self.n_matr
    def getID(self):
        return str(self.id)
    def getNome(self):
        return self.first_name
    def getCognome(self):
        return self.last_name

class Dipendente(models.Model):

    n_matricola = models.CharField(max_length=4, primary_key=True)
    nome = models.CharField(max_length=15)
    cognome = models.CharField(max_length=15)
    impiego = models.ForeignKey(Impiego)
    controlli_adhoc = models.ManyToManyField(
        ControlloAggiuntivo,
        blank=True,
        help_text="Selezionare o inserire ulteriori controlli specifici.",
    )
    class Meta:
        verbose_name_plural = "Dipendenti"
        ordering = [
            'cognome'
            ]

    def __unicode__(self):
        return self.n_matricola

    def getN_matr(self):
        return self.n_matricola
    def getNome(self):
        return self.nome
    def getCognome(self):
        return self.cognome
    def getList_ContrAdHoc(self):
        return self.controlli_adhoc.all()
    def getImpiego(self):
        return str(self.impiego)

    @classmethod
    def create(cls, matr, nome, cognome, impiego):
        dipendente = cls(
            matricola=matr,
            nome=nome,
            cognome=cognome,
            impiego=Impiego.objects.get(impiego=impiego)
        )
        return dipendente


class Orario(models.Model):
    nome = models.CharField(max_length=20)
    orario = models.TimeField()

    class Meta:
        verbose_name_plural = "Orari"
    def __unicode__(self):
        return self.nome
    def getNome(self):
        return self.nome
    def getOrario_string(self):
        return str(self.orario)
    def getOrario_time(self):
        return self.orario.strftime('%H:%M')
    def getChoices(self):
        pass



class Impostazione(models.Model):
    titolo = models.CharField(max_length=20)
    nuovo = models.BooleanField(default=True)

    '''
    Quando mi servono degli attributi di impostazione (es. messaggio mail)
    controllo che l'oggetto impostazione sia attivo: se si' prendo il valore dall'oggetto,
    altrimenti prendo il valore standard (es. MESSAGGIO_EMAIL).
    '''
    attiva = models.BooleanField(default=False)
    creazione = models.DateTimeField(auto_now_add=True)
    data_inizio = models.DateField(
        help_text="Inserire data dell'entrata in vigore delle impostazioni.",
        verbose_name="Data attivazione",
        blank=False,
    )
    smtp_server = models.CharField(max_length=20, verbose_name="Server smtp", default="none")
    smtp_username = models.CharField(max_length=30, verbose_name="Username (server smtp)")
    smtp_password = models.CharField(max_length=30,verbose_name="Password (server smtp)")
    port = models.IntegerField(default=587, help_text="Porta da usare (default=587).")

    messaggio = models.CharField(
        max_length=150,
        default="Il preposto non ha eseguito il giro controlli in data odierna.",
        help_text="Contenuto dell'email inviata quando un preposto non esegue un giro di controlli.",

    )
    orari_selezione = models.ManyToManyField(
        Orario,
        help_text="Orari disponibili nella compilazione del piano settimanale.",
    )

    sogliaControllo_ore = models.IntegerField(
        blank=False,
        help_text="Ore a disposizione per concludere il giro dei controlli.",
        verbose_name="Soglia ore"
    )
    sogliaControllo_minuti = models.IntegerField(
        blank=False,
        help_text="Minuti a disposizione per concludere il giro dei controlli.",
        verbose_name="Soglia minuti"
    )

    class Meta:
        verbose_name_plural = "Impostazioni"
        ordering = [
            '-id'
        ]
    def __unicode__(self):
        return str(self.id)
    def getSMTP_server(self):
        return self.smtp_server
    def getSMTP_username(self):
        return self.smtp_username
    def getSMTP_password(self):
        return self.smtp_password
    def getMessaggio(self):
        return self.messaggio
    def get_sogliaControllo_minuti(self):
        return self.sogliaControllo_minuti
    def get_sogliaControllo_ore(self):
        return self.sogliaControllo_ore
    def is_today(self):
        if self.data_inizio == date.today():
            return True
        else:
            return False
    def getChoices_orari(self):
        tupla = ()
        for i in self.orari_selezione.all():
            tupla += (i.getOrario_time,i.getOrario_time )

        return tupla