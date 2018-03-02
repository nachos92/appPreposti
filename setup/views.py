from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import *
import csv
from django.contrib.auth.models import Group,Permission
import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

lista_scelte = []

'''
Funzioni di caricamento automatico.
Creano le istanze relative, mentre per i preposti e i responsabili creano gli appositi User,
coi quali effettuare l'accesso all'interfaccia di amministrazione.

La pagina fornira' un form dal quale caricare un file excel, dal quale verranno letti in automatico
i valori.
'''
class UploadFileForm(forms.Form):
    file = forms.FileField()

"""
Carico un xls con righe del tipo
<cognome> <nome>

Per ogni riga viene creato un User-Responsabile con
credenziali del tipo:
-username: cognome+iniziale maiuscola nome
-password: 0000 
"""

def uploadDip(request):

    if request.method == 'POST':
        print "Prova"

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            #reader = f.read().decode("utf-8")
            reader = csv.reader(f)
            #lines = reader.split("\n")

            for row in reader:
                #Correzioni delle stringhe.
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
                print "Conteggio: "+str(imp.count())
                if imp.count()== 1:
                    dip.impiego = Impiego.objects.get(pk="Falegnameria")


                dip.save()
            return HttpResponse("File valido!!")
    else:
        form = UploadFileForm()
    return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Excel file upload and download example',
                'header': ('Seleziona il file CSV dei ' +
                           'dipendenti da importare:')
    })


def start(request):
    messaggio = "Setup in corso:\n"

    messaggio = creaImpostazioniBase(messaggio)
    messaggio = creaGruppi(messaggio)

    return HttpResponse(messaggio)

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
        #print "Errore creazione 'Impostazione' attuale."
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
        #print "Errore creazione 'Impostazione' in programma."
        testo += "ERRORE"
    else:
        testo += "OK"

    return testo

def creaGruppi(testo):

    testo += "\nCreazione gruppo 'Responsabile'... \t"

    if len(Group.objects.all())!=2:
        try:
            g = Group(name="Responsabile", id=1)
            g.save()
        except:
            testo += "ERRORE"
        else:
            elenco_permessi = [
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
                'add_ggchiusura',
                'change_ggchiusura',
                'delete_ggchiusura',
            ]

            lista_permessi = []

            for p in elenco_permessi:
                lista_permessi.append(
                    Permission.objects.get(
                        codename=p
                    )
                )
            g.permissions = lista_permessi

            g.save()
            testo += "OK"
    else:
        testo += "ERRORE"


    testo += "\nCreazione gruppo 'Preposto'... \t\t"

    if len(Group.objects.all())!=2:
        try:
            x = Group(name="Preposto", id=2)
            x.save()
        except:
            testo += "ERRORE"
        else:
            elenco_permessi = [
                'add_controllo',
                'change_controllo',
                'delete_controllo',
                'add_controlloaggiuntivo',
                'change_controlloaggiuntivo',
                'delete_controlloaggiuntivo',
            ]

            lista_permessi = []

            for p in elenco_permessi:
                lista_permessi.append(
                    Permission.objects.get(
                        codename=p
                    )
                )
            x.permissions = lista_permessi

            x.save()
            testo += "OK"
    else:
        testo += "ERRORE"
    return testo

'''
def uploadPrep(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")

    else:
        form = UploadFileForm()
    return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Excel file upload and download example',
                'header': ('Seleziona il file .xls dei ' +
                           'preposti da importare:')
            })

def uploadResp(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")

    else:
        form = UploadFileForm()
    return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'title': 'Excel file upload and download example',
                'header': ('Seleziona il file .xls dei ' +
                           'responsabili da importare:')
            })
'''





### Handler per assegnare in automatico il gruppo di appartenenza all'utente
'''
@receiver(pre_save, sender=Responsabile)
def aaa(sender, instance, **kwargs):
    print "Pre-save"
    try:
        instance.groups.add(pk=1)

    except:
        print "Errore assegnazione gruppo: 'Responsabile'"
    else:
        print str(instance)
'''

'''
@receiver(pre_save, sender=Responsabile)
def hhh(sender, instance, **kwargs):
    try:
        g = Group.objects.get(name="responsabile")

        g.user_set.add(instance)

    except:
        print "Errore assegnazione gruppo: 'Responsabile'"

    else:
        print g.save()
        #instance.save()
'''

'''
@receiver(pre_save, sender=Preposto)
def bbb(sender, instance, **kwargs):
    try:
        super(instance).groups.add(id=2)
    except:
        print "Errore assegnazione gruppo: 'Preposto'"
'''


