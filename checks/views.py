from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from setup.models import *
from .models import Settimana, Segnalazione
import datetime as dt
from django.views.decorators.csrf import csrf_exempt
import json
from crons import inizioSettimana,fineSettimana
from django.db.models.signals import post_save
from django.dispatch import receiver




def makeDict():
    """
    Costruisce un dizionario del tipo
    diz['impiego'] = [ <listacontrolliassociati> ]

    """
    diz = {}
    lista_impieghi = Impiego.objects.values_list('impiego', flat=True).all()

    for q in lista_impieghi:

        elenco_controlli = Impiego.objects.filter(impiego=q).values_list('controlli', flat=True).all()

        elenco_controlli = list(elenco_controlli)

        for x in range(0, len(elenco_controlli)):
            elenco_controlli[x] = str(elenco_controlli[x])
        diz[str(q)] = elenco_controlli

    return diz




"""
Ritorna un oggetto di lunghezza 0 se nella giornata attuale
e' gia' stato fatto il giro (se giornoattuale_fatto=true).
"""
def getWeek(cod_prep):
    """
    Prende in ingresso l'elenco dei dipendenti.
    Per la lista dei controlli accede al campo "impiego" del dipendente e lo usa come chiave di ricerca
    nel dizionario.

    Es. JSON generato:

    {
      "nome": "<nome>",
      "cognome": "<cognome>",
      "completato": "F",
      "id": "12",
      "lun": "09:00",
      "mar": "09:00",
      "mer": "09:00",
      "gio": "09:00",
      "ven": "09:00",
      "dipendenti": [
        {
          "n_matricola": "524",
          "nome": "Paolo",
          "cognome": "Bianchi",
          "impiego": "Operaio",
          "controlli": [
            {
              "id": "1",
              "titolo": "Controllo 1",
              "value": "F"
            },
            {
              "id": "3",
              "titolo": "Controllo 3",
              "value": "F"
            },
            {
              "id": "5",
              "titolo": "Abbigliamento antinfortunistico",
              "value": "F"
            }
          ],
          "controlli_adhoc": [
            {
              "titolo": "Controllo auto",
              "value": "F"
            }
          ]
        },
        ]
        }
    """

    planning = Settimana.objects.filter(
        data_inizio__range=[inizioSettimana, fineSettimana],
        cod_preposto=cod_prep,
        completato=False).values_list(
        'data_inizio',
        'area',
        'lun',
        'mar',
        'mer',
        'gio',
        'ven',
        'completato',
        'id'
    )
    return planning



def controlloPlanning(request, cod_prep):
    """ Es. se io vado su localhost/8000/checks/56
    mi stampa l'elenco dei dipendenti che il preposto 56
    non ha ancora controllato.
    """

    print "### Controllo planning in corso... ###"
    gruppo_sottoposti = Preposto.objects.filter(id=cod_prep).values_list('sottoposti')

    # elenco dipendenti del settore che il preposto deve controllare
    dipendenti = Dipendente.objects.filter(impiego__in=gruppo_sottoposti).values_list('n_matricola',
                                                                                      'nome',
                                                                                      'cognome',
                                                                                      'impiego',
                                                                                      )
    #print "Dipendenti totali: " + str(len(dipendenti)) + '\n' + str(dipendenti)
    planning = getWeek(cod_prep)

    try:
        preposto = Preposto.objects.get(n_matr=cod_prep)
        foglio = '{"nome":"' + preposto.first_name + '","cognome":"' + preposto.last_name + '",'
        foglio += '"n_matr":"'+ preposto.getN_matr()+'",'
        foglio += '"reparti":['

        gg = date.today().weekday()

        reparti = Settimana.objects.filter(
            cod_preposto__id=preposto.getID(),
            #data_inizio__range=[inizioSettimana,fineSettimana]
        )


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


        if len(reparti)==0:
            foglio += ']'
            print "Len == 0"
        else:
            iter = 0
            for r in reparti:
                if r.periodo_attivo()== True:
                    controlli_impiego = Impiego.objects.get(pk=r.getArea()).getControlli()

                    iter+=1
                    foglio += '{"nome":"'+r.getArea()+'",'
                    foglio += '"id":"'+ r.getId()+'",'
                    foglio += '"fatto":"F",'
                    foglio += '"data_inizio":{'
                    foglio += '"giorno":"'+ r.getGiornoInizio()+'",'
                    foglio += '"mese":"'+ r.getMeseInizio()+'",'
                    foglio += '"anno":"' +r.getAnnoInizio()+'"},'
                    foglio += '"orario":{'

                    #foglio += '"lun":{"hh":"'+r.getLun_HH()+'","mm":"'+r.getLun_MM()+'",'
                    foglio += '"lun":{"orario":"'+r.lunedi.getOrario_time()+'"},'

                    #foglio += '"mar":{"hh":"' + r.getMar_HH() + '","mm":"' + r.getMar_MM() + '",'
                    foglio += '"mar":{"orario":"'+r.martedi.getOrario_time()+'"},'

                    #foglio += '"mer":{"hh":"' + r.getMer_HH() + '","mm":"' + r.getMer_MM() + '",'
                    foglio += '"mer":{"orario":"'+r.mercoledi.getOrario_time()+'"},'

                    #foglio += '"gio":{"hh":"' + r.getGio_HH() + '","mm":"' + r.getGio_MM() + '",'
                    foglio += '"gio":{"orario":"'+r.giovedi.getOrario_time()+'"},'

                    #foglio += '"ven":{"hh":"' + r.getVen_HH() + '","mm":"' + r.getVen_MM() + '",'
                    foglio += '"ven":{"orario":"'+r.venerdi.getOrario_time()+'"}'

                    foglio += '},'
                    foglio += '"dipendenti":['



                    persone = Dipendente.objects.filter(impiego=r.getArea())
                    iter_dip = 0
                    for d in persone:
                        iter_dip+=1
                        foglio += '{"nome":"'+d.getNome()+'",'
                        foglio += '"cognome":"' + d.getCognome() + '",'
                        foglio += '"n_matr":"' + d.getN_matr() + '",'
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
                        iter_c_adhoc = 0
                        for cc in c_adhoc:
                            iter_c_adhoc +=1
                            foglio += '{"titolo":"'+cc.getTitolo()+'","value":"F"}'

                            if iter_c_adhoc < len(c_adhoc):
                                foglio += ','

                        foglio += ']'
                        foglio +='}'

                        if iter_dip < len(persone):
                            foglio += ','

                    foglio += ']'
                    foglio += '}'
                    if iter < len(reparti):
                        foglio += ','
            foglio += ']'
        foglio += '}'
        return HttpResponse(
            foglio,
            content_type='application/json'
        )

    except Preposto.DoesNotExist:
        print "Nessun match col n_matr passato"
        raise Http404
        #return HttpResponse("Nessun match col n_matr passato")






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



@csrf_exempt
def daydone(request):
    j = json.loads(request.body)

    for s in j['reparti']:
        plan = Settimana.objects.get(id=int(s['id_settimana']))

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
    #print str(Settimana.objects.get(id=4).martedi.getOrario() + timedelta(hours=1))
    #print str(datetime(Settimana.objects.get(id=4).martedi.getOrario_time())+ datetime.timedelta(hours=1))
    print((dt.datetime.combine(dt.date(1,1,1), Settimana.objects.get(id=4).martedi.getOrario()) + dt.timedelta(hours=1)).time())
'''