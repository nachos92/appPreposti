from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.forms import *
import django_excel as excel
from .models import Dipendente, Impiego

import csv



diz_settings = {}
'''
diz_settings['smtp_server']= EMAIL_HOST
diz_settings['smtp_username']= EMAIL_HOST_USER
diz_settings['smtp_password']= EMAIL_HOST_PASSWORD
diz_settings['port']= EMAIL_PORT
diz_settings['messaggio']= EMAIL_MESSAGE
'''




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

    if request == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            reader = csv.reader(open(request.FILES['file']))

            for row in reader:
                dip = Dipendente(
                    n_matricola=row[0],
                    nome=row[1],
                    cognome=row[2],
                    impiego= Impiego.objects.get(impiego=row[3]),
                )

                try:
                    dip.save()
                except:
                    print "Errore \n"
            return HttpResponse("OK!")
        else:
            return HttpResponseBadRequest('BAD')

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
    if request == 'POST':
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
    if request == 'POST':
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