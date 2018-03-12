from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from setup.models import *
from .models import Settimana, Segnalazione
import datetime as dt
from django.views.decorators.csrf import csrf_exempt
import json
from crons import inizioSettimana,fineSettimana, check_fuoriorario
from django.db.models.signals import post_save
from django.dispatch import receiver



def controlloPlanning(request, cod_prep):
    """ Es. <url> localhost/8000/checks/56
    Produce un json con la informazioni sui dipendenti da controllare e gli orari dei controlli.
    """

    print "### Controllo planning in corso... ###"


    try:
        preposto = Preposto.objects.get(n_matr=cod_prep)
        foglio = '{"n_matr":"'+ preposto.getN_matr()+'",'
        foglio += '"nome":"' + preposto.first_name + '","cognome":"' + preposto.last_name + '",'
        foglio += '"reparti":['


        reparti = Settimana.objects.filter(
            cod_preposto__id=preposto.getID(),
            data_inizio__lte=date.today()
        )
        print "Numero 'reparti': "+str(len(reparti))

        '''
        gg = date.today().weekday()

        if (gg == 0):
            reparti = reparti.filter(lun_fatto=False, lun_check=False)
        if (gg == 1):
            reparti = reparti.filter(mar_fatto=False, mar_check=False)
        if (gg == 2):
            reparti = reparti.filter(mer_fatto=False, mer_check=False)
        if (gg == 3):
            reparti = reparti.filter(gio_fatto=False, gio_check=False)
        if (gg == 4):
            reparti = reparti.filter(ven_fatto=False, ven_check=False)
        '''


        if len(reparti)==0:
            foglio += ']'
        else:
            iter = 0
            for r in reparti:
                if r.debug or r.periodo_attivo()== True:
                    controlli_impiego = Impiego.objects.get(pk=r.getArea()).getControlli()

                    iter+=1

                    foglio += '{"id":"'+ r.getId()+'",'
                    foglio += '"nome":"'+r.getArea()+'",'
                    foglio += '"data_inizio":"'
                    foglio += r.getDataInizio() +'",'
                    foglio += '"fatto":"F",'

                    foglio += '"orario":{'
                    foglio += '"lun":{"orario":"'+r.lunedi.getOrario_time()+'"},'
                    foglio += '"mar":{"orario":"'+r.martedi.getOrario_time()+'"},'
                    foglio += '"mer":{"orario":"'+r.mercoledi.getOrario_time()+'"},'
                    foglio += '"gio":{"orario":"'+r.giovedi.getOrario_time()+'"},'
                    foglio += '"ven":{"orario":"'+r.venerdi.getOrario_time()+'"}'
                    foglio += '},'

                    foglio += '"dipendenti":['



                    gg = date.today().weekday()
                    r = Settimana.objects.filter(pk=r.id)

                    if (gg == 0):
                        r = r.filter(lun_fatto=False, lun_check=False)
                    if (gg == 1):
                        r = r.filter(mar_fatto=False, mar_check=False)
                    if (gg == 2):
                        r = r.filter(mer_fatto=False, mer_check=False)
                    if (gg == 3):
                        r = r.filter(gio_fatto=False, gio_check=False)
                    if (gg == 4):
                        r = r.filter(ven_fatto=False, ven_check=False)


                    if len(r)!=0:

                        persone = Dipendente.objects.filter(impiego=r[0].getArea())
                        iter_dip = 0
                        for d in persone:
                            iter_dip+=1
                            foglio += '{"n_matr":"' + d.getN_matr() + '",'
                            foglio += '"nome":"'+d.getNome()+'",'
                            foglio += '"cognome":"' + d.getCognome() + '",'
                            foglio += '"fatto":"F",'
                            foglio += '"controlli":['

                            iter_controlli = 0
                            for c in controlli_impiego:
                                iter_controlli+=1
                                foglio += '{'
                                foglio += '"titolo":"' + c.getTitolo() + '",'
                                foglio += '"value":"F"}'

                                if iter_controlli < len(controlli_impiego):
                                    foglio += ','


                            c_adhoc = d.getList_ContrAdHoc()
                            if len(c_adhoc)>0:
                                foglio+=','
                            #else:
                            #    foglio += ']'

                            iter_c_adhoc = 0
                            for cc in c_adhoc:
                                iter_c_adhoc +=1
                                foglio += '{"titolo":"'+cc.getTitolo()+'","value":"F"}'

                                if iter_c_adhoc < len(c_adhoc):
                                    foglio += ','

                            foglio += ']'   #fine controlli

                            foglio += '}'   #fine dipendente

                        if iter_dip < len(persone):
                            foglio += ','

                    foglio += ']'   #fine dipendenti


                    foglio += '}'       #fine reparto
                if iter < len(reparti):
                    foglio += ','


            foglio += ']'           #fine reparti

        foglio += '}'                       #fine json
        return HttpResponse(
            foglio,
            content_type='application/json'
        )

    except Preposto.DoesNotExist:
        print "Nessun match col n_matr passato"
        raise Http404

