import datetime


"""
startdate ed enddate stabiliscono l'intervallo (centrato nella data odierna) 
entro cui viene verificata la presenza di controlli da effettuare.  
"""
startDate = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
endDate = startDate + datetime.timedelta(days=6)


"""
Orari in formato: datetime.time(HH,MM)
"""
inizio_turno = datetime.time(9, 0)
fine_turno = datetime.time(18, 0)


"""
Ogni orario che si vuole aggiungere alle scelte
deve essere prima creato come sopra, per poi essere aggiunto
alla tupla degli orari, rispettando il formato.
"""
orari = (
    (inizio_turno.strftime('%H:%M'), inizio_turno.strftime('%H:%M')),
    (fine_turno.strftime('%H:%M'), fine_turno.strftime('%H:%M')),
)


"""
Il preposto ha SOGLIA_ORE ore e SOGLIA_MINUTI minuti
per completare il giro dall'orario di inizo.
"""
SOGLIA_ORE = 1
SOGLIA_MINUTI = 0


"""- DATI per l'invio di EMAIL -"""
mittente_user = 'piano_master92@yahoo.it'
mittente_passw = 'zanarkand92'

