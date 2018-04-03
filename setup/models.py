from django.db import models
from django.contrib.auth.models import User, Group, AbstractBaseUser
from django.db.models import signals
from datetime import date


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

class ControlloAggiuntivo(models.Model):
    titolo = models.CharField(max_length=40)
    descrizione = models.CharField(default='', max_length=250, blank=True)
    check = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titolo
    def getTitolo(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Controlli extra"

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
    passw = models.CharField(
        max_length=20,
        default="password",
        verbose_name="Password",
        help_text="Default: 'password'"
    )

    class Meta:
        verbose_name_plural = "Responsabili"
    def __unicode__(self):
        return self.last_name

    def getEmail(self):
        return self.email

class Preposto(models.Model):

    n_matr = models.CharField(unique=True,max_length=8, verbose_name="Num. matricola")
    nome = models.CharField(max_length=20, verbose_name="nome")
    cognome = models.CharField(max_length=20, verbose_name="cognome")
    sottoposti = models.ManyToManyField(Impiego, blank=True)
    superiore = models.ForeignKey(Responsabile, verbose_name="responsabile")

    class Meta:
        verbose_name_plural = "Preposti"
    def __unicode__(self):
        return (self.getN_matr()+' - '+self.cognome)
    def getSuperiore(self):
        return str(self.superiore)
    def getN_matr(self):
        return self.n_matr
    def getNome(self):
        return self.nome
    def getCognome(self):
        return self.cognome

class Dipendente(models.Model):

    n_matricola = models.CharField(max_length=10, primary_key=True,
                                   help_text="Lunghezza max: 10.")
    nome = models.CharField(max_length=15)
    cognome = models.CharField(max_length=15)
    impiego = models.ForeignKey(Impiego, blank=True,null=True)
    fatto = models.BooleanField(default=False)
    controlli_extra = models.ManyToManyField(
        ControlloAggiuntivo,
        blank=True,
        help_text="Controlli specifici."
    )
    class Meta:
        verbose_name_plural = "Dipendenti"
        ordering = [
            'cognome'
            ]
    def __unicode__(self):
        return self.n_matricola
    def getFatto_string(self):
        if (self.fatto):
            return 'T'
        else:
            return 'F'
    def getN_matr(self):
        return self.n_matricola
    def getNome(self):
        return self.nome
    def getCognome(self):
        return self.cognome
    def getList_ContrAdHoc(self):
        return self.controlli_extra.all()
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
    orario = models.TimeField(unique=True)

    class Meta:
        verbose_name_plural = "Orari dei controlli"

    def __unicode__(self):
        return (self.nome + ' - '+self.getOrario_time())
    def getNome(self):
        return self.nome
    def getOrario_string(self):
        return str(self.orario)
    def getOrario_time(self):
        return self.orario.strftime('%H:%M')
    def getOrario(self):
        return self.orario

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
    messaggio = models.TextField(
        max_length=150,
        default="Il preposto non ha eseguito il giro controlli in data odierna.",
        help_text="Contenuto dell'email inviata quando un preposto non esegue un giro di controlli.",

    )
    sogliaControllo_ore = models.IntegerField(
        default=1,
        help_text="Ore a disposizione per concludere il giro dei controlli.",
        verbose_name="Soglia ore"
    )
    sogliaControllo_minuti = models.IntegerField(
        default=0,
        help_text="Minuti a disposizione per concludere il giro dei controlli.",
        verbose_name="Soglia minuti"
    )

    lunedi = models.BooleanField(default=True)
    martedi = models.BooleanField(default=True)
    mercoledi = models.BooleanField(default=True)
    giovedi = models.BooleanField(default=True)
    venerdi = models.BooleanField(default=True)
    sabato = models.BooleanField(default=True)
    domenica = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Impostazioni"
        ordering = [
            '-id'
        ]
    def __unicode__(self):
        return str(self.id)
    def getMessaggio(self):
        return self.messaggio
    def getSogliaControllo_minuti(self):
        return self.sogliaControllo_minuti
    def getSogliaControllo_ore(self):
        return self.sogliaControllo_ore
    def is_today(self):
        if self.data_inizio == date.today():
            return True
        else:
            return False

class GiornoChiusura(models.Model):
    data = models.DateField(unique=True)
    def __unicode__(self):
        return str(self.data)
    class Meta:
        verbose_name = "Giorno chiusura"
        verbose_name_plural = "Giorni chiusura"
        ordering = [
            'data'
            ]