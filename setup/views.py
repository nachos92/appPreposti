from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import *
import csv, random
from django.contrib.auth.models import Group,Permission
import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

lista_scelte = []


class UploadFileForm(forms.Form):
    file = forms.FileField()


def uploadDip(request):

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                f = request.FILES['file']
                reader = csv.reader(f)

                for row in reader:
                    row = row[0].split(';')
                    row[0] = "".join(row[0].split())
                    row[1] = "".join(row[1].split())
                    row[2] = "".join(row[2].split())
                    row[3] = "".join(row[3].split())

                    dip = Dipendente()
                    dip.n_matricola = row[0]
                    dip.nome = row[1]
                    dip.cognome = row[2]

                    imp = Impiego.objects.filter(pk=str(row[3]))
                    if imp.count()== 1:
                        dip.impiego = Impiego.objects.get(pk=row[3])

                    dip.save()
                return HttpResponse("File valido. Importazione eseguita.")
            except:
                return HttpResponse("File NON valido.")
    else:
        form = UploadFileForm()
        return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Upload dipendenti',
                'header': ('Seleziona il file CSV dei ' +
                           'dipendenti:')
            }
        )

def uploadFestivi(request):

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)

        '''
        Validazione: controllo che il contenuto sia della forma giusta.
        '''
        if form.is_valid():
            try:
                f = request.FILES['file']
                reader = csv.reader(f)

                for row in reader:

                    gg = GiornoChiusura()
                    gg.data = row[0]
                    gg.save()

                return HttpResponse("File valido. Importazione eseguita.")
            except:
                return HttpResponse("File NON valido.")
    else:
        form = UploadFileForm()
    return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Upload giorni chiusura',
                'header': ('Seleziona il file CSV dei ' +
                           'giorni di chiusura:')
            }
    )


def creaImpostazioniBase(testo):
    testo += "\nCreazione 'Impostazione' 1... \t\t"
    try:
        att = Impostazione(
            id=1,
            titolo="ATTUALE",
            data_inizio= datetime.date.today(),
            messaggio= "Messaggio predefinito.",
        ).save()
    except:
        testo += "ERRORE"
    else:
        testo += "OK"

    testo += "\nCreazione 'Impostazione' 2... \t\t"
    try:
        fut = Impostazione(
            id=2,
            titolo="IN PROGRAMMA",
            data_inizio= datetime.date.today(),
            messaggio="Messaggio (futuro) predefinito.",
        ).save()
    except:
        testo += "ERRORE"
    else:
        testo += "OK"

    return testo

def creaImpieghi(testo):

    testo += "\nCreazione esempi di Impiego... \t\t"
    c = Controllo.objects.all()

    g = Impiego(
        impiego="Falegnameria",
    ).save()
    g = Impiego.objects.get(pk="Falegnameria")
    g.controlli = c
    g.save()

    try:


        for i in xrange(3):
            x = Impiego(
                pk=("Impiego esempio "+str(i))
            ).save()
            y = Impiego.objects.get(pk=("Impiego esempio "+str(i)))
            y.controlli.add(random.randint(0, 4))
            y.controlli.add(random.randint(0, 4))
            y.save()

    except:
        testo += "ERRORE"
    else:
        testo += "OK"

    return testo

def creaControlli(testo):

    testo += "\nCreazione esempi di Controllo... \t"
    try:
        for i in xrange(5):
            c = Controllo(
                id=i+1,
                titolo=("Controllo "+str(i+1))
            ).save()
    except:
        testo += "ERRORE"
    else:
        testo += "OK"
    return testo

def creaDipendenti(testo):
    testo += "\nCreazione esempi di Dipendente... \t"

    try:
        for i in xrange(10):
            d = Dipendente(
                n_matricola=random.randint(10,100),
                nome="Nome",
                cognome=("Cognome "+str(i)),
            )
            d.impiego= (Impiego.objects.all()[random.randint(0,3)])
            d.save()
    except:
        testo +="ERRORE"
    else:
        testo += "OK"

    return testo

def creaOrariControlli(testo):
    testo += "\nCreazione esempi di Orario...\t\t"
    try:
        o = Orario(
        nome="Mattino",
        orario="9:00"
        ).save()

        o = Orario(
            nome="Sera",
            orario="18:00"
        ).save()

        o = Orario(
            nome="Pomeriggio",
            orario="15:00"
        ).save()
    except:
        testo+= "ERRORE"
    else:
        testo += "OK"
    return testo

def creaSuperiore(testo):
    testo += "\nCreazione esempio di Responsabile...\t"
    try:
        r = Responsabile(

            first_name="Luca",
            last_name="Rossi",
            email="aa@example.it",

            username="resp1",
            password="resp",


        ).save()

    except:
        testo += "ERRORE"
    else:
        testo += "OK"
    return testo


def creaPreposto(testo):
    testo +="\nCreazione esempio di Preposto...\t"
    try:
        p = Preposto(
            n_matr="56",

            nome="Mauro",
            cognome="Bianchi",

            superiore=Responsabile.objects.all()[0],

        ).save()

    except:
        testo += "ERRORE"
    else:
        testo += "OK"

    return testo

def esempio(request):
    messaggio = "Popolamento database d'esempio.\n"

    messaggio = creaControlli(messaggio)
    messaggio = creaImpieghi(messaggio)
    messaggio = creaDipendenti(messaggio)
    messaggio = creaOrariControlli(messaggio)
    messaggio = creaSuperiore(messaggio)
    messaggio = creaPreposto(messaggio)

    return HttpResponse(messaggio)

def start(request):
    messaggio = "Setup in corso:\n"

    messaggio = creaImpostazioniBase(messaggio)

    return HttpResponse(messaggio)




### Handler per assegnare in automatico il gruppo di appartenenza all'utente


@receiver(pre_save, sender=Responsabile)
def setPassword(sender, instance, **kwargs):
    try:
        instance.set_password(instance.passw)
    except:
        print "Errore set-password Responsabile (signResponsabile())"


@receiver(post_save, sender=Responsabile)
def permessiResponsabili(sender, instance, **kwargs):

    #Assegnazione permessi
    elenco_permessi = [
        'add_user',
        'change_user',
        'delete_user',
        'add_logentry',
        'change_logentry',
        'delete_logentry',
        'add_controllo',
        'change_controllo',
        'delete_controllo',
        'add_controlloaggiuntivo',
        'change_controlloaggiuntivo',
        'delete_controlloaggiuntivo',
        'add_impiego',
        'change_impiego',
        'delete_impiego',
        'add_preposto',
        'change_preposto',
        'delete_preposto',
        'add_dipendente',
        'change_dipendente',
        'delete_dipendente',
        'add_orario',
        'change_orario',
        'delete_orario',
        'change_impostazione',
        'add_settimana',
        'change_settimana',
        'delete_settimana',
        'change_segnalazioneprep',
        'change_segnalazione',
        'add_giornochiusura',
        'change_giornochiusura',
        'delete_giornochiusura',
    ]

    lista_permessi = []

    for p in elenco_permessi:
        lista_permessi.append(
            Permission.objects.get(
                codename=p
            )
        )
    instance.user_permissions = lista_permessi
