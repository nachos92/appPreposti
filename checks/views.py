from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from setup.models import *
from .models import Settimana, Segnalazione
import datetime as dt
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models.signals import post_save
from django.dispatch import receiver



def controlloPlanning(request, matricola):
    """ Es. <url> localhost/8000/checks/56
    Produce un json con la informazioni sui dipendenti da controllare e gli orari dei controlli.
    """

    print "### Controllo planning in corso... ###"

    i = Impostazione.objects.get(id=1)

    try:
        preposto = Preposto.objects.get(n_matr=matricola)
        foglio = '{"n_matr":"'+ preposto.getN_matr()+'",'
        foglio += '"nome":"' + preposto.first_name + '","cognome":"' + preposto.last_name + '",'
        foglio += '"reparti":['


        reparti = Settimana.objects.filter(
            cod_preposto__id=preposto.getID(),
            data_inizio__lte=date.today()
        )
        print "Numero 'reparti': "+str(len(reparti))


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
                    foglio += '"lun":{"orario":"'
                    if i.lunedi == False:
                        foglio += '"},'
                    else:
                        foglio += r.lunedi.getOrario_time()+'"},'

                    foglio += '"mar":{"orario":"'
                    if i.martedi == False:
                        foglio += '"},'
                    else:
                        foglio += r.martedi.getOrario_time()+'"},'

                    foglio += '"mer":{"orario":"'
                    if i.mercoledi == False:
                        foglio += '"},'
                    else:
                        foglio += r.mercoledi.getOrario_time()+'"},'

                    foglio += '"gio":{"orario":"'
                    if i.giovedi == False:
                        foglio += '"},'
                    else:
                        foglio += r.giovedi.getOrario_time()+'"},'

                    foglio += '"ven":{"orario":"'
                    if i.venerdi == False:
                        foglio += '"},'
                    else:
                        foglio += r.venerdi.getOrario_time()+'"},'

                    foglio += '"sab":{"orario":"'
                    if i.sabato == False:
                        foglio += '"},'
                    else:
                        foglio += r.sabato.getOrario_time()+'"},'
                    foglio += '"dom":{"orario":"'
                    if i.domenica == False:
                        foglio += '"}'
                    else:
                        foglio += r.domenica.getOrario_time()+'"}'

                    foglio += '},'

                    foglio += '"dipendenti":['
                    oggi = dt.date.today()
                    weekday = dt.date.today().weekday()


                    if weekday == 0 and i.lunedi == False:
                        foglio += ']'
                    elif weekday == 1 and i.martedi == False:
                        foglio += ']'
                    elif weekday == 2 and i.mercoledi == False:
                        foglio += ']'
                    elif weekday == 3 and i.giovedi == False:
                        foglio += ']'
                    elif weekday == 4 and i.venerdi == False:
                        foglio += ']'
                    elif weekday == 5 and i.sabato == False:
                        foglio += ']'
                    elif weekday == 6 and i.domenica == False:
                        foglio += ']'
                    elif ggChiusura.objects.filter(data=oggi).exists() == True:
                        foglio += ']'
                    else:
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
                            persone = Dipendente.objects.filter(impiego=r[0].getArea(), fatto=False)
                            iter_dip = 0
                            for d in persone:
                                iter_dip+=1
                                foglio += '{"n_matr":"' + d.getN_matr() + '",'
                                foglio += '"nome":"'+d.getNome()+'",'
                                foglio += '"cognome":"' + d.getCognome() + '",'
                                foglio += '"fatto":"' + d.getFatto_string()+'",'
                                foglio += '"controlli":['

                                iter_controlli = 0
                                for c in controlli_impiego:
                                    iter_controlli+=1
                                    foglio += '{'
                                    foglio += '"id":"'+str(c.id)+'",'
                                    foglio += '"titolo":"' + c.getTitolo() + '",'
                                    foglio += '"value":"F"}'

                                    if iter_controlli < len(controlli_impiego):
                                        foglio += ','


                                c_adhoc = d.getList_ContrAdHoc()
                                if len(c_adhoc)>0:
                                    foglio+=','

                                iter_c_adhoc = 0
                                for cc in c_adhoc:
                                    iter_c_adhoc +=1
                                    foglio += '{"id":"'+str(cc.id + 500)+'",'
                                    foglio+='"titolo":"'+cc.getTitolo()+'","value":"F"}'

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


            foglio += ']'                   #fine reparti

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
def visitato(request, matricola):

    received_json_data = json.loads(request.body)
    print "Ricevuto json da CLIENT:"
    print str(received_json_data)

    dip = Dipendente.objects.get(n_matricola=matricola)
    dip.fatto = True
    dip.save()

    if not received_json_data:
        print "----> Il dipendente "+matricola+" non ha controlli negativi!"
    else:
        dip = Dipendente.objects.get(n_matricola=matricola)
        testo = ("Elenco controlli con esito negativo da parte di "
                 +dip.getNome()
                 +' '
                 + dip.getCognome()
                 +': \n \n')


        for m in received_json_data['controlli']:

            testo += '-'+'\t'+str(m['titolo'])+'\n'

        Segnalazione.create(dip, testo).save()


    """
    Se sono stati visitati tutti i dipendenti,
    si imposta come Fatto il planning.
    """
    persone = Dipendente.objects.filter(impiego=dip.getImpiego())
    if len(persone.filter(fatto=False))==0:
        for p in persone:
            p = Dipendente.objects.get(n_matricola=p.getN_matr())
            p.fatto = False
            print "Dip. "+p.getCognome()+": T ---> "+str(p.fatto)
            p.save()

    return HttpResponse('')


'''
Devo reimpostare a False tutti gli attributi "Fatto"
dei dipendenti coinvolti.
'''
def fineGiro(request,matricola, id):
    plan = Settimana.objects.get(id=int(id))

    print "Ricevuto fineGiro dal preposto "+str(matricola)
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

    persone = Dipendente.objects.filter(impiego=plan.getArea())
    print "Persone: "
    print str(persone)
    for p in persone:
        d = Dipendente.objects.get(matricola=p.getN_matr())
        print "Dip. "+d.getCognome()+': T ---> F'
        d.fatto = False
        d.save()

    plan.save()


    return HttpResponse('')


#Handler con uso per debug

'''
@receiver(post_save, sender=Settimana)
def my_handler(sender, **kwargs):
    print "PROVAPROVA"
    print check_fuoriorario(Settimana.objects.get(pk=4).mercoledi)
'''