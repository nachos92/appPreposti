from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from setup.models import *
from .models import Settimana, Segnalazione
import datetime
from datetime import *
from django.views.decorators.csrf import csrf_exempt
import json
from parametri import *


"""
Costruisce un dizionario del tipo
diz['impiego'] = [ <listacontrolliassociati> ]

"""
def makeDict():
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
def makeJson(cod_prep, elenco, plan):

    index = 0
    diz = makeDict()
    prep = Preposto.objects.get(pk=cod_prep)

    if (len(plan) == 0):
        return ('[]')

    out = '{'
    '''
    Nome e cognome al momento non sono inseriti perche' prima
    bisogna decidere come implementare l'entita' preposto.
    '''

    # Aggiunta nome e cognome preposto
    out += '"nome":"'+prep.getNome()+\
           '","cognome":"'+prep.getCognome()+'",'

    # Aggiunta stato ('giro' completato o no)
    out += '"completato":"F",'

    # Aggiunta orario settimanale dei controlli.
    # out += '"orario":{'
    for k in plan:
        out += '"id":"' + str(k[8]) + '",'
        out += '"orario":{'
        out += '"lun":"' + k[2] \
               + '","mar":"' + k[3] \
               + '","mer":"' + k[4] \
               + '","gio":"' + k[5] \
               + '","ven":"' + k[6] \
               + '"},'

    k = date.today().weekday()

    if (k == 0):
        plan = plan.filter(lun_fatto=False, lun_check=False)
    if (k == 1):
        plan = plan.filter(mar_fatto=False, mar_check=False)
    if (k == 2):
        plan = plan.filter(mer_fatto=False, mer_check=False)
    if (k == 3):
        plan = plan.filter(gio_fatto=False, gio_check=False)
    if (k == 4):
        plan = plan.filter(ven_fatto=False, ven_check=False)

    out += '"dipendenti":['

    if (len(plan)==0):
        out += ']'
    else:

        for q in elenco:
            index_controlli = 0
            index += 1
            out += '{ "n_matricola":"' + q[0] + '",'\
                   + '"nome":"' + q[1] + '",' \
                   + '"cognome":"' + q[2] \
                   + '","impiego":"' \
                   + q[3] + '"'


            out += ',"controlli":['
            controlli = Impiego.objects.get(pk=q[3]).getControlli()
            if (len(controlli)>0):
                index_controlli2 = 0
                for controllo in controlli:
                    index_controlli2 += 1
                    out += '{"id":"'+str(controllo.id)+'","titolo":"'+str(controllo)+\
                           '","value":"F"}'
                    if index_controlli2 < len(controlli):
                        out+=','

            out += '],"controlli_adhoc":['

            index_extra = 0
            controlli_adhoc = Dipendente.objects.get(pk=q[0]).getList_ContrAdHoc()

            for extra in Dipendente.objects.get(pk=q[0]).getList_ContrAdHoc():
                index_extra += 1
                out += '{"titolo":"'+str(extra)+'","value":"F"}'

                if index_extra < len(controlli_adhoc):
                    out += ','

            out += ']'

            out += '}'

            if (index < len(elenco)):
                out += ','


        #Fine elenco dipendenti
        out += ']'

    #out += '"messaggio":'



    #Fine json
    out += '}'

    return out


"""
Ritorna un oggetto di lunghezza 0 se nella giornata attuale
e' gia' stato fatto il giro (se giornoattuale_fatto=true).
"""
def getWeek(cod_prep):
    planning = Settimana.objects.filter(data_inizio__range=[startDate, endDate],
                                       cod_preposto=cod_prep,
                                       completato=False).values_list('data_inizio',
                                                                     'area',
                                                                     'lun',
                                                                     'mar',
                                                                     'mer',
                                                                     'gio',
                                                                     'ven',
                                                                     'completato',
                                                                     'id'
                                                                     )
    '''
    k = date.today().weekday()

    if (k == 0):
        planning = planning.filter(lun_fatto=False, lun_check=False)
    if (k == 1):
        planning = planning.filter(mar_fatto=False, mar_check=False)
    if (k == 2):
        planning = planning.filter(mer_fatto=False, mer_check=False)
    if (k == 3):
        planning = planning.filter(gio_fatto=False, gio_check=False)
    if (k == 4):
        planning = planning.filter(ven_fatto=False, ven_check=False)
    '''


    return planning


""" Es. se io vado su localhost/8000/checks/56
mi stampa l'elenco dei dipendenti che il preposto 56
non ha ancora controllato.
"""
def controlloPlanning(request, cod_prep):
    gruppo_sottoposti = Preposto.objects.filter(id=cod_prep).values_list('sottoposti')

    # elenco dipendenti del settore che il preposto deve controllare
    dipendenti = Dipendente.objects.filter(impiego__in=gruppo_sottoposti).values_list('n_matricola',
                                                                                      'nome',
                                                                                      'cognome',
                                                                                      'impiego',
                                                                                      )
    #print "Dipendenti totali: " + str(len(dipendenti)) + '\n' + str(dipendenti)
    planning = getWeek(cod_prep)

    print "Invio json a client."

    return HttpResponse(
        makeJson(cod_prep, elenco=dipendenti, plan=planning),
        content_type='application/json'
    )



"""
Ricezione del json contenente i controlli con esito negativo di un dipendente.
Viene quindi creata una Segnalazione che riporta l'accaduto.
"""
@csrf_exempt
def ricezione(request, n_matricola):

    received_json_data = json.loads(request.body)

    if (len(received_json_data['controlli']) == 0):
        return HttpResponse('')

    # Creo una segnalazione di controllo non positivo su un determinato dipendente.
    dip = Dipendente.objects.get(n_matricola=n_matricola)
    testo = "Elenco controlli non rispettati da parte di "+str(received_json_data['nomeDip'])+' '+\
            str(received_json_data['cognomeDip'])+': \n \n'

    for m in received_json_data['controlli']:
        testo += "ID: "+str(m['id'])+'\t\t'+str(m['titolo'])+'\n'

    Segnalazione.create(dip, testo).save()

    print "Ricevuto json da CLIENT."

    return HttpResponse('')



@csrf_exempt
def daydone(request, planningId):
    plan = Settimana.objects.get(id=int(planningId))

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


