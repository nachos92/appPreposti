from models import Settimana, SegnalazionePrep
from datetime import date
from django.core.mail import send_mail
from setup.models import Responsabile,Preposto, Impostazione
import datetime



# ------- Variabili modificati in base ai valori di Impostazione
EMAIL_HOST = 'smtp.mail.yahoo.it'
EMAIL_HOST_USER = "piano_master92@yahoo.it"
EMAIL_HOST_PASSWORD = "zanarkand92"

MESSAGGIO = "Messaggio iniziale."


SOGLIA_ORE = 1
SOGLIA_MINUTI = 0

MITTENTE_USER = "piano_master92@yahoo.it"
MITTENTE_PASSW = "zanarkand92"


startDate = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
endDate = startDate + datetime.timedelta(days=6)

soglia_tot = datetime.timedelta(hours=SOGLIA_ORE, minutes=SOGLIA_MINUTI)


def aggiornaMessaggio(prima,dopo):
    prima = dopo

###-------- Fine blocco variabili



def invio_email(destinatario, messaggio):
    try:
        sett = Impostazione.objects.get(pk=1)
        send_mail(
        subject='SEGNALAZIONE',
        message=sett.getMessaggio(),
        from_email=sett.getSMTP_username(),
        recipient_list=[destinatario,],
        auth_user= sett.getSMTP_username(),
        auth_password= sett.getSMTP_password(),
        fail_silently=True
        )
    except:
        print "Errore invio email."
    else:
        pass


"""
Esegue il controllo periodico per verificare che i preposti non abbiano
dimenticato di fare un giro controlli o che non l'abbiano fatto fuori tempo limite (questo
secondo caso vuol dire che magari hanno iniziato tardi e all'orario limite devono ancora finire).
"""
def check_controlli():
    #Ottengo gli elem di Settimana nel periodo giusto
    totali = Settimana.objects.filter(
        data_inizio__range=[startDate, endDate],
    )

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
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())

                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=MESSAGGIO,
                            from_email=MITTENTE_USER,
                            recipient_list=[
                                Responsabile.objects.get(
                                    last_name=prep.getSuperiore()
                                ).getEmail(),
                            ],
                            auth_user=MITTENTE_USER,
                            auth_password=MITTENTE_PASSW,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=MESSAGGIO).save()
                    x.lun_check = True
                    x.save()

        if (k == 1):
            if x.mar_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.mar,'%H:%M') + soglia_tot).time():
                    if x.mar_fatto == False:
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())

                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=MESSAGGIO,
                            from_email=MITTENTE_USER,
                            recipient_list=[
                                Responsabile.objects.get(
                                    last_name=prep.getSuperiore()
                                ).getEmail(),
                            ],
                            auth_user=MITTENTE_USER,
                            auth_password=MITTENTE_PASSW,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=MESSAGGIO).save()
                    x.mar_check = True
                    x.save()

        if (k == 2):
            if x.mer_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.mer,'%H:%M') + soglia_tot).time():
                    if x.mer_fatto == False:

                        prep = Preposto.objects.get(last_name=x.getCod_preposto())


                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=Impostazione.objects.get(pk=1).getMessaggio(),
                            from_email=MITTENTE_USER,
                            recipient_list=[
                                Responsabile.objects.get(
                                    last_name=prep.getSuperiore()
                                ).getEmail(),
                            ],
                            auth_user=MITTENTE_USER,
                            auth_password=MITTENTE_PASSW,
                            fail_silently=True
                        )
                        

                        SegnalazionePrep.create(matr=prep, dett=MESSAGGIO).save()
                    x.mer_check = True
                    x.save()

        if (k == 3):

            if x.gio_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.gio,'%H:%M')+ soglia_tot).time():

                    if x.gio_fatto == False:
                        pass
                        '''
                        SegnalazionePrep.create(
                            matr=Preposto.objects.get(pk=x.getCod_preposto),
                            dett=MESSAGGIO
                        ).save()
                        '''

                    x.gio_check = True
                    x.save()


            '''
            if x.gio_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.gio,'%H:%M') + soglia_tot).time():
                    if x.gio_fatto == False:
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())
                        sett = Impostazione.objects.get(pk=1)

                        
                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=Impostazione.objects.get(pk=1).getMessaggio(),
                            from_email=MITTENTE_USER,
                            recipient_list=[
                                Responsabile.objects.get(
                                    last_name=prep.getSuperiore()
                                ).getEmail(),
                            ],
                            auth_user=MITTENTE_USER,
                            auth_password=MITTENTE_PASSW,
                            fail_silently=True
                        )
                        
                        SegnalazionePrep.create(matr=prep, dett=MESSAGGIO).save()
                    x.gio_check = True
                    x.save()
            '''
        if (k == 4):
            if x.ven_check == False:
                if datetime.datetime.now().time() > (datetime.datetime.strptime(x.ven,'%H:%M') + soglia_tot).time():
                    if x.ven_fatto == False:
                        prep = Preposto.objects.get(last_name=x.getCod_preposto())

                        # invio segnalazione via mail
                        send_mail(
                            subject='SEGNALAZIONE',
                            message=MESSAGGIO,
                            from_email=MITTENTE_USER,
                            recipient_list=[
                                Responsabile.objects.get(
                                    last_name=prep.getSuperiore()
                                ).getEmail(),
                            ],
                            auth_user=MITTENTE_USER,
                            auth_password=MITTENTE_PASSW,
                            fail_silently=True
                        )

                        SegnalazionePrep.create(matr=prep, dett=MESSAGGIO).save()

                    x.ven_check = True
                    x.save()
'''
def check_impostazioni():
    sett = Impostazione.objects.get(pk=1)
    if(sett.is_today()):
        global MESSAGGIO
        aggiornaMessaggio(MESSAGGIO,"ciaociao")
        sett.nuovo = False
        sett.save()

        #ASSEGNAZIONE DEI VALORI

        EMAIL_HOST = sett.getSMTP_server()
        EMAIL_HOST_USER = sett.getSMTP_username()
        EMAIL_HOST_PASSWORD = sett.getSMTP_password()


        SOGLIA_ORE = sett.get_sogliaControllo_ore()
        SOGLIA_MINUTI = sett.get_sogliaControllo_minuti()

        MITTENTE_USER = EMAIL_HOST_USER
        MITTENTE_PASSW = EMAIL_HOST_PASSWORD
'''