def orarioPlanning(request, id):
    try:
        plan = Settimana.objects.get(pk=id)
    except:
        return Http404()
    else:
        foglio = '{'
        foglio += '"orario":{'
        foglio += '"lun":{"orario":"' + plan.lunedi.getOrario_time() + '"},'
        foglio += '"mar":{"orario":"' + plan.martedi.getOrario_time() + '"},'
        foglio += '"mer":{"orario":"' + plan.mercoledi.getOrario_time() + '"},'
        foglio += '"gio":{"orario":"' + plan.giovedi.getOrario_time() + '"},'
        foglio += '"ven":{"orario":"' + plan.venerdi.getOrario_time() + '"}'
        foglio += '}}'

        return HttpResponse(
            foglio,
            content_type='application/json'
        )





"""
Ricezione del json contenente i controlli con esito negativo di un dipendente.
Viene quindi creata una Segnalazione che riporta l'accaduto.
"""
@csrf_exempt
def ricezione(request, n_matricola):

    received_json_data = json.loads(request.body)
    print str(received_json_data)

    if (len(received_json_data['controlli']) == 0):
        print "0"
        return HttpResponse('')

    # Creo una segnalazione di controllo non positivo su un determinato dipendente.
    dip = Dipendente.objects.get(n_matricola=n_matricola)

    testo = ("Elenco controlli non rispettati da parte di "
             +dip.getNome()
             +' '
             + dip.getCognome()
             +': \n \n')


    for m in received_json_data['controlli']:

        testo += '-'+str(m['titolo'])+'\n'

    Segnalazione.create(dip, testo).save()

    print "Ricevuto json da CLIENT."

    return HttpResponse('')


"""## VARIABILE DI DEBUG ##"""
"""
Se la conferma del giro completato arriva fuori orario (prima dell'inizio
o dopo tempo_inizio+soglia_ore e minuti, non si imposta a True. 
"""
@csrf_exempt
def daydone(request):
    j = json.loads(request.body)

    for s in j['reparti']:
        plan = Settimana.objects.get(id=int(s['id_settimana']))

        k = date.today().weekday()
        if plan.debug==True or plan.periodo_attivo()==True:

            if (k == 0):
                plan.lun_fatto = True
            if (k == 1):
                plan.mar_fatto = True
            if (k == 2):
                plan.mer_fatto = True
            if (k == 3):
                plan.gio_fatto = True
            if (k == 4):
                plan.ven_fatto = True

            plan.save()

    return HttpResponse('')


def fineGiro(request,n_matricola, id_sett):
    plan = Settimana.objects.get(id=int(id_sett))

    print "Ricevuto fineGiro dal preposto "+str(n_matricola)
    k = date.today().weekday()

    if (k == 0):
        plan.lun_fatto = True
    if (k == 1):
        plan.mar_fatto = True
    if (k == 2):
        plan.mer_fatto = True
    if (k == 3):
        plan.gio_fatto = True
    if (k == 4):
        plan.ven_fatto = True

    plan.save()


    return HttpResponse('')


#Handler con uso per debug

'''
@receiver(post_save, sender=Settimana)
def my_handler(sender, **kwargs):
    print "PROVAPROVA"
    print check_fuoriorario(Settimana.objects.get(pk=4).mercoledi)
'''