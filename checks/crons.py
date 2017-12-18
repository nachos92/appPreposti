from subprocess import call
from parametri import *
from models import Settimana, SegnalazionePrep
from datetime import date
from django.core.mail import send_mail
from setup.models import Responsabile,Preposto

import smtplib

"""
Esegue il controllo periodico per verificare che i preposti non abbiano
dimenticato di fare un giro controlli o che non l'abbiano fatto fuori tempo limite (questo
secondo caso vuol dire che magari hanno iniziato tardi e all'orario limite devono ancora finire).
"""

soglia_tot = datetime.timedelta(hours=SOGLIA_ORE, minutes=SOGLIA_MINUTI)

def invio_email(destinatario, messaggio):
    try:
        send_mail(
        subject='SEGNALAZIONE',
        message=messaggio,
        from_email=mittente_user,
        recipient_list=[destinatario,],
        auth_user=mittente_user,
        auth_password=mittente_passw,
        fail_silently=True
        )
    except:
        print "Errore invio email."
    else:
        pass


def my_job():
    #Ottengo gli elem di Settimana nel periodo giusto
    totali = Settimana.objects.filter(data_inizio__range=[startDate, endDate], completato=False)

    '''
    Per ogni elem di totali devo prima fare uno switch-case per il weekday e poi verifico
    se gg_check==false; nel caso, se gg_fatto==false invio una notifica al superiore.
    '''
    k = date.today().weekday()

    for x in totali:

        if (k == 0):
            if x.lun_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.lun,'%H:%M') + soglia_tot).time():
                    if x.lun_fatto == False:
                        #invio segnalazione
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        message = "Il preposto ID: " + \
                                    prep.getID() + \
                                    " non ha eseguito o non ha eseguito in tempo " + \
                                    "i controlli in data odierna."
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=message,
                            from_email=mittente_user,
                            recipient_list=[Responsabile.objects.get(
                                last_name=prep.getSuperiore()
                            ).getEmail(), ],
                            #auth_user=mittente_user,
                            #auth_password=mittente_passw,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep,dett=message).save()
                    x.lun_check = True
                    x.save()

        if (k == 1):
            if x.mar_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.mar,'%H:%M') + soglia_tot).time():
                    if x.mar_fatto == False:

                        # invio segnalazione
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        message = "Il preposto ID: " + \
                                  prep.getID() + \
                                  " non ha eseguito o non ha eseguito in tempo " + \
                                  "i controlli in data odierna."
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=message,
                            from_email=mittente_user,
                            recipient_list=[Responsabile.objects.get(
                                last_name=prep.getSuperiore()
                            ).getEmail(), ],
                            # auth_user=mittente_user,
                            # auth_password=mittente_passw,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=message).save()
                    x.mar_check = True
                    x.save()

        if (k == 2):
            if x.mer_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.mer,'%H:%M') + soglia_tot).time():
                    if x.mer_fatto == False:

                        # invio segnalazione
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        message = "Il preposto ID: " + \
                                  prep.getID() + \
                                  " non ha eseguito o non ha eseguito in tempo " + \
                                  "i controlli in data odierna."
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=message,
                            from_email=mittente_user,
                            recipient_list=[Responsabile.objects.get(
                                last_name=prep.getSuperiore()
                            ).getEmail(), ],
                            # auth_user=mittente_user,
                            # auth_password=mittente_passw,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=message).save()
                    x.mer_check = True
                    x.save()

        if (k == 3):
            if x.gio_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.gio,'%H:%M') + soglia_tot).time():
                    if x.gio_fatto == False:

                        # invio segnalazione
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        message = "Il preposto ID: " + \
                                  prep.getID() + \
                                  " non ha eseguito o non ha eseguito in tempo " + \
                                  "i controlli in data odierna."
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=message,
                            from_email=mittente_user,
                            recipient_list=[Responsabile.objects.get(
                                last_name=prep.getSuperiore()
                            ).getEmail(), ],
                            # auth_user=mittente_user,
                            # auth_password=mittente_passw,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=message).save()
                    x.gio_check = True
                    x.save()

        if (k == 4):
            if x.ven_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.ven,'%H:%M') + soglia_tot).time():
                    if x.ven_fatto == False:

                        # invio segnalazione
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        message = "Il preposto ID: " + \
                                  prep.getID() + \
                                  " non ha eseguito o non ha eseguito in tempo " + \
                                  "i controlli in data odierna."
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=message,
                            from_email=mittente_user,
                            recipient_list=[Responsabile.objects.get(
                                last_name=prep.getSuperiore()
                            ).getEmail(), ],
                            # auth_user=mittente_user,
                            # auth_password=mittente_passw,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=message).save()

                    x.ven_check = True
                    x.save()


