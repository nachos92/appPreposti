import datetime
from datetime import date
from django.core.mail import send_mail
from setup.models import Responsabile, Impostazione, ggChiusura
from models import Settimana, SegnalazionePrep
from django.conf import settings




# ----------------------------------------->
'''
Gruppo di funzioni che vanno selezionano l'attributo "standard" o inserito in impostazioni,
in base allo stato attivo/non attivo dell'oggetto impostazione.
'''

def selezMessaggio():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getMessaggio()
    except:
        print "Impostazione(pk=1) inesistente."
    else:
        return getattr(settings, "MESSAGGIO", None)

def selezMittente():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getSMTP_username()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "EMAIL_HOST_USER", None)

def selezPassword():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getSMTP_password()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "EMAIL_HOST_PASSWORD", None)

def selezSoglia_ore():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.get_sogliaControllo_ore()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "SOGLIA_ORE", None)

def selezSoglia_minuti():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.get_sogliaControllo_minuti()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "SOGLIA_MINUTI", None)


# <-----------------------------------------

################## Funzioni e variabili di supporto

def invio_email(x):
    try:
        send_mail(
            subject=('['+str(x.getPreposto())+'] Mancato giro controlli'),
            message= selezMessaggio(),
            from_email= selezMittente(),
            recipient_list=[
                Responsabile.objects.get(
                    last_name=x.getPreposto().getSuperiore()
                ).getEmail(),
            ],
            auth_user= selezMittente(),
            auth_password= selezPassword(),
            fail_silently=False
        )
        print "INVIO MAIL ----------"

    except:
        print "Errore send_mail"
    else:
        pass

soglia_tot = datetime.timedelta(
    hours=selezSoglia_ore(),
    minutes=selezSoglia_minuti()
)


inizioSettimana = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
fineSettimana = inizioSettimana + datetime.timedelta(days=6)


################## Fine funzioni e variabili di supporto




def check_giornochiusura():
    oggi = datetime.date.today()
    if(ggChiusura.objects.filter(data=oggi).exists() == True):
        pass
    else:
        check_controlli()



"""
Esegue il controllo periodico per verificare che i preposti non abbiano
dimenticato di fare un giro controlli o che non l'abbiano fatto fuori tempo limite (questo
secondo caso vuol dire che magari hanno iniziato tardi e all'orario limite devono ancora finire).
"""
def check_controlli():

    '''
    Per ogni elem di totali devo prima fare uno switch-case per il weekday e poi verifico
    se gg_check==false; nel caso, se gg_fatto==false invio una notifica al superiore.
    '''
    k = date.today().weekday()



    #Ottengo gli elem di Settimana nel periodo giusto
    totali = Settimana.objects.all()

    for x in totali:

        if (k == 0):
            if x.lun_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.lun,'%H:%M')+ soglia_tot).time():

                    if x.lun_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.lun_check = True
                    x.save()


        if (k == 1):
            if x.mar_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.mar,'%H:%M')+ soglia_tot).time():

                    if x.mar_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.mar_check = True
                    x.save()


        if (k == 2):
            if x.mer_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.mer,'%H:%M')+ soglia_tot).time():

                    if x.mer_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)



                    x.mer_check = True
                    x.save()


        if (k == 3):

            if x.gio_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.gio,'%H:%M')+ soglia_tot).time():

                    if x.gio_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.gio_check = True
                    x.save()



        if (k == 4):

            if x.ven_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.ven,'%H:%M')+ soglia_tot).time():

                    if x.ven_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.ven_check = True
                    x.save()


def check_impostazioni():
    '''
    try:
        imp = Impostazione.objects.get(pk=1)
        imp_fut = Impostazione.objects.get(pk=2)
    except:
        print "Imp. pk=1 e/o pk=2 mancanti."
    '''

    imp = Impostazione.objects.get(pk=1)
    imp_fut = Impostazione.objects.get(pk=2)


    if (imp_fut.attiva == True):
        if (imp_fut.is_today()):

            #Copia dei valori di #2 in #1
            imp.messaggio = imp_fut.getMessaggio()

            imp.sogliaControllo_ore = imp_fut.get_sogliaControllo_ore()
            imp.sogliaControllo_minuti = imp_fut.get_sogliaControllo_minuti()
            #manca ORARI SELEZIONE

            imp.data_inizio = imp_fut.data_inizio

            imp_fut.attiva = False
            imp_fut.save()

    if (imp_fut.attiva == False):
        if (imp_fut.is_today()==False):
            imp_fut.attiva=True
            imp_fut.save()


    if (imp.is_today()):
        imp.attiva = True
        imp.save()

    if (imp.data_inizio > date.today()):
        if imp.attiva == True:
            imp.attiva = False
            imp.save()