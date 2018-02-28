from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django import forms
import django_excel as excel
from .models import Dipendente, Impiego, Impostazione, Orario

from django.db.models.signals import post_save
from django.dispatch import receiver
import csv



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



def carica(request):
    return HttpResponse("OK")


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


def start(request):

    return HttpResponse("Inizializzazione completata!")

def impostazioni(request):
    """
    Assegno i valori dell'entry di Impostazione piu' recente.

    """
    return HttpResponse('')


def dipProva(request):

    print "Match? "

    a = Impiego.objects.filter(pk="")
    if a.count() == 0:
        print "No"
    else:
        print "Yes"


    return HttpResponse("Prova")


