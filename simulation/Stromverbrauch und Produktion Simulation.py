import random
import time

from Verbraucher import Verbraucher

from Kraftwerk import Kraftwerk, KraftwerkStatus, Windpark
from Energiespeicher import Energiespeicher

# TODO: Von Überobjekt "Element" erben, in dem update(+zeit) als Funktion festgelegt ist        

# Simulation
uhrzeit = 0
def wohngebiet1_uhrzeit_bedarf_funktion(uhrzeit):
    if 0 <= uhrzeit <= 6:
        return random.randint(1, 2)
    elif 7 <= uhrzeit <= 9:
        return random.randint(100, 120)
    elif 10 <= uhrzeit <= 16:
        return random.randint(10, 20)
    elif 17 <= uhrzeit <= 20:
        return random.randint(125, 160)
    elif 21 <= uhrzeit <= 23:
        return random.randint(25, 35)
wohngebiet1 = Verbraucher(
    grundbedarf = 1000, 
    # TODO: Syntax für Inline-Deklaration finden & verwenden
    uhrzeit_bedarf_funktion = wohngebiet1_uhrzeit_bedarf_funktion
)
kraftwerk1 = Kraftwerk(
    initStatus = KraftwerkStatus.SHUTDOWN,
    initStatusMap = {
        KraftwerkStatus.SHUTDOWN: 0,
        KraftwerkStatus.LOW_POWER: 400,
        KraftwerkStatus.MID_POWER: 1100,
        KraftwerkStatus.MAX_POWER: 2000
    }
)
kraftwerk2 = Kraftwerk(
    initStatus = KraftwerkStatus.SHUTDOWN,
    initStatusMap = {
        KraftwerkStatus.SHUTDOWN: -20,
        KraftwerkStatus.LOW_POWER: 500,
        KraftwerkStatus.MID_POWER: 1500,
        KraftwerkStatus.MAX_POWER: 2600
    }
)
industrie1 = Verbraucher(
    grundbedarf = 1250
)
windpark1 = Windpark(
    initStatus = KraftwerkStatus.MAX_POWER,
    initStatusMap = {
        KraftwerkStatus.SHUTDOWN: 0,
        KraftwerkStatus.MAX_POWER: 500
    }
)
pumpspeicherwerk = Energiespeicher(
    kapazitaet = 2000,
    ladeverlust_anteil = 0.1,
    entladeverlust_anteil = 0.2
)

while True:
    if uhrzeit == 23:
        uhrzeit = 0
    else:
        uhrzeit += 1

    # Energiebedarf berechnen
    energiebedarf = wohngebiet1.berechne_bedarf(uhrzeit) + industrie1.berechne_bedarf(uhrzeit)
    #print(energiebedarf) #Kontrolle ob Windpark einbezogen wird
    energiebedarf = energiebedarf - windpark1.get_leistung()

    # Kohlekraftwerk steuern (sehr einfache Logik hier)
    if energiebedarf > 1100:
        kraftwerk1.set_status(KraftwerkStatus.MAX_POWER)
    elif energiebedarf > 400:
        kraftwerk1.set_status(KraftwerkStatus.MID_POWER)
    else:
        kraftwerk1.set_status(KraftwerkStatus.LOW_POWER)
    
    ueberschuss = kraftwerk1.get_leistung() - energiebedarf

    # Ausgabe
    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt (Derzeit nur auf Kohlekraftwerk): {energiebedarf} MW")
    print(f"Kohlekraftwerk: {kraftwerk1.status} mit {kraftwerk1.get_leistung()} MW")
    print(f"Überschuss: {ueberschuss} MW")
    print("-" * 30)

    # (Für Debugging oder Simulation bricht er nach einer Iteration ab) (Nicht mehr) (Jetzt wartet er einfach kurz)
    time.sleep(1)

